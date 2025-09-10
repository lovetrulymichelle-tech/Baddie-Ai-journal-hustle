"""Tests for the storage module."""

import pytest
import tempfile
import os
from datetime import datetime
from baddie_journal.models import JournalEntry
from baddie_journal.storage import JsonStorage


class TestJsonStorage:
    """Test cases for JsonStorage class."""
    
    def setup_method(self):
        """Set up test storage with temporary file."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = JsonStorage(self.temp_file.name)
        
        # Create test entries
        self.entry1 = JournalEntry(
            id=1,
            content="Test entry 1",
            mood="happy",
            category="personal",
            tags=["test", "first"],
            created_at=datetime(2024, 1, 1, 12, 0, 0)
        )
        
        self.entry2 = JournalEntry(
            id=2,
            content="Test entry 2",
            mood="focused",
            category="work",
            tags=["productivity"],
            created_at=datetime(2024, 1, 2, 14, 30, 0)
        )
    
    def teardown_method(self):
        """Clean up temporary file."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_and_load_entry(self):
        """Test saving and loading a single entry."""
        # Save entry
        self.storage.save_entry(self.entry1)
        
        # Load and verify
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 1
        
        loaded_entry = entries[0]
        assert loaded_entry.id == self.entry1.id
        assert loaded_entry.content == self.entry1.content
        assert loaded_entry.mood == self.entry1.mood
        assert loaded_entry.category == self.entry1.category
        assert loaded_entry.tags == self.entry1.tags
        assert loaded_entry.created_at == self.entry1.created_at
    
    def test_save_multiple_entries(self):
        """Test saving multiple entries."""
        self.storage.save_entry(self.entry1)
        self.storage.save_entry(self.entry2)
        
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 2
        
        # Entries should be sorted by creation date in InsightData
        entry_ids = [entry.id for entry in entries]
        assert 1 in entry_ids
        assert 2 in entry_ids
    
    def test_update_existing_entry(self):
        """Test updating an existing entry."""
        # Save initial entry
        self.storage.save_entry(self.entry1)
        
        # Create updated version with same ID
        updated_entry = JournalEntry(
            id=1,  # Same ID
            content="Updated content",
            mood="excited",
            category="hobby",
            tags=["updated"],
            created_at=datetime(2024, 1, 1, 15, 0, 0)
        )
        
        # Save updated entry
        self.storage.save_entry(updated_entry)
        
        # Should still have only one entry, but with updated content
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 1
        
        loaded_entry = entries[0]
        assert loaded_entry.content == "Updated content"
        assert loaded_entry.mood == "excited"
        assert loaded_entry.category == "hobby"
    
    def test_get_entry_by_id(self):
        """Test retrieving specific entry by ID."""
        self.storage.save_entry(self.entry1)
        self.storage.save_entry(self.entry2)
        
        # Get existing entry
        entry = self.storage.get_entry_by_id(1)
        assert entry is not None
        assert entry.id == 1
        assert entry.content == "Test entry 1"
        
        # Get non-existing entry
        entry = self.storage.get_entry_by_id(999)
        assert entry is None
    
    def test_delete_entry(self):
        """Test deleting entries."""
        self.storage.save_entry(self.entry1)
        self.storage.save_entry(self.entry2)
        
        # Delete existing entry
        result = self.storage.delete_entry(1)
        assert result is True
        
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 1
        assert entries[0].id == 2
        
        # Try to delete non-existing entry
        result = self.storage.delete_entry(999)
        assert result is False
    
    def test_get_next_id(self):
        """Test getting next available ID."""
        # Empty storage should return 1
        assert self.storage.get_next_id() == 1
        
        # After saving entries, should return max + 1
        self.storage.save_entry(self.entry1)
        assert self.storage.get_next_id() == 2
        
        self.storage.save_entry(self.entry2)
        assert self.storage.get_next_id() == 3
    
    def test_get_insight_data(self):
        """Test getting insight data."""
        self.storage.save_entry(self.entry1)
        self.storage.save_entry(self.entry2)
        
        insight_data = self.storage.get_insight_data()
        assert len(insight_data.entries) == 2
        
        # Should be sorted by date
        assert insight_data.entries[0].created_at <= insight_data.entries[1].created_at
    
    def test_clear_all(self):
        """Test clearing all entries."""
        self.storage.save_entry(self.entry1)
        self.storage.save_entry(self.entry2)
        
        # Verify entries exist
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 2
        
        # Clear all
        self.storage.clear_all()
        
        # Verify all entries are gone
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 0
    
    def test_load_invalid_json_file(self):
        """Test handling of invalid JSON file."""
        # Write invalid JSON to file
        with open(self.temp_file.name, 'w') as f:
            f.write("invalid json content")
        
        # Should return empty list for invalid JSON
        entries = self.storage.load_all_entries()
        assert entries == []
        
        entries_objects = self.storage.load_entries_as_objects()
        assert entries_objects == []
    
    def test_load_entries_with_invalid_data(self):
        """Test loading entries with some invalid data."""
        # Manually create file with mixed valid/invalid entries
        entries_data = [
            {
                "id": 1,
                "content": "Valid entry",
                "mood": "happy",
                "category": "personal",
                "tags": ["test"],
                "created_at": "2024-01-01T12:00:00"
            },
            {
                "id": 2,
                "content": "",  # Invalid - empty content
                "mood": "sad",
                "category": "personal",
                "tags": [],
                "created_at": "2024-01-02T12:00:00"
            },
            {
                "id": 3,
                "content": "Another valid entry",
                "mood": "excited",
                "category": "work",
                "tags": ["productivity"],
                "created_at": "2024-01-03T12:00:00"
            }
        ]
        
        with open(self.temp_file.name, 'w') as f:
            import json
            json.dump(entries_data, f)
        
        # Should skip invalid entry and load valid ones
        entries = self.storage.load_entries_as_objects()
        assert len(entries) == 2  # Only valid entries loaded
        assert entries[0].id == 1
        assert entries[1].id == 3