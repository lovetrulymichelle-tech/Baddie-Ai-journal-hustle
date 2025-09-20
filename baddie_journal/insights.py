"""
Insights and analytics module for Baddie AI Journal Hustle.

This module provides the InsightsHelper class for analyzing journal entries
and generating insights about patterns, moods, and productivity over time.
"""

from datetime import datetime, UTC, timedelta
from typing import Dict, List, Tuple, Optional
from collections import Counter
import pandas as pd

from .models import InsightData, JournalEntry


class InsightsHelper:
    """
    Helper class for generating insights from journal entries.
    
    This class provides methods to analyze journal data and generate
    meaningful insights about writing patterns, moods, and trends.
    """
    
    def __init__(self, insight_data: InsightData):
        """
        Initialize the InsightsHelper with journal data.
        
        Args:
            insight_data: InsightData object containing journal entries
        """
        self.data = insight_data
    
    def calculate_streak(self) -> int:
        """
        Calculate the current streak of consecutive days with journal entries.
        
        Returns:
            Number of consecutive days with entries (counting backwards from today)
        """
        if not self.data.entries:
            return 0
        
        # Get entries sorted by date (most recent first)
        entries_by_date = {}
        for entry in self.data.entries:
            date_key = entry.timestamp.date()
            if date_key not in entries_by_date:
                entries_by_date[date_key] = []
            entries_by_date[date_key].append(entry)
        
        # Calculate streak from today backwards
        current_date = datetime.now(UTC).date()
        streak = 0
        
        while current_date in entries_by_date:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak
    
    def get_daily_counts(self, days: int = 30) -> Dict[str, int]:
        """
        Get daily entry counts for the last N days.
        
        Args:
            days: Number of days to look back (default: 30)
            
        Returns:
            Dictionary mapping date strings to entry counts
        """
        end_date = datetime.now(UTC)
        start_date = end_date - timedelta(days=days)
        
        # Get entries in the date range
        relevant_entries = self.data.get_entries_in_range(start_date, end_date)
        
        # Count entries by date
        daily_counts = {}
        for entry in relevant_entries:
            date_key = entry.timestamp.strftime('%Y-%m-%d')
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        return daily_counts
    
    def get_mood_breakdown(self) -> Dict[str, int]:
        """
        Get the distribution of moods across all entries.
        
        Returns:
            Dictionary mapping mood names to counts
        """
        mood_counts = Counter(entry.mood for entry in self.data.entries)
        return dict(mood_counts)
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """
        Get the distribution of categories across all entries.
        
        Returns:
            Dictionary mapping category names to counts
        """
        category_counts = Counter(entry.category for entry in self.data.entries)
        return dict(category_counts)
    
    def get_top_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get the most frequently used tags.
        
        Args:
            limit: Maximum number of tags to return (default: 10)
            
        Returns:
            List of tuples (tag, count) sorted by frequency
        """
        all_tags = self.data.get_all_tags()
        tag_counts = Counter(all_tags)
        return tag_counts.most_common(limit)
    
    def get_writing_frequency(self, days: int = 30) -> float:
        """
        Calculate average writing frequency over the last N days.
        
        Args:
            days: Number of days to calculate over (default: 30)
            
        Returns:
            Average entries per day
        """
        daily_counts = self.get_daily_counts(days)
        total_entries = sum(daily_counts.values())
        return total_entries / days if days > 0 else 0.0
    
    def get_mood_trends(self, days: int = 30) -> Dict[str, List[Tuple[str, int]]]:
        """
        Get mood trends over the last N days.
        
        Args:
            days: Number of days to analyze (default: 30)
            
        Returns:
            Dictionary mapping mood names to list of (date, count) tuples
        """
        end_date = datetime.now(UTC)
        start_date = end_date - timedelta(days=days)
        relevant_entries = self.data.get_entries_in_range(start_date, end_date)
        
        # Group by mood and date
        mood_trends = {}
        for entry in relevant_entries:
            mood = entry.mood
            date_key = entry.timestamp.strftime('%Y-%m-%d')
            
            if mood not in mood_trends:
                mood_trends[mood] = {}
            
            if date_key not in mood_trends[mood]:
                mood_trends[mood][date_key] = 0
            
            mood_trends[mood][date_key] += 1
        
        # Convert to sorted lists
        result = {}
        for mood, date_counts in mood_trends.items():
            sorted_dates = sorted(date_counts.items())
            result[mood] = sorted_dates
        
        return result
    
    def get_total_metrics(self) -> Dict[str, any]:
        """
        Get overall metrics about the journal entries.
        
        Returns:
            Dictionary containing various metrics
        """
        return {
            'total_entries': self.data.total_entries(),
            'unique_moods': len(self.data.get_unique_moods()),
            'unique_categories': len(self.data.get_unique_categories()),
            'unique_tags': len(self.data.get_unique_tags()),
            'total_tags': len(self.data.get_all_tags()),
            'current_streak': self.calculate_streak(),
            'average_frequency_30_days': self.get_writing_frequency(30),
            'date_range': {
                'earliest': min(entry.timestamp for entry in self.data.entries).isoformat() if self.data.entries else None,
                'latest': max(entry.timestamp for entry in self.data.entries).isoformat() if self.data.entries else None
            }
        }
    
    def export_to_csv(self, filename: str = None) -> str:
        """
        Export insights to CSV format.
        
        Args:
            filename: Optional filename for the CSV file
            
        Returns:
            Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
            filename = f"journal_insights_{timestamp}.csv"
        
        # Convert entries to DataFrame
        entries_data = []
        for entry in self.data.entries:
            entries_data.append({
                'id': entry.id,
                'content': entry.content,
                'mood': entry.mood,
                'category': entry.category,
                'tags': ', '.join(entry.tags),
                'timestamp': entry.timestamp.isoformat(),
                'date': entry.timestamp.strftime('%Y-%m-%d'),
                'hour': entry.timestamp.hour
            })
        
        df = pd.DataFrame(entries_data)
        df.to_csv(filename, index=False)
        
        return filename
    
    def generate_summary_report(self) -> str:
        """
        Generate a text summary report of insights.
        
        Returns:
            String containing a formatted summary report
        """
        metrics = self.get_total_metrics()
        mood_breakdown = self.get_mood_breakdown()
        top_tags = self.get_top_tags(5)
        
        report = []
        report.append("=== Baddie AI Journal Insights Report ===\n")
        
        # Basic metrics
        report.append(f"Total Entries: {metrics['total_entries']}")
        report.append(f"Current Streak: {metrics['current_streak']} days")
        report.append(f"Average Frequency (30 days): {metrics['average_frequency_30_days']:.1f} entries/day")
        report.append(f"Unique Moods: {metrics['unique_moods']}")
        report.append(f"Unique Categories: {metrics['unique_categories']}")
        report.append(f"Unique Tags: {metrics['unique_tags']}")
        report.append("")
        
        # Mood breakdown
        if mood_breakdown:
            report.append("Mood Distribution:")
            for mood, count in sorted(mood_breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / metrics['total_entries']) * 100
                report.append(f"  {mood}: {count} entries ({percentage:.1f}%)")
            report.append("")
        
        # Top tags
        if top_tags:
            report.append("Top Tags:")
            for tag, count in top_tags:
                report.append(f"  #{tag}: {count} times")
            report.append("")
        
        # Date range
        if metrics['date_range']['earliest']:
            report.append(f"Date Range: {metrics['date_range']['earliest'][:10]} to {metrics['date_range']['latest'][:10]}")
        
        return "\n".join(report)