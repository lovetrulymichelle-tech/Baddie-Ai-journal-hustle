"""Tests for the models module."""

import pytest
from datetime import datetime
from baddie_journal.models import JournalEntry, InsightData


class TestJournalEntry:
    """Test cases for JournalEntry dataclass."""
    
    def test_journal_entry_creation(self):
        """Test creating a journal entry."""
        entry = JournalEntry(
            id=1,
            content="Test content",
            mood="happy",
            category="test",
            tags=["tag1", "tag2"],
            created_at=datetime.utcnow()
        )
        
        assert entry.id == 1
        assert entry.content == "Test content"
        assert entry.mood == "happy"
        assert entry.category == "test"
        assert entry.tags == ["tag1", "tag2"]
        assert isinstance(entry.created_at, datetime)
    
    def test_journal_entry_with_empty_tags(self):
        """Test creating a journal entry with empty tags."""
        entry = JournalEntry(
            id=1,
            content="Test content",
            mood="happy",
            category="test",
            tags=[],
            created_at=datetime.utcnow()
        )
        
        assert entry.tags == []


class TestInsightData:
    """Test cases for InsightData class."""
    
    def test_insight_data_creation(self, sample_entries):
        """Test creating InsightData instance."""
        data = InsightData(sample_entries)
        assert len(data.entries) == 4
        assert all(isinstance(entry, JournalEntry) for entry in data.entries)
    
    def test_entries_sorted_by_date(self, sample_entries):
        """Test that entries are sorted by creation date."""
        # Shuffle entries before creating InsightData
        shuffled = [sample_entries[2], sample_entries[0], sample_entries[3], sample_entries[1]]
        data = InsightData(shuffled)
        
        # Check they are sorted
        for i in range(1, len(data.entries)):
            assert data.entries[i-1].created_at <= data.entries[i].created_at
    
    def test_filter_by_date_range(self, insight_data):
        """Test filtering entries by date range."""
        start_date = datetime(2023, 1, 2)
        end_date = datetime(2023, 1, 3, 23, 59, 59)  # Include end of day
        
        filtered = insight_data.filter_by_date_range(start_date, end_date)
        
        assert len(filtered.entries) == 2
        for entry in filtered.entries:
            assert start_date <= entry.created_at <= end_date
    
    def test_filter_by_mood(self, insight_data):
        """Test filtering entries by mood."""
        happy_entries = insight_data.filter_by_mood("happy")
        
        assert len(happy_entries.entries) == 2
        for entry in happy_entries.entries:
            assert entry.mood == "happy"
    
    def test_filter_by_category(self, insight_data):
        """Test filtering entries by category."""
        work_entries = insight_data.filter_by_category("work")
        
        assert len(work_entries.entries) == 2
        for entry in work_entries.entries:
            assert entry.category == "work"
    
    def test_filter_empty_result(self, insight_data):
        """Test filtering with no matching results."""
        filtered = insight_data.filter_by_mood("nonexistent")
        assert len(filtered.entries) == 0