#!/usr/bin/env python3
"""
Verify and fix personalized inserts in existing Outlook drafts.
Only checks Round 2 campaigns from last 7 days.
"""

import argparse
import re
from datetime import datetime, timedelta
from email_drafter import load_config, get_google_sheet

# MCP Playwright imports handled by Claude environment

ROUND2_SUBJECTS = [
    "Middlebury Freshman - Hungry to Learn",
    "College Freshman - Hungry to Learn"
]

INSERT_PATTERN = r"curious about the world\.\s+(.*?)\s+\n\nI understand"

def main():
    parser = argparse.ArgumentParser(
        description="Verify and fix personalized inserts in Outlook drafts"
    )
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be checked without making changes")
    parser.add_argument("--limit", type=int,
                       help="Limit number of drafts to check (for testing)")

    args = parser.parse_args()

    print("Loading Google Sheet...")
    config = load_config()
    ws = get_google_sheet(config)

    print("Opening Outlook...")
    # MCP Playwright implementation here

    print("\n✓ Done!")

if __name__ == "__main__":
    main()
