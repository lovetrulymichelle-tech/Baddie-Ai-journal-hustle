"""
Insights helpers for analyzing journal entries and generating statistics.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
from .models import JournalEntry, InsightData


class InsightsHelper:
    """Helper class for generating insights from journal entries."""
    
    def __init__(self, insight_data: InsightData):
        self.entries = insight_data.entries
    
    def calculate_streak(self) -> int:
        """
        Calculate the current writing streak (consecutive days with entries).
        
        Returns:
            int: Number of consecutive days with journal entries, starting from today.
        """
        if not self.entries:
            return 0
        
        # Sort entries by date (most recent first)
        sorted_entries = sorted(self.entries, key=lambda x: x.created_at, reverse=True)
        
        # Get unique dates
        entry_dates = set()
        for entry in sorted_entries:
            entry_dates.add(entry.created_at.date())
        
        # Calculate streak starting from today
        current_date = datetime.now().date()
        streak = 0
        
        while current_date in entry_dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def get_daily_counts(self, days: int = 30) -> Dict[str, int]:
        """
        Get daily entry counts for the last N days.
        
        Args:
            days: Number of days to look back (default: 30)
            
        Returns:
            Dict[str, int]: Dictionary with date strings as keys and entry counts as values.
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days - 1)
        
        daily_counts = defaultdict(int)
        
        # Initialize all dates with 0
        current_date = start_date
        while current_date <= end_date:
            daily_counts[current_date.isoformat()] = 0
            current_date += timedelta(days=1)
        
        # Count entries for each date
        for entry in self.entries:
            entry_date = entry.created_at.date()
            if start_date <= entry_date <= end_date:
                daily_counts[entry_date.isoformat()] += 1
        
        return dict(daily_counts)
    
    def get_mood_breakdown(self) -> Dict[str, int]:
        """
        Get breakdown of moods across all entries.
        
        Returns:
            Dict[str, int]: Dictionary with mood names as keys and counts as values.
        """
        mood_counts = Counter()
        
        for entry in self.entries:
            if entry.mood:
                mood_counts[entry.mood] += 1
        
        return dict(mood_counts)
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """
        Get breakdown of categories across all entries.
        
        Returns:
            Dict[str, int]: Dictionary with category names as keys and counts as values.
        """
        category_counts = Counter()
        
        for entry in self.entries:
            if entry.category:
                category_counts[entry.category] += 1
        
        return dict(category_counts)
    
    def get_top_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get the most frequently used tags.
        
        Args:
            limit: Maximum number of tags to return (default: 10)
            
        Returns:
            List[Tuple[str, int]]: List of (tag, count) tuples sorted by frequency.
        """
        tag_counts = Counter()
        
        for entry in self.entries:
            if entry.tags:
                for tag in entry.tags:
                    tag_counts[tag] += 1
        
        return tag_counts.most_common(limit)
    
    def get_totals(self) -> Dict[str, int]:
        """
        Get total counts for various metrics.
        
        Returns:
            Dict[str, int]: Dictionary with total counts for entries, moods, categories, and tags.
        """
        unique_moods = set()
        unique_categories = set()
        unique_tags = set()
        
        for entry in self.entries:
            if entry.mood:
                unique_moods.add(entry.mood)
            if entry.category:
                unique_categories.add(entry.category)
            if entry.tags:
                unique_tags.update(entry.tags)
        
        return {
            'total_entries': len(self.entries),
            'unique_moods': len(unique_moods),
            'unique_categories': len(unique_categories),
            'unique_tags': len(unique_tags),
        }
    
    def get_writing_frequency(self) -> float:
        """
        Calculate average entries per day over the time period covered by entries.
        
        Returns:
            float: Average entries per day, or 0 if no entries exist.
        """
        if not self.entries:
            return 0.0
        
        sorted_entries = sorted(self.entries, key=lambda x: x.created_at)
        first_entry_date = sorted_entries[0].created_at.date()
        last_entry_date = sorted_entries[-1].created_at.date()
        
        total_days = (last_entry_date - first_entry_date).days + 1
        
        return len(self.entries) / total_days if total_days > 0 else 0.0