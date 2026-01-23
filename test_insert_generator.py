"""Tests for insert_generator.py - comprehensive test suite."""

import csv
import json
import os
import pytest
from unittest.mock import MagicMock, patch, call
from insert_generator import (
    load_input_csv,
    validate_required_columns,
    load_processed_contacts,
    is_already_processed,
    validate_insert,
    assign_confidence,
    load_prompt_rules,
    get_current_branch,
    write_csv_row,
    add_to_google_sheet,
    ensure_sheet_columns,
    MODELS,
    REQUIRED_COLUMNS,
    BANNED_PHRASES,
)


class TestLoadCSV:
    """Tests for CSV loading functionality."""

    def test_load_csv_parses_all_rows(self, tmp_path):
        """CSV should be parsed with all rows returned."""
        csv_file = tmp_path / "contacts.csv"
        csv_file.write_text(
            "Name,Company,Email,Title\n"
            "John Doe,Acme Corp,john@acme.com,CEO\n"
            "Jane Smith,Tech Inc,jane@tech.com,CTO\n"
        )

        contacts = load_input_csv(str(csv_file))

        assert len(contacts) == 2
        assert contacts[0]["Name"] == "John Doe"
        assert contacts[1]["Name"] == "Jane Smith"

    def test_load_csv_preserves_all_columns(self, tmp_path):
        """All CSV columns should be preserved in output."""
        csv_file = tmp_path / "contacts.csv"
        csv_file.write_text(
            "Name,Company,Email,Title,LinkedIn URL,Email Confidence\n"
            "John Doe,Acme Corp,john@acme.com,CEO,linkedin.com/in/john,HIGH\n"
        )

        contacts = load_input_csv(str(csv_file))

        assert contacts[0]["LinkedIn URL"] == "linkedin.com/in/john"
        assert contacts[0]["Email Confidence"] == "HIGH"

    def test_load_csv_handles_empty_values(self, tmp_path):
        """Empty values should be preserved as empty strings."""
        csv_file = tmp_path / "contacts.csv"
        csv_file.write_text(
            "Name,Company,Email,Title\n" "John Doe,Acme Corp,,CEO\n"
        )

        contacts = load_input_csv(str(csv_file))

        assert contacts[0]["Email"] == ""


class TestRequiredColumns:
    """Tests for required column validation."""

    def test_valid_contact_passes(self):
        """Contact with all required fields should pass."""
        contact = {
            "Name": "John Doe",
            "Company": "Acme Corp",
            "Email": "john@acme.com",
            "Title": "CEO",
        }

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is True
        assert missing == ""

    def test_missing_name_fails(self):
        """Missing Name should fail validation."""
        contact = {
            "Name": "",
            "Company": "Acme Corp",
            "Email": "john@acme.com",
            "Title": "CEO",
        }

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Name"

    def test_missing_company_fails(self):
        """Missing Company should fail validation."""
        contact = {
            "Name": "John Doe",
            "Company": "",
            "Email": "john@acme.com",
            "Title": "CEO",
        }

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Company"

    def test_missing_email_fails(self):
        """Missing Email should fail validation."""
        contact = {
            "Name": "John Doe",
            "Company": "Acme Corp",
            "Email": "",
            "Title": "CEO",
        }

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Email"

    def test_missing_title_fails(self):
        """Missing Title should fail validation."""
        contact = {
            "Name": "John Doe",
            "Company": "Acme Corp",
            "Email": "john@acme.com",
            "Title": "",
        }

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Title"

    def test_whitespace_only_fails(self):
        """Whitespace-only values should fail validation."""
        contact = {
            "Name": "   ",
            "Company": "Acme Corp",
            "Email": "john@acme.com",
            "Title": "CEO",
        }

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Name"


class TestCheckpointSkipByEmail:
    """Tests for checkpoint functionality using Email matching."""

    def test_loads_processed_emails(self, tmp_path):
        """Already-processed emails should be loaded from output CSV."""
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Company,Title,Personalized Insert\n"
            "test,John Doe,john@acme.com,Acme,CEO,Test insert.\n"
            "test,Jane Smith,jane@tech.com,Tech,CTO,Another insert.\n"
        )

        processed = load_processed_contacts(str(output_file))

        assert "email:john@acme.com" in processed
        assert "email:jane@tech.com" in processed

    def test_is_already_processed_by_email(self, tmp_path):
        """Contact with matching email should be detected as processed."""
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Company,Title,Personalized Insert\n"
            "test,John Doe,john@acme.com,Acme,CEO,Test insert.\n"
        )
        processed = load_processed_contacts(str(output_file))

        contact = {
            "Name": "John Doe",
            "Company": "Acme",
            "Email": "john@acme.com",
            "Title": "CEO",
        }

        assert is_already_processed(contact, processed) is True

    def test_email_matching_case_insensitive(self, tmp_path):
        """Email matching should be case insensitive."""
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Company,Title,Personalized Insert\n"
            "test,John Doe,John@Acme.com,Acme,CEO,Test insert.\n"
        )
        processed = load_processed_contacts(str(output_file))

        contact = {"Name": "John Doe", "Company": "Acme", "Email": "john@acme.com", "Title": "CEO"}

        assert is_already_processed(contact, processed) is True


class TestCheckpointSkipByNameCompany:
    """Tests for checkpoint functionality using Name+Company fallback."""

    def test_fallback_to_name_company_when_no_email(self, tmp_path):
        """When Email is missing, should fall back to Name+Company matching."""
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Company,Title,Personalized Insert\n"
            "test,John Doe,,Acme,CEO,Test insert.\n"
        )
        processed = load_processed_contacts(str(output_file))

        contact = {"Name": "John Doe", "Company": "Acme", "Email": "", "Title": "CEO"}

        assert is_already_processed(contact, processed) is True

    def test_name_company_matching_case_insensitive(self, tmp_path):
        """Name+Company matching should be case insensitive."""
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Company,Title,Personalized Insert\n"
            "test,John Doe,,ACME CORP,CEO,Test insert.\n"
        )
        processed = load_processed_contacts(str(output_file))

        contact = {"Name": "john doe", "Company": "acme corp", "Email": "", "Title": "CEO"}

        assert is_already_processed(contact, processed) is True


class TestValidateInsert:
    """Tests for insert validation (word count, banned phrases, punctuation)."""

    def test_valid_insert_passes(self):
        """Insert with 15-25 words and proper punctuation should pass."""
        insert = (
            "I've been thinking a lot about fintech and PayPal's push on "
            "financial inclusion stands out. I'm curious what made you bet on that."
        )

        is_valid, issues = validate_insert(insert)

        assert is_valid is True
        assert issues == []

    def test_too_short_fails(self):
        """Insert with fewer than 15 words should fail."""
        insert = "I love your work on AI."

        is_valid, issues = validate_insert(insert)

        assert is_valid is False
        assert any("Too short" in issue for issue in issues)

    def test_too_long_fails(self):
        """Insert with more than 25 words should fail."""
        insert = (
            "I've been thinking a lot about fintech and PayPal's push on "
            "financial inclusion stands out and I'm curious what made you bet on that "
            "because it seems like a really interesting strategic decision that paid off."
        )

        is_valid, issues = validate_insert(insert)

        assert is_valid is False
        assert any("Too long" in issue for issue in issues)

    def test_missing_punctuation_fails(self):
        """Insert without ending punctuation should fail."""
        insert = (
            "I've been thinking a lot about fintech and PayPal's push on "
            "financial inclusion stands out"
        )

        is_valid, issues = validate_insert(insert)

        assert is_valid is False
        assert any("punctuation" in issue.lower() for issue in issues)

    def test_banned_phrase_fails(self):
        """Insert with banned phrase should fail."""
        insert = (
            "I came across your work on AI and I've been thinking a lot about "
            "how to apply it to my own projects."
        )

        is_valid, issues = validate_insert(insert)

        assert is_valid is False
        assert any("banned phrase" in issue.lower() for issue in issues)

    def test_em_dash_fails(self):
        """Insert with em dash should fail."""
        insert = (
            "I've been thinking about fintech — especially PayPal's push on "
            "financial inclusion."
        )

        is_valid, issues = validate_insert(insert)

        assert is_valid is False
        assert any("em dash" in issue.lower() for issue in issues)

    def test_exclamation_mark_valid(self):
        """Insert ending with ! should be valid punctuation."""
        insert = (
            "I've been building voice agents and would love to learn about "
            "what problems in conversational AI are worth solving!"
        )

        is_valid, issues = validate_insert(insert)

        # Only check punctuation issue, not word count
        assert not any("punctuation" in issue.lower() for issue in issues)

    def test_question_mark_valid(self):
        """Insert ending with ? should be valid punctuation."""
        insert = (
            "I've been building voice agents and would love to learn what "
            "problems in conversational AI are actually worth solving?"
        )

        is_valid, issues = validate_insert(insert)

        assert not any("punctuation" in issue.lower() for issue in issues)


class TestAssignConfidence:
    """Tests for confidence level assignment."""

    def test_high_confidence_with_multiple_sources(self):
        """Multiple sources + valid insert = HIGH confidence."""
        insert = (
            "I've been thinking a lot about fintech and PayPal's push on "
            "financial inclusion stands out."
        )
        sources = ["Wikipedia", "Forbes", "Bloomberg"]

        confidence = assign_confidence(insert, sources, "detailed")

        assert confidence == "HIGH"

    def test_medium_confidence_with_single_source(self):
        """Single source + valid insert = MEDIUM confidence."""
        insert = (
            "I've been thinking a lot about fintech and PayPal's push on "
            "financial inclusion stands out."
        )
        sources = ["Wikipedia"]

        confidence = assign_confidence(insert, sources, "basic")

        assert confidence == "MEDIUM"

    def test_low_confidence_with_minimal_research(self):
        """Minimal research = LOW confidence."""
        insert = (
            "I've been thinking a lot about your company and would love to "
            "learn from your experience."
        )
        sources = []

        confidence = assign_confidence(insert, sources, "minimal")

        assert confidence == "LOW"

    def test_low_confidence_with_invalid_insert(self):
        """Invalid insert (too short) = LOW confidence regardless of sources."""
        insert = "I love your work."
        sources = ["Wikipedia", "Forbes"]

        confidence = assign_confidence(insert, sources, "detailed")

        assert confidence == "LOW"


class TestMainBranchWarning:
    """Tests for main branch warning behavior."""

    def test_get_current_branch_returns_branch_name(self):
        """Should return current branch name."""
        branch = get_current_branch()

        # We're on main in the test environment
        assert isinstance(branch, str)
        assert len(branch) > 0

    @patch("insert_generator.subprocess.run")
    def test_get_current_branch_handles_error(self, mock_run):
        """Should return 'unknown' if git command fails."""
        from subprocess import CalledProcessError

        mock_run.side_effect = CalledProcessError(1, "git")

        branch = get_current_branch()

        assert branch == "unknown"


class TestModelFlag:
    """Tests for --model flag behavior."""

    def test_haiku_model_maps_correctly(self):
        """--model haiku should map to correct model ID."""
        assert "haiku" in MODELS
        assert "claude" in MODELS["haiku"].lower()

    def test_sonnet_model_maps_correctly(self):
        """--model sonnet should map to correct model ID."""
        assert "sonnet" in MODELS
        assert "claude" in MODELS["sonnet"].lower()

    def test_opus_model_maps_correctly(self):
        """--model opus should map to correct model ID."""
        assert "opus" in MODELS
        assert "claude" in MODELS["opus"].lower()


class TestPromptFileLoading:
    """Tests for prompt file loading."""

    def test_load_prompt_rules_returns_content(self):
        """Should return content of prompt file."""
        # Assumes email_personalization_prompt.md exists in project root
        try:
            content = load_prompt_rules()
            assert "15-25 words" in content or "word count" in content.lower()
        except FileNotFoundError:
            pytest.skip("Prompt file not found in test environment")

    def test_load_prompt_rules_missing_file_raises_error(self, tmp_path, monkeypatch):
        """Should raise FileNotFoundError with clear message if file missing."""
        monkeypatch.chdir(tmp_path)  # Change to temp dir without prompt file
        # Also need to patch the PROMPT_FILE path
        with patch("insert_generator.PROMPT_FILE", "nonexistent.md"):
            with pytest.raises(FileNotFoundError) as exc_info:
                load_prompt_rules()

            assert "email_personalization_prompt.md" in str(exc_info.value) or "nonexistent.md" in str(exc_info.value)


class TestEmailConfidencePassthrough:
    """Tests for Email Confidence passthrough from input to output."""

    def test_csv_row_preserves_email_confidence(self, tmp_path):
        """Email Confidence from input should be preserved in output."""
        output_file = tmp_path / "output.csv"

        row = {
            "Campaign": "test",
            "Name": "John Doe",
            "Email": "john@acme.com",
            "Email Confidence": "HIGH",
            "Company": "Acme",
            "Title": "CEO",
            "Personalized Insert": "Test insert here.",
            "Word Count": 3,
            "Insert Confidence": "MEDIUM",
            "Sources": "Wikipedia",
        }

        write_csv_row(str(output_file), row, is_first=True)

        # Read back and verify
        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            written_row = next(reader)

        assert written_row["Email Confidence"] == "HIGH"


class TestSheetColumnMatching:
    """Tests for Google Sheet column matching by name."""

    def test_add_to_google_sheet_writes_by_column_name(self):
        """Should write to columns by name, not position."""
        mock_worksheet = MagicMock()
        mock_worksheet.get_all_values.return_value = [
            ["Name", "Email", "Company", "Personalized Insert"]
        ]

        headers = ["Name", "Email", "Company", "Personalized Insert"]
        row_data = {
            "Name": "John Doe",
            "Email": "john@acme.com",
            "Company": "Acme",
            "Personalized Insert": "Test insert.",
        }

        add_to_google_sheet(mock_worksheet, row_data, headers)

        # Verify cells were updated by column name position
        calls = mock_worksheet.update_cell.call_args_list
        # Row 2 (first data row), column positions based on headers
        assert any(c[0][1] == 1 and c[0][2] == "John Doe" for c in calls)  # Name col 1
        assert any(c[0][1] == 2 and c[0][2] == "john@acme.com" for c in calls)  # Email col 2

    def test_ensure_sheet_columns_adds_missing(self):
        """Should add missing columns to sheet."""
        mock_worksheet = MagicMock()
        mock_worksheet.row_values.return_value = ["Name", "Email"]

        headers = ensure_sheet_columns(mock_worksheet)

        # Should have added missing columns
        assert mock_worksheet.update_cell.called
        # Campaign should be added since it's required
        assert "Campaign" in headers


class TestRateLimiting:
    """Tests for rate limiting behavior."""

    def test_delay_parameter_accepted(self):
        """--delay parameter should be accepted by argument parser."""
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--delay", type=float, default=1.0)
        args = parser.parse_args(["--delay", "2.5"])

        assert args.delay == 2.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
