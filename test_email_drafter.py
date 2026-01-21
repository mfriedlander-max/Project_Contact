"""Tests for email_drafter.py - specifically the build_email_body function."""

import pytest
from email_drafter import build_email_body


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
