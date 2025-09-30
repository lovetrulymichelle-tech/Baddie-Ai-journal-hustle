"""
Tests for Baddie AI Journal Hustle Flask application.

These tests verify the web application functionality including:
- Web routes and responses
- Database integration
- Core insights functionality
"""

import pytest
from datetime import datetime, timezone
import os
import tempfile
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402
from database import DatabaseManager  # noqa: E402
from baddie_journal.models import JournalEntry, InsightData  # noqa: E402
from baddie_journal.insights import InsightsHelper  # noqa: E402


@pytest.fixture
def client():
    """Create a test client with in-memory database."""
    # Create temporary database file for testing
    db_fd, db_path = tempfile.mkstemp()

    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-key"

    # Override the database manager with test database
    test_db_url = f"sqlite:///{db_path}"

    with app.test_client() as client:
        with app.app_context():
            # Initialize test database
            global db_manager
            original_db_manager = app.config.get("db_manager")
            db_manager = DatabaseManager(test_db_url)
            app.config["db_manager"] = db_manager

            yield client

            # Cleanup
            db_manager.close()
            os.close(db_fd)
            os.unlink(db_path)
            if original_db_manager:
                app.config["db_manager"] = original_db_manager


def test_home_page(client):
    """Test that home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert (
        b"New Journal Entry" in response.data or b"Baddie AI Journal" in response.data
    )


def test_add_entry_post(client):
    """Test adding a new journal entry via POST."""
    response = client.post(
        "/add_entry",
        data={
            "content": "Test journal entry content",
            "mood": "happy",
            "category": "test",
            "tags": "test,happy",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_entries_page(client):
    """Test that entries page loads."""
    response = client.get("/entries")
    assert response.status_code == 200


def test_insights_page(client):
    """Test that insights page loads."""
    response = client.get("/insights")
    assert response.status_code == 200


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_api_entries(client):
    """Test API entries endpoint."""
    response = client.get("/api/entries")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)  # API returns list of entries directly


def test_insights_helper():
    """Test the InsightsHelper functionality."""
    # Create test entries
    entries = [
        JournalEntry(1, "Happy day!", "happy", "personal", ["joy"], datetime.now(timezone.utc)),
        JournalEntry(
            2, "Work productive", "focused", "work", ["productivity"], datetime.now(timezone.utc)
        ),
        JournalEntry(
            3,
            "Reflection",
            "contemplative",
            "personal",
            ["reflection"],
            datetime.now(timezone.utc),
        ),
    ]

    insight_data = InsightData(entries)
    helper = InsightsHelper(insight_data)

    # Test streak calculation
    streak = helper.calculate_streak()
    assert isinstance(streak, int)
    assert streak >= 0

    # Test mood breakdown
    mood_breakdown = helper.get_mood_breakdown()
    assert isinstance(mood_breakdown, dict)
    assert len(mood_breakdown) <= 3  # At most 3 different moods

    # Test top tags
    top_tags = helper.get_top_tags(5)
    assert isinstance(top_tags, list)

    # Test summary report
    report = helper.generate_summary_report()
    assert isinstance(report, str)
    assert "Total Entries: 3" in report


def test_database_operations():
    """Test database operations directly."""
    # Create temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    test_db_url = f"sqlite:///{db_path}"

    try:
        db_manager = DatabaseManager(test_db_url)

        # Test adding entry
        entry = db_manager.add_entry(
            content="Test content", mood="happy", category="test", tags=["test", "unit"]
        )

        assert entry.content == "Test content"
        assert entry.mood == "happy"

        # Test getting entries
        entries = db_manager.get_all_entries()
        assert len(entries) == 1
        assert entries[0].content == "Test content"

        # Test entry count
        count = db_manager.get_entry_count()
        assert count == 1

        db_manager.close()

    finally:
        os.close(db_fd)
        os.unlink(db_path)
