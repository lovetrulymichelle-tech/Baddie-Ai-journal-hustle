"""
Data models for the Baddie Journal app.
"""

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class JournalEntry:
    """Represents a single journal entry."""
    id: int
    content: str
    mood: str
    category: str
    tags: List[str]
    created_at: datetime
    affirmation: Optional[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class InsightData:
    """Container for insights data."""
    entries: List[JournalEntry]
    
    def __post_init__(self):
        if self.entries is None:
            self.entries = []