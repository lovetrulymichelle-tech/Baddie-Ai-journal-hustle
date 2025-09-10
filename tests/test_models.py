"""Tests for the models module."""

import pytest
from datetime import datetime
from baddie_journal.models import JournalEntry, InsightData


class TestJournalEntry:
    """Test cases for JournalEntry model."""
    
    def test_valid_journal_entry(self):
        """Test creating a valid journal entry."""
        entry = JournalEntry(
            id=1,
            content="Great day today!",
            mood="happy",
            category="personal",
            tags=["motivation", "positive"],
            created_at=datetime.utcnow()
        )
        
        assert entry.id == 1
        assert entry.content == "Great day today!"
        assert entry.mood == "happy"
        assert entry.category == "personal"
        assert "motivation" in entry.tags
        
    def test_empty_content_raises_error(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="Journal entry content cannot be empty"):
            JournalEntry(
                id=1,
                content="   ",  # Only whitespace
                mood="happy",
                category="personal",
                tags=[],
                created_at=datetime.utcnow()
            )
    
    def test_empty_mood_raises_error(self):
        """Test that empty mood raises ValueError."""
        with pytest.raises(ValueError, match="Mood cannot be empty"):
            JournalEntry(
                id=1,
                content="Some content",
                mood="",
                category="personal",
                tags=[],
                created_at=datetime.utcnow()
            )
    
    def test_empty_category_raises_error(self):
        """Test that empty category raises ValueError."""
        with pytest.raises(ValueError, match="Category cannot be empty"):
            JournalEntry(
                id=1,
                content="Some content",
                mood="happy",
                category="",
                tags=[],
                created_at=datetime.utcnow()
            )


class TestInsightData:
    """Test cases for InsightData model."""
    
    def test_valid_insight_data(self):
        """Test creating valid insight data."""
        entries = [
            JournalEntry(1, "Day 1", "happy", "personal", ["tag1"], datetime.utcnow()),
            JournalEntry(2, "Day 2", "sad", "work", ["tag2"], datetime.utcnow())
        ]
        
        insight_data = InsightData(entries)
        assert len(insight_data.entries) == 2
    
    def test_entries_are_sorted_by_date(self):
        """Test that entries are sorted by creation date."""
        now = datetime.utcnow()
        
        entries = [
            JournalEntry(2, "Later", "happy", "personal", [], now),
            JournalEntry(1, "Earlier", "sad", "work", [], now.replace(hour=now.hour-1))
        ]
        
        insight_data = InsightData(entries)
        assert insight_data.entries[0].id == 1  # Earlier entry first
        assert insight_data.entries[1].id == 2  # Later entry second
    
    def test_get_entries_by_mood(self):
        """Test filtering entries by mood."""
        entries = [
            JournalEntry(1, "Happy day", "happy", "personal", [], datetime.utcnow()),
            JournalEntry(2, "Sad day", "sad", "personal", [], datetime.utcnow()),
            JournalEntry(3, "Another happy day", "happy", "work", [], datetime.utcnow())
        ]
        
        insight_data = InsightData(entries)
        happy_entries = insight_data.get_entries_by_mood("happy")
        
        assert len(happy_entries) == 2
        assert all(entry.mood == "happy" for entry in happy_entries)
    
    def test_get_entries_by_category(self):
        """Test filtering entries by category."""
        entries = [
            JournalEntry(1, "Work stuff", "focused", "work", [], datetime.utcnow()),
            JournalEntry(2, "Personal stuff", "happy", "personal", [], datetime.utcnow()),
            JournalEntry(3, "More work", "tired", "work", [], datetime.utcnow())
        ]
        
        insight_data = InsightData(entries)
        work_entries = insight_data.get_entries_by_category("work")
        
        assert len(work_entries) == 2
        assert all(entry.category == "work" for entry in work_entries)
    
    def test_get_entries_with_tag(self):
        """Test filtering entries by tag."""
        entries = [
            JournalEntry(1, "Productive", "happy", "work", ["productivity", "focus"], datetime.utcnow()),
            JournalEntry(2, "Exercise", "energetic", "health", ["fitness"], datetime.utcnow()),
            JournalEntry(3, "Work done", "satisfied", "work", ["productivity"], datetime.utcnow())
        ]
        
        insight_data = InsightData(entries)
        productivity_entries = insight_data.get_entries_with_tag("productivity")
        
        assert len(productivity_entries) == 2
        assert all("productivity" in entry.tags for entry in productivity_entries)