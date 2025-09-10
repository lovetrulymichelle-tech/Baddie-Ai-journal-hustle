"""
Storage module for the Baddie AI Journal application.

This module provides data persistence functionality for journal entries.
"""

import json
import os
from datetime import datetime
from typing import List, Optional
from .models import JournalEntry, InsightData


class JsonStorage:
    """Simple JSON file storage for journal entries."""
    
    def __init__(self, file_path: str = "journal_data.json"):
        """Initialize with a file path."""
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the storage file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def save_entry(self, entry: JournalEntry) -> None:
        """Save a journal entry to storage."""
        entries = self.load_all_entries()
        
        # Convert entry to dictionary for JSON serialization
        entry_dict = {
            "id": entry.id,
            "content": entry.content,
            "mood": entry.mood,
            "category": entry.category,
            "tags": entry.tags,
            "created_at": entry.created_at.isoformat()
        }
        
        # Check if entry with this ID already exists, update if so
        for i, existing_entry in enumerate(entries):
            if existing_entry["id"] == entry.id:
                entries[i] = entry_dict
                break
        else:
            entries.append(entry_dict)
        
        # Save back to file
        with open(self.file_path, 'w') as f:
            json.dump(entries, f, indent=2)
    
    def load_all_entries(self) -> List[dict]:
        """Load all entries from storage as dictionaries."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def load_entries_as_objects(self) -> List[JournalEntry]:
        """Load all entries from storage as JournalEntry objects."""
        entries_data = self.load_all_entries()
        entries = []
        
        for entry_dict in entries_data:
            try:
                entry = JournalEntry(
                    id=entry_dict["id"],
                    content=entry_dict["content"],
                    mood=entry_dict["mood"],
                    category=entry_dict["category"],
                    tags=entry_dict["tags"],
                    created_at=datetime.fromisoformat(entry_dict["created_at"])
                )
                entries.append(entry)
            except (KeyError, ValueError) as e:
                print(f"Warning: Skipping invalid entry {entry_dict}: {e}")
                continue
        
        return entries
    
    def get_entry_by_id(self, entry_id: int) -> Optional[JournalEntry]:
        """Get a specific entry by ID."""
        entries = self.load_entries_as_objects()
        for entry in entries:
            if entry.id == entry_id:
                return entry
        return None
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete an entry by ID. Returns True if deleted, False if not found."""
        entries = self.load_all_entries()
        original_length = len(entries)
        
        entries = [entry for entry in entries if entry["id"] != entry_id]
        
        if len(entries) < original_length:
            with open(self.file_path, 'w') as f:
                json.dump(entries, f, indent=2)
            return True
        return False
    
    def get_insight_data(self) -> InsightData:
        """Get all entries as InsightData for analysis."""
        entries = self.load_entries_as_objects()
        return InsightData(entries)
    
    def get_next_id(self) -> int:
        """Get the next available ID for a new entry."""
        entries = self.load_all_entries()
        if not entries:
            return 1
        
        max_id = max(entry["id"] for entry in entries)
        return max_id + 1
    
    def clear_all(self) -> None:
        """Clear all entries from storage."""
        with open(self.file_path, 'w') as f:
            json.dump([], f)