#!/usr/bin/env python3
"""
Database models and setup for Baddie AI Journal Hustle web application.

This module provides SQLAlchemy database models and initialization.
"""

import os
from datetime import datetime, UTC

# Optional SQLAlchemy import for database functionality
try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    print("SQLAlchemy not available. Using in-memory storage.")

if SQLALCHEMY_AVAILABLE:
    Base = declarative_base()

    class JournalEntryDB(Base):
        """SQLAlchemy model for journal entries."""

        __tablename__ = "journal_entries"

        id = Column(Integer, primary_key=True, autoincrement=True)
        content = Column(String, nullable=False)
        mood = Column(String, nullable=False)
        category = Column(String, default="personal")
        tags = Column(JSON, default=lambda: [])
        timestamp = Column(DateTime, default=datetime.now(UTC))

        def to_journal_entry(self):
            """Convert to our domain model JournalEntry."""
            from baddie_journal.models import JournalEntry

            return JournalEntry(
                id=self.id,
                content=self.content,
                mood=self.mood,
                category=self.category,
                tags=self.tags or [],
                timestamp=self.timestamp,
            )

    class DatabaseManager:
        """Manages database connections and operations."""

        def __init__(self, database_url=None):
            if not SQLALCHEMY_AVAILABLE:
                raise ImportError("SQLAlchemy is required for database functionality")

            if database_url is None:
                database_url = os.getenv(
                    "SQLALCHEMY_DATABASE_URI", "sqlite:///journal.db"
                )

            self.engine = create_engine(database_url, echo=False)
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

        def add_entry(self, content, mood, category="personal", tags=None):
            """Add a new journal entry to the database."""
            if tags is None:
                tags = []

            entry = JournalEntryDB(
                content=content,
                mood=mood,
                category=category,
                tags=tags,
                timestamp=datetime.now(UTC),
            )
            self.session.add(entry)
            self.session.commit()
            return entry.to_journal_entry()

        def get_all_entries(self):
            """Get all journal entries from the database."""
            db_entries = (
                self.session.query(JournalEntryDB)
                .order_by(JournalEntryDB.timestamp.desc())
                .all()
            )
            return [entry.to_journal_entry() for entry in db_entries]

        def get_entry_count(self):
            """Get the total number of entries."""
            return self.session.query(JournalEntryDB).count()

        def close(self):
            """Close the database session."""
            self.session.close()

else:
    # Fallback when SQLAlchemy is not available
    class DatabaseManager:
        """Fallback database manager using in-memory storage."""

        def __init__(self, database_url=None):
            print("Using in-memory storage (SQLAlchemy not available)")
            self.entries = []
            self.next_id = 1

        def add_entry(self, content, mood, category="personal", tags=None):
            """Add a new journal entry to memory."""
            from baddie_journal.models import JournalEntry

            if tags is None:
                tags = []

            entry = JournalEntry(
                id=self.next_id,
                content=content,
                mood=mood,
                category=category,
                tags=tags,
                timestamp=datetime.now(UTC),
            )
            self.entries.append(entry)
            self.next_id += 1
            return entry

        def get_all_entries(self):
            """Get all journal entries from memory."""
            return sorted(self.entries, key=lambda x: x.timestamp, reverse=True)

        def get_entry_count(self):
            """Get the total number of entries."""
            return len(self.entries)

        def close(self):
            """No-op for in-memory storage."""
            pass
