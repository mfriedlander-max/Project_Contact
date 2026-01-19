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
    """Login to Outlook and save session."""
    print("Login not yet implemented")


def create_drafts(config):
    """Create draft emails from Google Sheet data."""
    print("Create drafts not yet implemented")


def sync_sent_emails(config):
    """Scan Sent folder and update sheet."""
    print("Sync sent not yet implemented")


if __name__ == "__main__":
    main()
