"""
Data models for the Baddie AI Journal application.

This module defines the core data structures used throughout the application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class JournalEntry:
    """Represents a single journal entry."""
    
    id: int
    content: str
    mood: str
    category: str
    tags: List[str]
    created_at: datetime
    
    def __post_init__(self):
        """Validate the journal entry data."""
        if not self.content.strip():
            raise ValueError("Journal entry content cannot be empty")
        if not self.mood.strip():
            raise ValueError("Mood cannot be empty")
        if not self.category.strip():
            raise ValueError("Category cannot be empty")


@dataclass
class InsightData:
    """Container for journal entries used for generating insights."""
    
    entries: List[JournalEntry]
    
    def __post_init__(self):
        """Validate insight data."""
        if not isinstance(self.entries, list):
            raise TypeError("Entries must be a list")
        
        # Sort entries by creation date for consistent processing
        self.entries.sort(key=lambda x: x.created_at)
    
    def get_entries_in_range(self, start_date: datetime, end_date: datetime) -> List[JournalEntry]:
        """Get entries within a specific date range."""
        return [
            entry for entry in self.entries
            if start_date <= entry.created_at <= end_date
        ]
    
    def get_entries_by_mood(self, mood: str) -> List[JournalEntry]:
        """Get all entries with a specific mood."""
        return [entry for entry in self.entries if entry.mood.lower() == mood.lower()]
    
    def get_entries_by_category(self, category: str) -> List[JournalEntry]:
        """Get all entries with a specific category."""
        return [entry for entry in self.entries if entry.category.lower() == category.lower()]
    
    def get_entries_with_tag(self, tag: str) -> List[JournalEntry]:
        """Get all entries that contain a specific tag."""
        return [
            entry for entry in self.entries
            if any(t.lower() == tag.lower() for t in entry.tags)
        ]