"""Shared pytest fixtures for email_drafter tests."""

import json
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def sample_config():
    """Sample configuration matching outlook_config.json structure."""
    return {
        "subject_line": "Test Subject",
        "availability": {
            "window1": "Tuesday 10am-1pm EST",
            "window2": "Wednesday 1:30-4pm EST",
            "window3": "Friday 9am-3pm EST"
        },
        "template": (
            "Hello {name},\n\n"
            "My name is Max. {insert}\n\n"
            "I have windows:\n"
            "- {window1}\n"
            "- {window2}\n"
            "- {window3}\n\n"
            "Best,\nMax"
        ),
        "google_sheet_id": "test_sheet_id",
        "session_dir": ".playwright_session"
    }


@pytest.fixture
def tmp_config_file(tmp_path, sample_config):
    """Create a temporary config file and return its path."""
    config_path = tmp_path / "outlook_config.json"
    with open(config_path, "w") as f:
        json.dump(sample_config, f, indent=2)
    return config_path


@pytest.fixture
def mock_worksheet():
    """Mock gspread worksheet for testing without API calls."""
    worksheet = MagicMock()

    # Default headers
    worksheet.row_values.return_value = [
        "Name", "Email", "Company", "Email Status",
        "Draft Created", "Sent Date", "Personalized Insert"
    ]

    # Default records (empty)
    worksheet.get_all_records.return_value = []

    return worksheet


@pytest.fixture
def sample_contacts():
    """Sample contact records in various states."""
    return [
        {
            "Name": "John Smith",
            "Email": "john@example.com",
            "Company": "Acme Corp",
            "Email Status": "",
            "Personalized Insert": "I love your work."
        },
        {
            "Name": "Jane Doe",
            "Email": "jane@example.com",
            "Company": "Tech Inc",
            "Email Status": "drafted",
            "Personalized Insert": "Your startup is impressive."
        },
        {
            "Name": "Bob Wilson",
            "Email": "bob@example.com",
            "Company": "Big Co",
            "Email Status": "sent",
            "Personalized Insert": "Great to meet you."
        },
        {
            "Name": "Alice Brown",
            "Email": "",
            "Company": "Small LLC",
            "Email Status": "",
            "Personalized Insert": "Looking forward to chatting."
        },
    ]
