"""
Models for the Baddie AI Journal application.
"""
from datetime import datetime
from typing import List, Optional


class JournalEntry:
    """Represents a single journal entry."""
    
    def __init__(self, id: int, content: str, mood: str, category: str, 
                 tags: List[str], created_at: datetime):
        self.id = id
        self.content = content
        self.mood = mood
        self.category = category
        self.tags = tags
        self.created_at = created_at
    
    def __repr__(self):
        return f"JournalEntry(id={self.id}, mood='{self.mood}', category='{self.category}')"


class InsightData:
    """Container for journal entries used for insights analysis."""
    
    def __init__(self, entries: List[JournalEntry]):
        self.entries = entries
    
    def get_entries_by_date_range(self, start_date: datetime, end_date: datetime) -> List[JournalEntry]:
        """Get entries within a specific date range."""
        return [entry for entry in self.entries 
                if start_date <= entry.created_at <= end_date]
    
    def get_all_entries(self) -> List[JournalEntry]:
        """Get all journal entries."""
        return self.entries