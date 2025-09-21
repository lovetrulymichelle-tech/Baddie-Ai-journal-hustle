"""
Core data models for Baddie AI Journal Hustle.

This module defines the main data structures used throughout the application:
- JournalEntry: Represents a single journal entry
- InsightData: Container for aggregated journal data for analysis
"""

from dataclasses import dataclass
from datetime import datetime, UTC
from typing import List


@dataclass
class JournalEntry:
    """
    Represents a single journal entry.

    Attributes:
        id: Unique identifier for the entry
        content: The journal entry text content
        mood: The mood associated with the entry (e.g., 'happy', 'sad', 'focused')
        category: Category of the entry (e.g., 'personal', 'work', 'goals')
        tags: List of tags associated with the entry
        timestamp: When the entry was created (stored in UTC)
    """
    id: int
    content: str
    mood: str
    category: str
    tags: List[str]
    timestamp: datetime

    def __post_init__(self):
        """Ensure timestamp is in UTC."""
        if self.timestamp.tzinfo is None:
            # If no timezone info, assume it's already UTC
            self.timestamp = self.timestamp.replace(tzinfo=UTC)
        elif self.timestamp.tzinfo != UTC:
            # Convert to UTC if it's in a different timezone
            self.timestamp = self.timestamp.astimezone(UTC)

    def to_dict(self) -> dict:
        """Convert the entry to a dictionary for serialization."""
        return {
            'id': self.id,
            'content': self.content,
            'mood': self.mood,
            'category': self.category,
            'tags': self.tags,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'JournalEntry':
        """Create a JournalEntry from a dictionary."""
        timestamp = datetime.fromisoformat(data['timestamp'])
        return cls(
            id=data['id'],
            content=data['content'],
            mood=data['mood'],
            category=data['category'],
            tags=data['tags'],
            timestamp=timestamp
        )


@dataclass
class InsightData:
    """
    Container for aggregated journal data used for analysis.

    This class holds a collection of journal entries and provides
    methods for accessing and organizing the data for insights generation.
    """
    entries: List[JournalEntry]

    def __post_init__(self):
        """Sort entries by timestamp after initialization."""
        self.entries.sort(key=lambda e: e.timestamp)

    def get_entries_by_mood(self, mood: str) -> List[JournalEntry]:
        """Get all entries with a specific mood."""
        return [entry for entry in self.entries if entry.mood == mood]

    def get_entries_by_category(self, category: str) -> List[JournalEntry]:
        """Get all entries with a specific category."""
        return [entry for entry in self.entries if entry.category == category]

    def get_entries_with_tag(self, tag: str) -> List[JournalEntry]:
        """Get all entries that contain a specific tag."""
        return [entry for entry in self.entries if tag in entry.tags]

    def get_entries_in_range(self, start_date: datetime, end_date: datetime) -> List[JournalEntry]:
        """Get entries within a specific date range."""
        return [
            entry for entry in self.entries
            if start_date <= entry.timestamp <= end_date
        ]

    def get_unique_moods(self) -> List[str]:
        """Get all unique moods from the entries."""
        return list(set(entry.mood for entry in self.entries))

    def get_unique_categories(self) -> List[str]:
        """Get all unique categories from the entries."""
        return list(set(entry.category for entry in self.entries))

    def get_all_tags(self) -> List[str]:
        """Get all tags from all entries (with duplicates)."""
        all_tags = []
        for entry in self.entries:
            all_tags.extend(entry.tags)
        return all_tags

    def get_unique_tags(self) -> List[str]:
        """Get all unique tags from the entries."""
        return list(set(self.get_all_tags()))

    def total_entries(self) -> int:
        """Get the total number of entries."""
        return len(self.entries)

    def to_dict(self) -> dict:
        """Convert the insight data to a dictionary for serialization."""
        return {
            'entries': [entry.to_dict() for entry in self.entries],
            'total_entries': self.total_entries(),
            'unique_moods': self.get_unique_moods(),
            'unique_categories': self.get_unique_categories(),
            'unique_tags': self.get_unique_tags()
        }
