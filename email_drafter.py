#!/usr/bin/env python3
"""
Outlook Email Drafter - Automates email drafting via Outlook web
and tracks status in Google Sheets.

Usage:
    python3 email_drafter.py --login           # Save Outlook session
    python3 email_drafter.py --create-drafts   # Create drafts from sheet
    python3 email_drafter.py --sync-sent       # Update sheet with sent emails
    python3 email_drafter.py --set-subject "Subject line here"
"""

import argparse
import json
import os
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright

CONFIG_FILE = "outlook_config.json"
CREDENTIALS_FILE = "credentials/google_sheets_key.json"


def load_config():
    """Load configuration from JSON file."""
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    """Save configuration to JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_google_sheet(config):
    """Connect to Google Sheet and return worksheet."""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(config["google_sheet_id"])
    return sheet.sheet1


def get_contacts_to_draft(worksheet):
    """Get contacts that need drafts created."""
    records = worksheet.get_all_records()
    contacts = []
    for i, row in enumerate(records, start=2):  # Row 2 is first data row
        # Skip if already drafted or no email
        if row.get("Email Status") in ["drafted", "sent"]:
            continue
        if not row.get("Email"):
            continue
        contacts.append({
            "row": i,
            "name": row.get("Name", ""),
            "email": row.get("Email", ""),
            "company": row.get("Company", ""),
            "insert": row.get("Personalized Insert", ""),
        })
    return contacts


def update_draft_status(worksheet, row, status="drafted"):
    """Update the Email Status column for a contact."""
    # Find Email Status column
    headers = worksheet.row_values(1)
    status_col = headers.index("Email Status") + 1 if "Email Status" in headers else None
    draft_col = headers.index("Draft Created") + 1 if "Draft Created" in headers else None

    if status_col:
        worksheet.update_cell(row, status_col, status)
    if draft_col:
        from datetime import datetime
        worksheet.update_cell(row, draft_col, datetime.now().strftime("%Y-%m-%d %H:%M"))


def build_email_body(config, contact):
    """Build the email body from template and contact data."""
    template = config["template"]

    # Get first name
    first_name = contact["name"].split()[0] if contact["name"] else "there"

    # Get personalized insert or use generic
    insert = contact.get("insert", "")
    if not insert:
        insert = "I'd love to learn from your experience."

    body = template.format(name=first_name, insert=insert)
    return body


def main():
    parser = argparse.ArgumentParser(description="Outlook Email Drafter")
    parser.add_argument("--login", action="store_true", help="Login to Outlook and save session")
    parser.add_argument("--create-drafts", action="store_true", help="Create draft emails from sheet")
    parser.add_argument("--sync-sent", action="store_true", help="Sync sent emails to sheet")
    parser.add_argument("--set-subject", type=str, help="Set the email subject line")

    args = parser.parse_args()
    config = load_config()

    if args.set_subject:
        config["subject_line"] = args.set_subject
        save_config(config)
        print(f"Subject line set to: {args.set_subject}")
        return

    if args.login:
        outlook_login(config)
    elif args.create_drafts:
        create_drafts(config)
    elif args.sync_sent:
        sync_sent_emails(config)
    else:
        parser.print_help()


def outlook_login(config):
    """Login to Outlook and save session for reuse."""
    session_dir = Path(config["session_dir"])
    session_dir.mkdir(exist_ok=True)

    print("Opening Outlook login page...")
    print("Please log in manually. The session will be saved for future use.")

    with sync_playwright() as p:
        # Launch visible browser for login
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        # Navigate to Outlook
        page.goto("https://outlook.office.com/mail/")

        print("\n" + "="*50)
        print("Log in to your Middlebury Outlook account.")
        print("Once you see your inbox, press Enter here to save the session.")
        print("="*50 + "\n")

        input("Press Enter when logged in...")

        # Verify we're logged in by checking for inbox
        if "mail" in page.url.lower():
            print("Session saved successfully!")
        else:
            print("Warning: May not be fully logged in. URL:", page.url)

        browser.close()

    print(f"Session stored in: {session_dir}")


def create_drafts(config):
    """Create draft emails in Outlook from Google Sheet contacts."""
    session_dir = Path(config["session_dir"])

    if not session_dir.exists():
        print("Error: No saved session. Run --login first.")
        return

    if config["subject_line"] == "TBD":
        print("Error: Subject line not set. Run --set-subject first.")
        return

    # Get contacts from sheet
    print("Connecting to Google Sheet...")
    worksheet = get_google_sheet(config)
    contacts = get_contacts_to_draft(worksheet)

    if not contacts:
        print("No contacts need drafts.")
        return

    print(f"Found {len(contacts)} contacts to draft.")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=True,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        # Go to Outlook
        page.goto("https://outlook.office.com/mail/")
        page.wait_for_load_state("networkidle")

        # Check if logged in
        if "login" in page.url.lower() or "signin" in page.url.lower():
            print("Error: Session expired. Run --login again.")
            browser.close()
            return

        print("Connected to Outlook.")

        for i, contact in enumerate(contacts, 1):
            print(f"\n[{i}/{len(contacts)}] Creating draft for {contact['name']}...")

            try:
                # Click New Mail button
                page.click('button[aria-label="New mail"]')
                page.wait_for_timeout(1000)

                # Fill To field
                to_field = page.locator('input[aria-label="To"]')
                to_field.fill(contact["email"])
                page.wait_for_timeout(500)

                # Fill Subject
                subject_field = page.locator('input[aria-label="Add a subject"]')
                subject_field.fill(config["subject_line"])
                page.wait_for_timeout(500)

                # Fill Body
                body = build_email_body(config, contact)
                body_field = page.locator('div[aria-label="Message body"]')
                body_field.fill(body)
                page.wait_for_timeout(500)

                # Close to save as draft (click X or press Escape)
                page.keyboard.press("Escape")
                page.wait_for_timeout(1000)

                # Update sheet
                update_draft_status(worksheet, contact["row"], "drafted")
                print(f"  Draft created for {contact['email']}")

            except Exception as e:
                print(f"  Error: {e}")
                continue

        browser.close()

    print(f"\nDone! Created {len(contacts)} drafts.")


def sync_sent_emails(config):
    """Scan Outlook Sent folder and update sheet for matching emails."""
    session_dir = Path(config["session_dir"])

    if not session_dir.exists():
        print("Error: No saved session. Run --login first.")
        return

    # Get contacts from sheet that are in "drafted" status
    print("Connecting to Google Sheet...")
    worksheet = get_google_sheet(config)
    records = worksheet.get_all_records()

    drafted_emails = {}
    for i, row in enumerate(records, start=2):
        if row.get("Email Status") == "drafted" and row.get("Email"):
            drafted_emails[row["Email"].lower()] = i

    if not drafted_emails:
        print("No drafted emails to check.")
        return

    print(f"Checking {len(drafted_emails)} drafted contacts...")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=True,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        # Go to Sent folder
        page.goto("https://outlook.office.com/mail/sentitems")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        # Check if logged in
        if "login" in page.url.lower() or "signin" in page.url.lower():
            print("Error: Session expired. Run --login again.")
            browser.close()
            return

        print("Connected to Outlook Sent folder.")

        # Get sent email recipients from the list
        sent_count = 0

        # Find all email items in sent folder
        email_items = page.locator('[data-convid]').all()[:50]  # Check last 50

        for item in email_items:
            try:
                # Click to open email
                item.click()
                page.wait_for_timeout(500)

                # Look for recipient in the To field
                to_element = page.locator('span[aria-label^="To:"]').first
                if to_element.count() > 0:
                    to_text = to_element.text_content().lower()

                    # Check against our drafted emails
                    for email, row in list(drafted_emails.items()):
                        if email in to_text:
                            # Found a match - update sheet
                            headers = worksheet.row_values(1)
                            status_col = headers.index("Email Status") + 1
                            sent_col = headers.index("Sent Date") + 1 if "Sent Date" in headers else None

                            worksheet.update_cell(row, status_col, "sent")
                            if sent_col:
                                from datetime import datetime
                                worksheet.update_cell(row, sent_col, datetime.now().strftime("%Y-%m-%d"))

                            print(f"  Marked as sent: {email}")
                            del drafted_emails[email]
                            sent_count += 1
                            break

            except Exception as e:
                continue

        browser.close()

    print(f"\nDone! Found {sent_count} sent emails.")


if __name__ == "__main__":
    main()
