#!/usr/bin/env python3
"""
Verify and fix personalized inserts in existing Outlook drafts.
Only checks Round 2 campaigns from last 7 days.
"""

import argparse
import re
import time
from datetime import datetime, timedelta
from email_drafter import load_config, get_google_sheet

# MCP Playwright will be called via Claude's tool system

ROUND2_SUBJECTS = [
    "Middlebury Freshman - Hungry to Learn",
    "College Freshman - Hungry to Learn"
]

INSERT_PATTERN = r"curious about the world\.\s+(.*?)\s+I understand"

BANNED_PATTERNS = [
    "i came across", "i noticed", "your remarkable",
    "your impressive", "i would be honored", "resonates with me",
    "aligns with my interests"
]


def extract_insert_from_body(body_text: str) -> str:
    """Extract personalized insert using regex."""
    # Try multiline pattern
    match = re.search(INSERT_PATTERN, body_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def validate_insert_quality(insert: str) -> tuple:
    """Check quality rules: word count, banned phrases, punctuation."""
    errors = []

    word_count = len(insert.split())
    if word_count < 15:
        errors.append(f"Too short: {word_count} words (need 15-25)")
    elif word_count > 25:
        errors.append(f"Too long: {word_count} words (need 15-25)")

    for banned in BANNED_PATTERNS:
        if banned in insert.lower():
            errors.append(f"Banned phrase: '{banned}'")

    if not insert.strip().endswith(('.', '!', '?')):
        errors.append("No punctuation")

    is_valid = len(errors) == 0
    return is_valid, errors


def find_contact_in_sheet(worksheet, email: str):
    """Look up contact by email in Google Sheet."""
    records = worksheet.get_all_records()
    for i, row in enumerate(records, start=2):
        if row.get("Email", "").lower() == email.lower():
            return i, row
    return None, None


def present_for_verification(draft, contact_row):
    """Display draft info for user to review with Claude."""
    print(f"\n{'='*70}")
    print(f"Contact: {draft['recipient_name']} ({draft['recipient_email']})")
    print(f"Company: {contact_row.get('Company', 'Unknown')}")
    print(f"\nCurrent insert:")
    print(f'  "{draft["insert"]}"')
    print(f"  Word count: {len(draft['insert'].split())}")

    # Check quality
    is_valid, errors = validate_insert_quality(draft["insert"])
    if not is_valid:
        print(f"\n⚠️  Quality issues:")
        for error in errors:
            print(f"    - {error}")

    print(f"\n{'='*70}")
    print("\nNext steps:")
    print("  1. Ask Claude to research this person with WebSearch")
    print("  2. Claude will provide findings + suggested fix")
    print("  3. Choose action below")


def update_sheet_insert(worksheet, row_num: int, new_insert: str):
    """Update Personalized Insert column in Google Sheet."""
    headers = worksheet.row_values(1)
    insert_col = headers.index("Personalized Insert") + 1

    worksheet.update_cell(row_num, insert_col, new_insert)
    print(f"    ✓ Updated row {row_num} in sheet")


def main():
    parser = argparse.ArgumentParser(
        description="Verify and fix personalized inserts in Outlook drafts"
    )
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be checked without making changes")
    parser.add_argument("--limit", type=int,
                       help="Limit number of drafts to check (for testing)")

    args = parser.parse_args()

    try:
        print("Loading Google Sheet...")
        config = load_config()
        ws = get_google_sheet(config)

        print("\n" + "="*70)
        print("OUTLOOK DRAFT VERIFICATION")
        print("="*70)
        print("\nThis script requires MCP Playwright integration via Claude.")
        print("Claude will navigate Outlook, extract drafts, and help verify inserts.")
        print("\nInstructions for Claude:")
        print("  1. Navigate to https://outlook.office.com/mail/drafts")
        print("  2. Wait for page load (5 seconds)")
        print("  3. Take snapshot to see draft list")
        print("  4. For each draft with Round 2 subject (Middlebury/College Freshman):")
        print("     - Click to open draft")
        print("     - Extract email body")
        print("     - Extract recipient email from To: field")
        print("     - Extract recipient name from 'Hello {name}' line")
        print("     - Extract personalized insert using regex")
        print("     - Present to user for verification")
        print("  5. User will ask you to research each person")
        print("  6. You'll suggest fixes using WebSearch")
        print("  7. User approves fixes, you update Outlook + Sheet")
        print("\n" + "="*70)

        print("\nReady to start? (Press Ctrl+C to cancel)")
        input("\nPress Enter when Claude has navigated to Outlook drafts...")

        # Stats tracking
        checked_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0

        print("\n✓ Sheet loaded. Ready for draft verification.")
        print("\nClaude: Please begin navigating drafts and presenting them for verification.")
        print("(User will interact with Claude to verify each draft)")

        # Summary at end
        print(f"\n{'='*70}")
        print("Session ended. Use Claude to continue verification.")
        print(f"{'='*70}")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("If session expired, run: python3 email_drafter.py --login")
        return


if __name__ == "__main__":
    main()
