"""
Insights module for the Baddie AI Journal application.

This module provides analytics functionality to help users track patterns,
moods, and productivity over time based on their journal entries.
"""

import csv
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .models import InsightData, JournalEntry


class InsightsHelper:
    """Helper class for generating insights from journal entries."""
    
    def __init__(self, insight_data: InsightData):
        """Initialize with insight data."""
        self.insight_data = insight_data
    
    def calculate_streak(self) -> int:
        """
        Calculate the current consecutive days streak of journaling.
        
        Returns:
            Number of consecutive days with journal entries ending today.
        """
        if not self.insight_data.entries:
            return 0
        
        # Get today's date (UTC) without time component
        today = datetime.utcnow().date()
        
        # Group entries by date
        entries_by_date = {}
        for entry in self.insight_data.entries:
            entry_date = entry.created_at.date()
            if entry_date not in entries_by_date:
                entries_by_date[entry_date] = []
            entries_by_date[entry_date].append(entry)
        
        # Count consecutive days backward from today
        streak = 0
        current_date = today
        
        while current_date in entries_by_date:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def get_daily_counts(self, days: int = 30) -> Dict[str, int]:
        """
        Get the count of journal entries per day for the last N days.
        
        Args:
            days: Number of days to look back (default: 30)
            
        Returns:
            Dictionary with date strings as keys and entry counts as values.
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get entries in the date range
        relevant_entries = self.insight_data.get_entries_in_range(start_date, end_date)
        
        # Count entries by date
        daily_counts = {}
        for entry in relevant_entries:
            date_str = entry.created_at.strftime("%Y-%m-%d")
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        return daily_counts
    
    def get_mood_breakdown(self) -> Dict[str, int]:
        """
        Get the distribution of moods across all journal entries.
        
        Returns:
            Dictionary with mood names as keys and counts as values.
        """
        moods = [entry.mood.lower() for entry in self.insight_data.entries]
        return dict(Counter(moods))
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """
        Get the distribution of categories across all journal entries.
        
        Returns:
            Dictionary with category names as keys and counts as values.
        """
        categories = [entry.category.lower() for entry in self.insight_data.entries]
        return dict(Counter(categories))
    
    def get_top_tags(self, limit: int = 10) -> List[tuple]:
        """
        Get the most frequently used tags.
        
        Args:
            limit: Maximum number of tags to return
            
        Returns:
            List of tuples (tag, count) sorted by frequency.
        """
        all_tags = []
        for entry in self.insight_data.entries:
            all_tags.extend([tag.lower() for tag in entry.tags])
        
        tag_counter = Counter(all_tags)
        return tag_counter.most_common(limit)
    
    def get_totals_and_metrics(self) -> Dict[str, Any]:
        """
        Get total counts and average metrics.
        
        Returns:
            Dictionary with various metrics and totals.
        """
        entries = self.insight_data.entries
        
        if not entries:
            return {
                "total_entries": 0,
                "unique_tags": 0,
                "unique_categories": 0,
                "unique_moods": 0,
                "average_entries_per_day": 0.0,
                "date_range_days": 0
            }
        
        # Calculate date range
        start_date = min(entry.created_at for entry in entries)
        end_date = max(entry.created_at for entry in entries)
        date_range_days = (end_date - start_date).days + 1
        
        # Count unique items
        all_tags = set()
        all_categories = set()
        all_moods = set()
        
        for entry in entries:
            all_tags.update([tag.lower() for tag in entry.tags])
            all_categories.add(entry.category.lower())
            all_moods.add(entry.mood.lower())
        
        # Calculate average
        avg_entries_per_day = len(entries) / date_range_days if date_range_days > 0 else 0
        
        return {
            "total_entries": len(entries),
            "unique_tags": len(all_tags),
            "unique_categories": len(all_categories),
            "unique_moods": len(all_moods),
            "average_entries_per_day": round(avg_entries_per_day, 2),
            "date_range_days": date_range_days
        }
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export insights data to a CSV file.
        
        Args:
            filename: Path to the CSV file to create
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'content', 'mood', 'category', 'tags', 'created_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for entry in self.insight_data.entries:
                writer.writerow({
                    'id': entry.id,
                    'content': entry.content,
                    'mood': entry.mood,
                    'category': entry.category,
                    'tags': ', '.join(entry.tags),
                    'created_at': entry.created_at.isoformat()
                })
    
    def generate_full_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive insights report.
        
        Returns:
            Dictionary containing all available insights.
        """
        return {
            "streak": self.calculate_streak(),
            "daily_counts": self.get_daily_counts(),
            "mood_breakdown": self.get_mood_breakdown(),
            "category_breakdown": self.get_category_breakdown(),
            "top_tags": self.get_top_tags(),
            "totals_and_metrics": self.get_totals_and_metrics()
        }