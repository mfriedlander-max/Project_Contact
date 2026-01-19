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
