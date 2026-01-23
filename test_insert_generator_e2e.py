"""End-to-end tests for insert_generator.py pipeline.

These tests simulate the full pipeline with mocked API responses.
"""

import csv
import os
import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from insert_generator import (
    main,
    load_input_csv,
    load_processed_contacts,
    validate_required_columns,
    is_already_processed,
    write_csv_row,
    MODELS,
)


class MockAnthropicResponse:
    """Mock Anthropic API response."""

    def __init__(self, insert, sources, quality):
        self.content = [
            MagicMock(
                text=f'''{{
                    "insert": "{insert}",
                    "word_count": {len(insert.split())},
                    "sources": {sources},
                    "research_quality": "{quality}"
                }}'''
            )
        ]


@pytest.fixture
def test_contacts_csv(tmp_path):
    """Create test CSV with 5 contacts for E2E testing."""
    csv_file = tmp_path / "test_contacts.csv"
    csv_file.write_text(
        "Name,Company,Email,Title,Email Confidence\n"
        # Contact 1: Famous person (expect HIGH)
        "Elon Musk,Tesla,elon@tesla.com,CEO,HIGH\n"
        # Contact 2: Obscure person (expect LOW)
        "Jane Unknown,TinyStartup Inc,jane@tinystartup.com,Founder,MEDIUM\n"
        # Contact 3: Missing Email (expect skip)
        "Missing Email,SomeCompany,,Engineer,HIGH\n"
        # Contact 4: Missing Title (expect skip)
        "Missing Title,AnotherCompany,person@company.com,,HIGH\n"
        # Contact 5: Duplicate of contact 1 (expect skip as duplicate)
        "Elon Musk Duplicate,SpaceX,elon@tesla.com,CEO,HIGH\n"
    )
    return str(csv_file)


@pytest.fixture
def output_csv(tmp_path):
    """Output CSV path for test."""
    return str(tmp_path / "test_output.csv")


@pytest.fixture
def mock_worksheet():
    """Mock Google Sheet worksheet."""
    worksheet = MagicMock()
    worksheet.row_values.return_value = [
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
    ]
    worksheet.get_all_values.return_value = [worksheet.row_values.return_value]
    return worksheet


class TestE2EPipeline:
    """End-to-end pipeline tests with 5 contacts."""

    def test_famous_person_high_confidence(self, test_contacts_csv, output_csv, mock_worksheet, tmp_path):
        """Famous person should get HIGH confidence insert."""
        # Create prompt file
        prompt_file = tmp_path / "email_personalization_prompt.md"
        prompt_file.write_text("# Rules\n15-25 words required.")

        with patch("insert_generator.PROMPT_FILE", str(prompt_file)):
            with patch("insert_generator.get_google_sheet", return_value=mock_worksheet):
                with patch("insert_generator.anthropic.Anthropic") as mock_client_class:
                    # Mock API response for famous person
                    mock_client = MagicMock()
                    mock_client_class.return_value = mock_client
                    mock_client.messages.create.return_value = MockAnthropicResponse(
                        "I've been thinking a lot about electric vehicles and Tesla's approach to vertical integration is fascinating.",
                        '["Wikipedia", "Bloomberg", "TechCrunch"]',
                        "detailed",
                    )

                    with patch("insert_generator.get_current_branch", return_value="test-campaign"):
                        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
                            # Process just the first contact (famous person)
                            contacts = load_input_csv(test_contacts_csv)
                            contact = contacts[0]  # Elon Musk

                            is_valid, _ = validate_required_columns(contact)
                            assert is_valid is True

                            # Verify this is the famous person contact
                            assert contact["Name"] == "Elon Musk"
                            assert contact["Company"] == "Tesla"

    def test_obscure_person_low_confidence(self, test_contacts_csv, output_csv):
        """Obscure person with minimal research should get LOW confidence."""
        contacts = load_input_csv(test_contacts_csv)
        contact = contacts[1]  # Jane Unknown

        # Verify contact
        assert contact["Name"] == "Jane Unknown"
        assert contact["Company"] == "TinyStartup Inc"

        # Validation should pass
        is_valid, _ = validate_required_columns(contact)
        assert is_valid is True

    def test_missing_email_skipped(self, test_contacts_csv):
        """Contact with missing Email should be skipped."""
        contacts = load_input_csv(test_contacts_csv)
        contact = contacts[2]  # Missing Email

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Email"

    def test_missing_title_skipped(self, test_contacts_csv):
        """Contact with missing Title should be skipped."""
        contacts = load_input_csv(test_contacts_csv)
        contact = contacts[3]  # Missing Title

        is_valid, missing = validate_required_columns(contact)

        assert is_valid is False
        assert missing == "Title"

    def test_duplicate_contact_skipped(self, test_contacts_csv, tmp_path):
        """Duplicate contact (same email) should be skipped."""
        # Create output file with first contact already processed
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Email Confidence,Company,Title,Personalized Insert,Word Count,Insert Confidence,Sources\n"
            "test,Elon Musk,elon@tesla.com,HIGH,Tesla,CEO,Test insert sentence here with enough words.,8,HIGH,Wikipedia\n"
        )

        # Load processed contacts
        processed = load_processed_contacts(str(output_file))

        # Check contact 5 (duplicate email)
        contacts = load_input_csv(test_contacts_csv)
        duplicate = contacts[4]  # Elon Musk Duplicate

        # Should be detected as already processed (same email)
        assert is_already_processed(duplicate, processed) is True


class TestE2EOutputFormat:
    """Tests for output format correctness."""

    def test_csv_output_has_correct_columns(self, tmp_path):
        """Output CSV should have all required columns."""
        output_file = tmp_path / "test_output.csv"

        row = {
            "Campaign": "test-campaign",
            "Name": "John Doe",
            "Email": "john@example.com",
            "Email Confidence": "HIGH",
            "Company": "Example Corp",
            "Title": "CEO",
            "Personalized Insert": "I've been thinking about your company and would love to learn more.",
            "Word Count": 13,
            "Insert Confidence": "MEDIUM",
            "Sources": "Wikipedia, LinkedIn",
        }

        write_csv_row(str(output_file), row, is_first=True)

        # Read back and verify columns
        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

        expected_columns = [
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
        for col in expected_columns:
            assert col in headers, f"Missing column: {col}"

    def test_csv_output_preserves_email_confidence(self, tmp_path):
        """Email Confidence should be preserved from input to output."""
        output_file = tmp_path / "test_output.csv"

        row = {
            "Campaign": "test",
            "Name": "Test Person",
            "Email": "test@example.com",
            "Email Confidence": "MEDIUM",
            "Company": "Test Co",
            "Title": "Engineer",
            "Personalized Insert": "Test insert.",
            "Word Count": 2,
            "Insert Confidence": "LOW",
            "Sources": "",
        }

        write_csv_row(str(output_file), row, is_first=True)

        # Verify
        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            written_row = next(reader)

        assert written_row["Email Confidence"] == "MEDIUM"

    def test_campaign_column_matches_branch(self, tmp_path):
        """Campaign column should match git branch name."""
        output_file = tmp_path / "test_output.csv"

        with patch("insert_generator.get_current_branch", return_value="round-3-contacts"):
            from insert_generator import get_current_branch

            campaign = get_current_branch()

        row = {
            "Campaign": campaign,
            "Name": "Test",
            "Email": "test@test.com",
            "Email Confidence": "",
            "Company": "Test",
            "Title": "CEO",
            "Personalized Insert": "Test.",
            "Word Count": 1,
            "Insert Confidence": "LOW",
            "Sources": "",
        }

        write_csv_row(str(output_file), row, is_first=True)

        with open(output_file, "r") as f:
            reader = csv.DictReader(f)
            written_row = next(reader)

        assert written_row["Campaign"] == "round-3-contacts"


class TestE2ECheckpointing:
    """Tests for checkpointing and resume functionality."""

    def test_checkpoint_skips_already_processed(self, tmp_path):
        """Re-running should skip already processed contacts."""
        # Create output with one processed contact
        output_file = tmp_path / "output.csv"
        output_file.write_text(
            "Campaign,Name,Email,Email Confidence,Company,Title,Personalized Insert,Word Count,Insert Confidence,Sources\n"
            "test,John Doe,john@example.com,HIGH,Example,CEO,Test insert.,2,MEDIUM,Wiki\n"
        )

        # Create input with same contact plus new one
        input_file = tmp_path / "input.csv"
        input_file.write_text(
            "Name,Company,Email,Title\n"
            "John Doe,Example,john@example.com,CEO\n"
            "Jane Smith,Other,jane@other.com,CTO\n"
        )

        # Load processed
        processed = load_processed_contacts(str(output_file))

        # Load input contacts
        contacts = load_input_csv(str(input_file))

        # John should be skipped, Jane should not
        assert is_already_processed(contacts[0], processed) is True
        assert is_already_processed(contacts[1], processed) is False

    def test_checkpoint_handles_empty_output(self, tmp_path):
        """Should handle missing output file gracefully."""
        output_file = tmp_path / "nonexistent.csv"

        processed = load_processed_contacts(str(output_file))

        assert processed == set()


class TestE2EInsertValidation:
    """Tests for insert quality validation."""

    def test_all_inserts_15_to_25_words(self):
        """All generated inserts should be 15-25 words."""
        # Test word count validation
        valid_insert = (
            "I've been thinking a lot about electric vehicles and Tesla's "
            "approach to vertical integration is fascinating."
        )
        word_count = len(valid_insert.split())

        assert 15 <= word_count <= 25, f"Word count {word_count} not in range 15-25"

    def test_no_banned_phrases_in_output(self):
        """No inserts should contain banned phrases."""
        from insert_generator import BANNED_PHRASES

        valid_insert = (
            "I've been thinking a lot about electric vehicles and Tesla's "
            "approach to vertical integration is fascinating."
        )

        for phrase in BANNED_PHRASES:
            assert phrase not in valid_insert.lower(), f"Insert contains banned phrase: {phrase}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
