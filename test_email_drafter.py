"""Tests for email_drafter.py - comprehensive test suite."""

import json
import pytest
from unittest.mock import MagicMock, patch
from email_drafter import (
    build_email_body,
    load_config,
    save_config,
    get_contacts_to_draft,
    update_draft_status,
    setup_sheet_columns,
)


class TestBuildEmailBody:
    """Tests for the build_email_body function."""

    @pytest.fixture
    def config(self):
        """Sample config with template containing all placeholders."""
        return {
            "template": (
                "Hello {name},\n\n"
                "Intro text. {insert}\n\n"
                "I have windows:\n"
                "- {window1}\n"
                "- {window2}\n"
                "- {window3}\n\n"
                "Best,\nMax"
            )
        }

    @pytest.fixture
    def contact(self):
        """Sample contact with all fields."""
        return {
            "name": "John Smith",
            "email": "john@example.com",
            "company": "Acme Corp",
            "insert": "I love your work on AI.",
        }

    def test_windows_inserted_correctly(self, config, contact):
        """Windows should be inserted into the template."""
        windows = ["Tuesday 2-4pm EST", "Thursday 10am-12pm EST", "Friday 3-5pm EST"]

        body = build_email_body(config, contact, windows)

        assert "Tuesday 2-4pm EST" in body
        assert "Thursday 10am-12pm EST" in body
        assert "Friday 3-5pm EST" in body

    def test_default_windows_when_none_provided(self, config, contact):
        """Default placeholder windows should be used when windows=None."""
        body = build_email_body(config, contact, windows=None)

        assert "[Time slot 1]" in body
        assert "[Time slot 2]" in body
        assert "[Time slot 3]" in body

    def test_first_name_extracted(self, config, contact):
        """Only first name should be used in greeting."""
        body = build_email_body(config, contact)

        assert "Hello John," in body
        assert "Hello John Smith," not in body

    def test_single_name_works(self, config):
        """Single-word name should work."""
        contact = {"name": "Madonna", "insert": "Test insert."}

        body = build_email_body(config, contact)

        assert "Hello Madonna," in body

    def test_empty_name_uses_fallback(self, config):
        """Empty name should fall back to 'there'."""
        contact = {"name": "", "insert": "Test insert."}

        body = build_email_body(config, contact)

        assert "Hello there," in body

    def test_missing_name_uses_fallback(self, config):
        """Missing name key should fall back to 'there'."""
        contact = {"insert": "Test insert."}

        body = build_email_body(config, contact)

        assert "Hello there," in body

    def test_personalized_insert_used(self, config, contact):
        """Personalized insert should be included in body."""
        body = build_email_body(config, contact)

        assert "I love your work on AI." in body

    def test_default_insert_when_empty(self, config):
        """Default insert should be used when insert is empty."""
        contact = {"name": "John Smith", "insert": ""}

        body = build_email_body(config, contact)

        assert "I'd love to learn from your experience." in body

    def test_default_insert_when_missing(self, config):
        """Default insert should be used when insert key is missing."""
        contact = {"name": "John Smith"}

        body = build_email_body(config, contact)

        assert "I'd love to learn from your experience." in body

    def test_all_placeholders_replaced(self, config, contact):
        """No placeholder syntax should remain in output."""
        windows = ["Window 1", "Window 2", "Window 3"]

        body = build_email_body(config, contact, windows)

        assert "{name}" not in body
        assert "{insert}" not in body
        assert "{window1}" not in body
        assert "{window2}" not in body
        assert "{window3}" not in body


class TestBuildEmailBodyWithRealTemplate:
    """Tests using the actual template format from outlook_config.json."""

    @pytest.fixture
    def real_config(self):
        """The actual template from outlook_config.json."""
        return {
            "template": (
                "Hello {name},\n\n"
                "My name is Max Friedlander, I am 20 years old, and a current Freshman at "
                "Middlebury. I am interested in entrepreneurship, ambitious, and curious "
                "about the world. {insert}\n\n"
                "I understand that you're very busy, but if you had 15 minutes to chat "
                "with me, I would love to introduce myself, and learn from you.\n\n"
                "I have a few windows open this week if any work for you:\n"
                "- {window1}\n"
                "- {window2}\n"
                "- {window3}\n\n"
                "Feel free to let me know what works best.\n\n"
                "Best,\nMax"
            )
        }

    def test_complete_email_generation(self, real_config):
        """Full email should be generated correctly with all fields."""
        contact = {
            "name": "Sarah Johnson",
            "email": "sarah@techcorp.com",
            "company": "TechCorp",
            "insert": "I've been building voice agents and would love to learn about your AI work.",
        }
        windows = ["Tuesday 2-4pm EST", "Thursday 10am-12pm EST", "Friday 3-5pm EST"]

        body = build_email_body(real_config, contact, windows)

        # Check greeting
        assert body.startswith("Hello Sarah,")

        # Check insert is placed correctly
        assert "curious about the world. I've been building voice agents" in body

        # Check windows section
        assert "I have a few windows open this week if any work for you:" in body
        assert "- Tuesday 2-4pm EST" in body
        assert "- Thursday 10am-12pm EST" in body
        assert "- Friday 3-5pm EST" in body

        # Check sign-off
        assert body.endswith("Best,\nMax")

    def test_windows_appear_after_busy_paragraph(self, real_config):
        """Windows should appear after the 'busy' paragraph."""
        contact = {"name": "Test Person", "insert": "Test insert."}
        windows = ["Monday 9am", "Tuesday 10am", "Wednesday 11am"]

        body = build_email_body(real_config, contact, windows)

        busy_pos = body.find("I understand that you're very busy")
        windows_pos = body.find("I have a few windows open")
        best_pos = body.find("Best,")

        assert busy_pos < windows_pos < best_pos


class TestConfigPersistence:
    """Tests for load_config and save_config functions."""

    def test_load_config_returns_dict_with_required_keys(self, tmp_path, sample_config):
        """Config should have subject_line, template, google_sheet_id, session_dir."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()

        assert "subject_line" in config
        assert "template" in config
        assert "google_sheet_id" in config
        assert "session_dir" in config

    def test_load_config_includes_availability_section(self, tmp_path, sample_config):
        """Config should have availability with window1, window2, window3."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()

        assert "availability" in config
        assert "window1" in config["availability"]
        assert "window2" in config["availability"]
        assert "window3" in config["availability"]

    def test_save_config_persists_changes(self, tmp_path, sample_config):
        """Saved config should be loadable with same values."""
        config_path = tmp_path / "outlook_config.json"

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            save_config(sample_config)
            loaded = load_config()

        assert loaded["subject_line"] == sample_config["subject_line"]
        assert loaded["availability"] == sample_config["availability"]

    def test_save_config_preserves_template_newlines(self, tmp_path, sample_config):
        """Template with newlines should round-trip correctly."""
        config_path = tmp_path / "outlook_config.json"
        sample_config["template"] = "Line 1\n\nLine 2\n\nLine 3"

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            save_config(sample_config)
            loaded = load_config()

        assert loaded["template"] == "Line 1\n\nLine 2\n\nLine 3"

    def test_load_config_missing_file_raises_error(self, tmp_path):
        """Missing config file should raise FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.json"

        with patch("email_drafter.CONFIG_FILE", str(nonexistent)):
            with pytest.raises(FileNotFoundError):
                load_config()


class TestGetContactsToDraft:
    """Tests for get_contacts_to_draft function."""

    def test_skips_contacts_with_drafted_status(self, mock_worksheet, sample_contacts):
        """Contacts with Email Status = 'drafted' should be skipped."""
        mock_worksheet.get_all_records.return_value = sample_contacts

        contacts = get_contacts_to_draft(mock_worksheet)

        names = [c["name"] for c in contacts]
        assert "Jane Doe" not in names

    def test_skips_contacts_with_sent_status(self, mock_worksheet, sample_contacts):
        """Contacts with Email Status = 'sent' should be skipped."""
        mock_worksheet.get_all_records.return_value = sample_contacts

        contacts = get_contacts_to_draft(mock_worksheet)

        names = [c["name"] for c in contacts]
        assert "Bob Wilson" not in names

    def test_skips_contacts_without_email(self, mock_worksheet, sample_contacts):
        """Contacts with empty Email field should be skipped."""
        mock_worksheet.get_all_records.return_value = sample_contacts

        contacts = get_contacts_to_draft(mock_worksheet)

        names = [c["name"] for c in contacts]
        assert "Alice Brown" not in names

    def test_includes_contacts_with_blank_status(self, mock_worksheet, sample_contacts):
        """Contacts with no Email Status should be included."""
        mock_worksheet.get_all_records.return_value = sample_contacts

        contacts = get_contacts_to_draft(mock_worksheet)

        names = [c["name"] for c in contacts]
        assert "John Smith" in names

    def test_returns_correct_row_numbers(self, mock_worksheet, sample_contacts):
        """Returned contacts should have correct row numbers (2-indexed)."""
        mock_worksheet.get_all_records.return_value = sample_contacts

        contacts = get_contacts_to_draft(mock_worksheet)

        # John Smith is first in records, so row should be 2
        john = next(c for c in contacts if c["name"] == "John Smith")
        assert john["row"] == 2

    def test_extracts_all_contact_fields(self, mock_worksheet, sample_contacts):
        """Should extract name, email, company, insert fields."""
        mock_worksheet.get_all_records.return_value = sample_contacts

        contacts = get_contacts_to_draft(mock_worksheet)

        john = next(c for c in contacts if c["name"] == "John Smith")
        assert john["email"] == "john@example.com"
        assert john["company"] == "Acme Corp"
        assert john["insert"] == "I love your work."

    def test_empty_worksheet_returns_empty_list(self, mock_worksheet):
        """Empty worksheet should return empty list."""
        mock_worksheet.get_all_records.return_value = []

        contacts = get_contacts_to_draft(mock_worksheet)

        assert contacts == []


class TestUpdateDraftStatus:
    """Tests for update_draft_status function."""

    def test_updates_email_status_column(self, mock_worksheet):
        """Should update Email Status to 'drafted'."""
        mock_worksheet.row_values.return_value = [
            "Name", "Email", "Company", "Email Status", "Draft Created"
        ]

        update_draft_status(mock_worksheet, row=2, status="drafted")

        # Email Status is column 4
        mock_worksheet.update_cell.assert_any_call(2, 4, "drafted")

    def test_updates_draft_created_timestamp(self, mock_worksheet):
        """Should set Draft Created to current timestamp."""
        mock_worksheet.row_values.return_value = [
            "Name", "Email", "Company", "Email Status", "Draft Created"
        ]

        update_draft_status(mock_worksheet, row=2, status="drafted")

        # Draft Created is column 5 - verify it was called with a timestamp-like string
        calls = mock_worksheet.update_cell.call_args_list
        timestamp_call = [c for c in calls if c[0][1] == 5]
        assert len(timestamp_call) == 1

    def test_handles_missing_status_column_gracefully(self, mock_worksheet):
        """Missing Email Status column should not raise error."""
        mock_worksheet.row_values.return_value = ["Name", "Email", "Company"]

        # Should not raise
        update_draft_status(mock_worksheet, row=2, status="drafted")

    def test_handles_missing_draft_created_column(self, mock_worksheet):
        """Missing Draft Created column should not raise error."""
        mock_worksheet.row_values.return_value = [
            "Name", "Email", "Company", "Email Status"
        ]

        # Should not raise
        update_draft_status(mock_worksheet, row=2, status="drafted")

    def test_accepts_custom_status_value(self, mock_worksheet):
        """Should accept 'sent' or other status values."""
        mock_worksheet.row_values.return_value = [
            "Name", "Email", "Company", "Email Status", "Draft Created"
        ]

        update_draft_status(mock_worksheet, row=2, status="sent")

        mock_worksheet.update_cell.assert_any_call(2, 4, "sent")


class TestSetupSheetColumns:
    """Tests for setup_sheet_columns function."""

    def test_adds_missing_columns(self, mock_worksheet):
        """Missing required columns should be added."""
        mock_worksheet.row_values.return_value = ["Name", "Email", "Company"]

        setup_sheet_columns(mock_worksheet)

        # Should add Email Status, Subject Line, Draft Created, Sent Date, Personalized Insert
        assert mock_worksheet.update_cell.call_count >= 5

    def test_returns_true_when_columns_added(self, mock_worksheet):
        """Should return True if any columns were added."""
        mock_worksheet.row_values.return_value = ["Name", "Email", "Company"]

        result = setup_sheet_columns(mock_worksheet)

        assert result is True

    def test_returns_false_when_all_exist(self, mock_worksheet):
        """Should return False if all columns already exist."""
        mock_worksheet.row_values.return_value = [
            "Name", "Email", "Company",
            "Email Status", "Subject Line", "Draft Created", "Sent Date", "Personalized Insert"
        ]

        result = setup_sheet_columns(mock_worksheet)

        assert result is False

    def test_does_not_duplicate_existing_columns(self, mock_worksheet):
        """Existing columns should not be added again."""
        mock_worksheet.row_values.return_value = [
            "Name", "Email", "Company", "Email Status", "Personalized Insert"
        ]

        setup_sheet_columns(mock_worksheet)

        # Should only add: Subject Line, Draft Created, Sent Date (3 columns)
        assert mock_worksheet.update_cell.call_count == 3


class TestSetSubjectCommand:
    """Tests for --set-subject CLI command behavior."""

    def test_set_subject_updates_config(self, tmp_path, sample_config):
        """--set-subject should update subject_line in config."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        # Simulate what the CLI command does
        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            config["subject_line"] = "New Test Subject"
            save_config(config)
            reloaded = load_config()

        assert reloaded["subject_line"] == "New Test Subject"

    def test_set_subject_preserves_other_config_fields(self, tmp_path, sample_config):
        """Setting subject should not affect template, availability, etc."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            original_template = config["template"]
            original_availability = config["availability"].copy()

            config["subject_line"] = "Changed Subject"
            save_config(config)
            reloaded = load_config()

        assert reloaded["template"] == original_template
        assert reloaded["availability"] == original_availability

    def test_set_subject_with_special_characters(self, tmp_path, sample_config):
        """Subject with quotes and special chars should persist correctly."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        special_subject = "Subject with 'quotes' and \"double quotes\""

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            config["subject_line"] = special_subject
            save_config(config)
            reloaded = load_config()

        assert reloaded["subject_line"] == special_subject


class TestSetAvailabilityCommand:
    """Tests for --set-availability CLI command behavior."""

    def test_set_availability_saves_all_windows(self, tmp_path, sample_config):
        """All three windows should be saved to config."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        new_windows = {
            "window1": "Monday 9am-12pm EST",
            "window2": "Tuesday 2-5pm EST",
            "window3": "Wednesday 10am-1pm EST"
        }

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            config["availability"] = new_windows
            save_config(config)
            reloaded = load_config()

        assert reloaded["availability"]["window1"] == "Monday 9am-12pm EST"
        assert reloaded["availability"]["window2"] == "Tuesday 2-5pm EST"
        assert reloaded["availability"]["window3"] == "Wednesday 10am-1pm EST"

    def test_availability_flows_to_email_body(self, tmp_path, sample_config):
        """Saved availability should be used by build_email_body."""
        config_path = tmp_path / "outlook_config.json"
        sample_config["availability"] = {
            "window1": "Custom Window 1",
            "window2": "Custom Window 2",
            "window3": "Custom Window 3"
        }
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            windows = [
                config["availability"]["window1"],
                config["availability"]["window2"],
                config["availability"]["window3"]
            ]

        contact = {"name": "Test Person", "insert": "Test insert."}
        body = build_email_body(sample_config, contact, windows)

        assert "Custom Window 1" in body
        assert "Custom Window 2" in body
        assert "Custom Window 3" in body

    def test_availability_preserves_subject_line(self, tmp_path, sample_config):
        """Setting availability should not affect subject line."""
        config_path = tmp_path / "outlook_config.json"
        sample_config["subject_line"] = "Original Subject"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            config["availability"] = {
                "window1": "New Window 1",
                "window2": "New Window 2",
                "window3": "New Window 3"
            }
            save_config(config)
            reloaded = load_config()

        assert reloaded["subject_line"] == "Original Subject"


class TestWorkflowIntegration:
    """End-to-end workflow integration tests."""

    def test_availability_fallback_chain(self, tmp_path, sample_config):
        """CLI args → config → placeholders fallback order."""
        config_path = tmp_path / "outlook_config.json"
        sample_config["availability"] = {
            "window1": "Config Window 1",
            "window2": "Config Window 2",
            "window3": "Config Window 3"
        }
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        contact = {"name": "Test", "insert": "Insert."}

        # Case 1: CLI args provided → use CLI args
        cli_windows = ["CLI 1", "CLI 2", "CLI 3"]
        body = build_email_body(sample_config, contact, cli_windows)
        assert "CLI 1" in body
        assert "Config Window 1" not in body

        # Case 2: No CLI args, config has availability → use config
        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            config = load_config()
            config_windows = [
                config["availability"]["window1"],
                config["availability"]["window2"],
                config["availability"]["window3"]
            ]
        body = build_email_body(sample_config, contact, config_windows)
        assert "Config Window 1" in body

        # Case 3: No CLI args, no config → use placeholders
        body = build_email_body(sample_config, contact, windows=None)
        assert "[Time slot 1]" in body

    def test_full_config_round_trip(self, tmp_path, sample_config):
        """Set subject + availability → create drafts uses correct values."""
        config_path = tmp_path / "outlook_config.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        with patch("email_drafter.CONFIG_FILE", str(config_path)):
            # Step 1: Set subject
            config = load_config()
            config["subject_line"] = "Integration Test Subject"
            save_config(config)

            # Step 2: Set availability
            config = load_config()
            config["availability"] = {
                "window1": "Test Monday",
                "window2": "Test Tuesday",
                "window3": "Test Wednesday"
            }
            save_config(config)

            # Step 3: Load config and verify both are set
            final_config = load_config()

        assert final_config["subject_line"] == "Integration Test Subject"
        assert final_config["availability"]["window1"] == "Test Monday"
        assert final_config["availability"]["window2"] == "Test Tuesday"
        assert final_config["availability"]["window3"] == "Test Wednesday"

        # Step 4: Build email body uses correct windows
        contact = {"name": "Final Test", "insert": "Final insert."}
        windows = [
            final_config["availability"]["window1"],
            final_config["availability"]["window2"],
            final_config["availability"]["window3"]
        ]
        body = build_email_body(final_config, contact, windows)

        assert "Hello Final," in body
        assert "Final insert." in body
        assert "Test Monday" in body
        assert "Test Tuesday" in body
        assert "Test Wednesday" in body

    def test_contact_filtering_with_mixed_statuses(self, mock_worksheet):
        """Verify contact filtering works with various Email Status values."""
        records = [
            {"Name": "Alice", "Email": "alice@test.com", "Company": "A", "Email Status": "", "Personalized Insert": "A insert"},
            {"Name": "Bob", "Email": "bob@test.com", "Company": "B", "Email Status": "drafted", "Personalized Insert": "B insert"},
            {"Name": "Charlie", "Email": "charlie@test.com", "Company": "C", "Email Status": "sent", "Personalized Insert": "C insert"},
            {"Name": "David", "Email": "", "Company": "D", "Email Status": "", "Personalized Insert": "D insert"},
            {"Name": "Eve", "Email": "eve@test.com", "Company": "E", "Email Status": "", "Personalized Insert": "E insert"},
        ]
        mock_worksheet.get_all_records.return_value = records

        contacts = get_contacts_to_draft(mock_worksheet)

        # Only Alice and Eve should be included (have email, no status)
        names = [c["name"] for c in contacts]
        assert len(contacts) == 2
        assert "Alice" in names
        assert "Eve" in names
        assert "Bob" not in names  # drafted
        assert "Charlie" not in names  # sent
        assert "David" not in names  # no email


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
