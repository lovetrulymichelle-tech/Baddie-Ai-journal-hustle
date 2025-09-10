"""Test configuration and fixtures."""

import pytest
from datetime import datetime, timedelta
from baddie_journal.models import JournalEntry, InsightData


@pytest.fixture
def sample_entries():
    """Create sample journal entries for testing."""
    return [
        JournalEntry(
            id=1,
            content="Great day at work!",
            mood="happy",
            category="work",
            tags=["productivity", "achievement"],
            created_at=datetime(2023, 1, 1, 12, 0, 0)
        ),
        JournalEntry(
            id=2,
            content="Feeling stressed about deadlines.",
            mood="anxious",
            category="work",
            tags=["stress", "deadlines"],
            created_at=datetime(2023, 1, 2, 14, 0, 0)
        ),
        JournalEntry(
            id=3,
            content="Had fun with friends!",
            mood="happy",
            category="social",
            tags=["friends", "fun"],
            created_at=datetime(2023, 1, 3, 18, 0, 0)
        ),
        JournalEntry(
            id=4,
            content="Productive morning routine.",
            mood="focused",
            category="personal",
            tags=["productivity", "morning"],
            created_at=datetime(2023, 1, 4, 8, 0, 0)
        )
    ]


@pytest.fixture
def insight_data(sample_entries):
    """Create InsightData instance with sample entries."""
    return InsightData(sample_entries)