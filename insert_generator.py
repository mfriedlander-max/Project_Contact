#!/usr/bin/env python3
"""
Insert Generator - Research contacts and generate personalized email inserts.

Uses Claude API with web search to research contacts and generate 15-25 word
personalized inserts for cold outreach emails.

Usage:
    python3 insert_generator.py -i contacts.csv -o output.csv
    python3 insert_generator.py -i contacts.csv -o output.csv --model haiku
    python3 insert_generator.py -i contacts.csv -o output.csv --delay 2.0
"""

import argparse
import csv
import json
import logging
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import anthropic
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
CONFIG_FILE = "outlook_config.json"
CREDENTIALS_FILE = "credentials/google_sheets_key.json"
PROMPT_FILE = "email_personalization_prompt.md"
LOG_FILE = "insert_generator.log"

# Model mapping
MODELS = {
    "haiku": "claude-haiku-4-20250514",
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-20250514",
}

# Required input columns
REQUIRED_COLUMNS = ["Name", "Company", "Email", "Title"]

# Banned phrases for insert validation
BANNED_PHRASES = [
    "i came across",
    "i noticed",
    "your remarkable",
    "your impressive",
    "your incredible",
    "i would be honored",
    "i am deeply interested",
    "your journey",
    "your path inspires",
    "as someone who",
    "i believe that",
    "resonates with me",
    "i am passionate about",
    "aligns with my interests",
]


def setup_logging():
    """Configure logging to file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def get_current_branch() -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def load_config() -> dict:
    """Load configuration from JSON file."""
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def load_prompt_rules() -> str:
    """Load insert generation rules from prompt file."""
    if not os.path.exists(PROMPT_FILE):
        raise FileNotFoundError(
            f"Prompt file not found: {PROMPT_FILE}. "
            "This file is required for insert generation rules."
        )
    with open(PROMPT_FILE, "r") as f:
        return f.read()


def get_google_sheet(config: dict):
    """Connect to Google Sheet and return worksheet."""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(config["google_sheet_id"])
    return sheet.sheet1


def load_input_csv(filepath: str) -> list[dict]:
    """Load contacts from input CSV file."""
    contacts = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append(dict(row))
    return contacts


def validate_required_columns(contact: dict) -> tuple[bool, str]:
    """Check if contact has all required columns with values."""
    for col in REQUIRED_COLUMNS:
        if not contact.get(col, "").strip():
            return False, col
    return True, ""


def load_processed_contacts(output_path: str) -> set[str]:
    """Load already-processed contacts from output CSV for checkpoint."""
    processed = set()
    if not os.path.exists(output_path):
        return processed

    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create unique key: Email if present, else Name+Company
            email = row.get("Email", "").strip().lower()
            if email:
                processed.add(f"email:{email}")
            else:
                name = row.get("Name", "").strip().lower()
                company = row.get("Company", "").strip().lower()
                processed.add(f"name_company:{name}|{company}")
    return processed


def is_already_processed(contact: dict, processed: set[str]) -> bool:
    """Check if contact was already processed."""
    email = contact.get("Email", "").strip().lower()
    if email and f"email:{email}" in processed:
        return True

    name = contact.get("Name", "").strip().lower()
    company = contact.get("Company", "").strip().lower()
    if f"name_company:{name}|{company}" in processed:
        return True

    return False


def validate_insert(insert: str) -> tuple[bool, list[str]]:
    """Validate insert against rules. Returns (is_valid, list of issues)."""
    issues = []

    # Word count check
    words = insert.split()
    word_count = len(words)
    if word_count < 15:
        issues.append(f"Too short: {word_count} words (need 15-25)")
    elif word_count > 25:
        issues.append(f"Too long: {word_count} words (need 15-25)")

    # Punctuation check
    if not insert.strip().endswith((".", "!", "?")):
        issues.append("Missing ending punctuation (. ! ?)")

    # Banned phrases check
    insert_lower = insert.lower()
    for phrase in BANNED_PHRASES:
        if phrase in insert_lower:
            issues.append(f"Contains banned phrase: '{phrase}'")

    # Em dash check
    if "—" in insert:
        issues.append("Contains em dash (use 'and' instead)")

    return len(issues) == 0, issues


def assign_confidence(
    insert: str, sources: list[str], research_quality: str
) -> str:
    """Assign confidence level based on research quality and insert validation."""
    is_valid, issues = validate_insert(insert)

    # If insert has validation issues, LOW confidence
    if not is_valid:
        return "LOW"

    # If research found minimal info, LOW confidence
    if research_quality == "minimal" or not sources:
        return "LOW"

    # If research from 2+ sources, HIGH confidence
    if len(sources) >= 2:
        return "HIGH"

    # Single source = MEDIUM
    return "MEDIUM"


def research_and_generate_insert(
    client: anthropic.Anthropic,
    contact: dict,
    prompt_rules: str,
    model: str,
) -> dict:
    """
    Research contact and generate personalized insert using Claude API with web search.
    Returns dict with: insert, word_count, confidence, sources
    """
    name = contact.get("Name", "")
    company = contact.get("Company", "")
    title = contact.get("Title", "")

    system_prompt = f"""You are helping write personalized email inserts for cold outreach.

{prompt_rules}

Your task:
1. Research the person using web search to find accurate, current information
2. Generate ONE personalized insert sentence (15-25 words exactly)
3. Return your response in this exact JSON format:
{{
    "insert": "Your 15-25 word sentence here.",
    "word_count": 22,
    "sources": ["Source 1", "Source 2"],
    "research_quality": "detailed|basic|minimal"
}}

research_quality meanings:
- "detailed": Found multiple sources with specific facts about the person
- "basic": Found some info from one source
- "minimal": Very little or no specific info found (use generic fallback)

If you can't find much info, use this fallback pattern:
"I've been thinking a lot about [industry] and would love to learn from your experience building [Company]."

CRITICAL: The insert MUST be 15-25 words. Count carefully before responding."""

    user_message = f"""Research and generate a personalized insert for:
Name: {name}
Company: {company}
Title: {title}

Use web search to find current information about this person, then generate an insert."""

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system_prompt,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 5,
                }
            ],
            messages=[{"role": "user", "content": user_message}],
        )

        # Extract text response
        text_content = ""
        for block in response.content:
            if hasattr(block, "text"):
                text_content += block.text

        # Parse JSON from response
        json_match = re.search(r"\{[\s\S]*\}", text_content)
        if json_match:
            result = json.loads(json_match.group())
            insert = result.get("insert", "")
            sources = result.get("sources", [])
            research_quality = result.get("research_quality", "minimal")

            # Validate and assign confidence
            word_count = len(insert.split())
            confidence = assign_confidence(insert, sources, research_quality)

            return {
                "insert": insert,
                "word_count": word_count,
                "confidence": confidence,
                "sources": sources,
            }

        # Fallback if JSON parsing fails
        logger.warning(f"Could not parse JSON from response for {name}")
        return {
            "insert": f"I've been thinking a lot about {company}'s work and would love to learn from your experience.",
            "word_count": 17,
            "confidence": "LOW",
            "sources": [],
        }

    except anthropic.RateLimitError:
        logger.error(f"Rate limit hit for {name}, waiting...")
        raise
    except Exception as e:
        logger.error(f"API error for {name}: {e}")
        return {
            "insert": f"I've been thinking a lot about {company}'s work and would love to learn from your experience.",
            "word_count": 17,
            "confidence": "LOW",
            "sources": [],
        }


def write_csv_row(filepath: str, row: dict, is_first: bool = False):
    """Append a row to CSV file. Creates file with headers if is_first."""
    fieldnames = [
        "Campaign",
        "Name",
        "Email",
        "Email Confidence",
        "Company",
        "Title",
        "Personalized Insert",
        "Word Count",
        "Insert Confidence",
        "Sources",
    ]

    mode = "w" if is_first else "a"
    with open(filepath, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_first:
            writer.writeheader()
        writer.writerow(row)


def add_to_google_sheet(worksheet, row_data: dict, headers: list[str]):
    """Add a new row to Google Sheet. Writes by column name."""
    # Find next empty row
    all_values = worksheet.get_all_values()
    next_row = len(all_values) + 1

    # Map column names to positions
    col_map = {h: i + 1 for i, h in enumerate(headers)}

    # Write each field by column name
    for field, value in row_data.items():
        if field in col_map:
            worksheet.update_cell(next_row, col_map[field], value)


def ensure_sheet_columns(worksheet) -> list[str]:
    """Ensure required columns exist in sheet. Returns current headers."""
    headers = worksheet.row_values(1)
    required = [
        "Campaign",
        "Name",
        "Email",
        "Email Confidence",
        "Company",
        "Title",
        "Personalized Insert",
        "Word Count",
        "Insert Confidence",
        "Sources",
        "Email Status",
        "Draft Created",
        "Sent Date",
    ]

    # Add missing columns
    for col in required:
        if col not in headers:
            next_col = len(headers) + 1
            worksheet.update_cell(1, next_col, col)
            headers.append(col)
            logger.info(f"Added column to sheet: {col}")

    return headers


def main():
    parser = argparse.ArgumentParser(
        description="Research contacts and generate personalized email inserts"
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Input CSV file with contacts"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="inserts_output.csv",
        help="Output CSV file (default: inserts_output.csv)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds between API calls (default: 1.0)",
    )
    parser.add_argument(
        "--model",
        choices=["haiku", "sonnet", "opus"],
        default="sonnet",
        help="Claude model to use (default: sonnet)",
    )

    args = parser.parse_args()

    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        print("\nError: ANTHROPIC_API_KEY not set")
        print("Run: export ANTHROPIC_API_KEY='your_key_here'")
        return 1

    # Get current branch (campaign name)
    campaign = get_current_branch()
    if campaign == "main":
        logger.warning("Running on main branch - consider using a feature branch")
        print("\n⚠️  Warning: Running on main branch")
        print("   Consider: git checkout -b round-X-campaign-name\n")

    # Load prompt rules
    try:
        prompt_rules = load_prompt_rules()
    except FileNotFoundError as e:
        logger.error(str(e))
        print(f"\nError: {e}")
        return 1

    # Load config for Google Sheet
    config = load_config()

    # Load input contacts
    logger.info(f"Loading contacts from: {args.input}")
    contacts = load_input_csv(args.input)
    logger.info(f"Found {len(contacts)} contacts in input file")

    # Load already-processed contacts (checkpoint)
    processed = load_processed_contacts(args.output)
    if processed:
        logger.info(f"Found {len(processed)} already-processed contacts (will skip)")

    # Connect to Google Sheet
    logger.info("Connecting to Google Sheet...")
    worksheet = get_google_sheet(config)
    headers = ensure_sheet_columns(worksheet)

    # Initialize Claude client
    client = anthropic.Anthropic(api_key=api_key)
    model = MODELS[args.model]
    logger.info(f"Using model: {args.model} ({model})")

    # Process contacts
    is_first_write = not os.path.exists(args.output)
    processed_count = 0
    skipped_count = 0
    error_count = 0

    for i, contact in enumerate(contacts, 1):
        name = contact.get("Name", "Unknown")

        # Validate required columns
        is_valid, missing_col = validate_required_columns(contact)
        if not is_valid:
            logger.warning(f"{name} | SKIP | Missing required field: {missing_col}")
            skipped_count += 1
            continue

        # Check if already processed (checkpoint)
        if is_already_processed(contact, processed):
            logger.info(f"{name} | SKIP | Already processed")
            skipped_count += 1
            continue

        # Process this contact
        logger.info(f"[{i}/{len(contacts)}] {name} | PROCESSING")

        try:
            # Research and generate insert
            result = research_and_generate_insert(
                client, contact, prompt_rules, model
            )

            # Prepare output row
            output_row = {
                "Campaign": campaign,
                "Name": contact.get("Name", ""),
                "Email": contact.get("Email", ""),
                "Email Confidence": contact.get("Email Confidence", ""),
                "Company": contact.get("Company", ""),
                "Title": contact.get("Title", ""),
                "Personalized Insert": result["insert"],
                "Word Count": result["word_count"],
                "Insert Confidence": result["confidence"],
                "Sources": ", ".join(result["sources"]),
            }

            # Write to CSV (checkpoint)
            write_csv_row(args.output, output_row, is_first=is_first_write)
            is_first_write = False

            # Add to Google Sheet
            sheet_row = output_row.copy()
            sheet_row["Email Status"] = ""  # Ready for drafting
            add_to_google_sheet(worksheet, sheet_row, headers)

            logger.info(
                f"{name} | DONE | {result['word_count']} words, "
                f"{result['confidence']} confidence"
            )
            processed_count += 1

            # Rate limiting
            if i < len(contacts):
                time.sleep(args.delay)

        except anthropic.RateLimitError:
            # Exponential backoff
            for wait_time in [5, 10, 20]:
                logger.warning(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                try:
                    result = research_and_generate_insert(
                        client, contact, prompt_rules, model
                    )
                    # Success - write and continue
                    output_row = {
                        "Campaign": campaign,
                        "Name": contact.get("Name", ""),
                        "Email": contact.get("Email", ""),
                        "Email Confidence": contact.get("Email Confidence", ""),
                        "Company": contact.get("Company", ""),
                        "Title": contact.get("Title", ""),
                        "Personalized Insert": result["insert"],
                        "Word Count": result["word_count"],
                        "Insert Confidence": result["confidence"],
                        "Sources": ", ".join(result["sources"]),
                    }
                    write_csv_row(args.output, output_row, is_first=is_first_write)
                    is_first_write = False
                    sheet_row = output_row.copy()
                    sheet_row["Email Status"] = ""
                    add_to_google_sheet(worksheet, sheet_row, headers)
                    processed_count += 1
                    break
                except anthropic.RateLimitError:
                    continue
            else:
                logger.error(f"{name} | FAIL | Rate limit exceeded after retries")
                error_count += 1

        except Exception as e:
            logger.error(f"{name} | ERROR | {e}")
            error_count += 1

    # Summary
    print(f"\n{'='*50}")
    print("Summary:")
    print(f"  Processed: {processed_count}")
    print(f"  Skipped:   {skipped_count}")
    print(f"  Errors:    {error_count}")
    print(f"  Output:    {args.output}")
    print(f"  Log:       {LOG_FILE}")
    print(f"{'='*50}")

    logger.info(
        f"Complete. Processed: {processed_count}, "
        f"Skipped: {skipped_count}, Errors: {error_count}"
    )

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    exit(main())
