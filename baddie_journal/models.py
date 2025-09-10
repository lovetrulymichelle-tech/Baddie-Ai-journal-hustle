"""
Core models for the Baddie AI Journal application.
"""
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class JournalEntryDB(Base):
    """SQLAlchemy model for journal entries."""
    
    __tablename__ = 'journal_entries'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    mood = Column(String(50))
    category = Column(String(50))
    tags = Column(JSON)  # Store tags as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@dataclass
class JournalEntry:
    """Data class for journal entries used in insights calculations."""
    
    id: int
    content: str
    mood: str
    category: str
    tags: List[str]
    created_at: datetime
    
    def __post_init__(self):
        """Ensure created_at is UTC."""
        if self.created_at.tzinfo is not None:
            self.created_at = self.created_at.utctimetuple()
            self.created_at = datetime(*self.created_at[:6])


@dataclass
class InsightData:
    """Container for journal entries used in insights analysis."""
    
    entries: List[JournalEntry]
    
    def __post_init__(self):
        """Sort entries by creation date."""
        self.entries.sort(key=lambda x: x.created_at)
    
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> 'InsightData':
        """Filter entries by date range."""
        filtered = [
            entry for entry in self.entries 
            if start_date <= entry.created_at <= end_date
        ]
        return InsightData(filtered)
    
    def filter_by_mood(self, mood: str) -> 'InsightData':
        """Filter entries by mood."""
        filtered = [entry for entry in self.entries if entry.mood == mood]
        return InsightData(filtered)
    
    def filter_by_category(self, category: str) -> 'InsightData':
        """Filter entries by category."""
        filtered = [entry for entry in self.entries if entry.category == category]
        return InsightData(filtered)

    def get_entries_by_date_range(self, start_date: datetime, end_date: datetime) -> List[JournalEntry]:
        """Get entries within a specific date range."""
        return [entry for entry in self.entries 
                if start_date <= entry.created_at <= end_date]
    
    def get_all_entries(self) -> List[JournalEntry]:
        """Get all journal entries."""
        return self.entries


# Database setup functions
def create_database_engine(database_url: str = "sqlite:///journal.db"):
    """Create database engine."""
    return create_engine(database_url)


def create_tables(engine):
    """Create all database tables."""
    Base.metadata.create_all(engine)


def get_session_maker(engine):
    """Get SQLAlchemy session maker."""
    return sessionmaker(bind=engine)