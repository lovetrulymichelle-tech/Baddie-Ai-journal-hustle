"""Insights and analytics functionality for journal entries."""

import csv
import io
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd

from .models import InsightData, JournalEntry


class InsightsHelper:
    """Helper class for calculating insights and analytics from journal data."""
    
    def __init__(self, insight_data: InsightData):
        """Initialize with insight data."""
        self.data = insight_data
        self.entries = insight_data.entries
    
    def calculate_streak(self) -> int:
        """Calculate current consecutive days streak of journal entries."""
        if not self.entries:
            return 0
        
        # Sort entries by date
        sorted_entries = sorted(self.entries, key=lambda x: x.created_at.date())
        
        # Get unique dates
        dates = list(set(entry.created_at.date() for entry in sorted_entries))
        dates.sort(reverse=True)  # Most recent first
        
        if not dates:
            return 0
        
        # Check if today has an entry, if not start from yesterday
        today = datetime.utcnow().date()
        current_streak = 0
        
        # Start checking from today or the most recent entry date
        check_date = today if today in dates else dates[0]
        
        for i, date in enumerate(dates):
            expected_date = check_date - timedelta(days=i)
            if date == expected_date:
                current_streak += 1
            else:
                break
        
        return current_streak
    
    def get_daily_counts(self, days: int = 30) -> Dict[str, int]:
        """Get daily entry counts for the last N days."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Initialize all dates with 0
        daily_counts = {}
        current_date = start_date
        while current_date <= end_date:
            daily_counts[current_date.isoformat()] = 0
            current_date += timedelta(days=1)
        
        # Count entries for each date
        for entry in self.entries:
            entry_date = entry.created_at.date()
            if start_date <= entry_date <= end_date:
                daily_counts[entry_date.isoformat()] += 1
        
        return daily_counts
    
    def get_mood_breakdown(self) -> Dict[str, int]:
        """Get breakdown of moods across all entries."""
        moods = [entry.mood for entry in self.entries if entry.mood]
        return dict(Counter(moods))
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """Get breakdown of categories across all entries."""
        categories = [entry.category for entry in self.entries if entry.category]
        return dict(Counter(categories))
    
    def get_top_tags(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get top N most used tags."""
        all_tags = []
        for entry in self.entries:
            if entry.tags:
                all_tags.extend(entry.tags)
        
        tag_counts = Counter(all_tags)
        return tag_counts.most_common(limit)
    
    def get_totals_and_metrics(self) -> Dict[str, Any]:
        """Get total counts and key metrics."""
        if not self.entries:
            return {
                "total_entries": 0,
                "unique_tags": 0,
                "unique_categories": 0,
                "unique_moods": 0,
                "avg_entries_per_day": 0.0,
                "first_entry_date": None,
                "last_entry_date": None,
                "total_days_active": 0
            }
        
        # Get unique values
        all_tags = set()
        categories = set()
        moods = set()
        
        for entry in self.entries:
            if entry.tags:
                all_tags.update(entry.tags)
            if entry.category:
                categories.add(entry.category)
            if entry.mood:
                moods.add(entry.mood)
        
        # Date calculations
        dates = [entry.created_at.date() for entry in self.entries]
        unique_dates = set(dates)
        first_date = min(dates)
        last_date = max(dates)
        
        # Calculate average entries per day
        total_days = (last_date - first_date).days + 1
        avg_per_day = len(self.entries) / total_days if total_days > 0 else 0
        
        return {
            "total_entries": len(self.entries),
            "unique_tags": len(all_tags),
            "unique_categories": len(categories),
            "unique_moods": len(moods),
            "avg_entries_per_day": round(avg_per_day, 2),
            "first_entry_date": first_date.isoformat(),
            "last_entry_date": last_date.isoformat(),
            "total_days_active": len(unique_dates)
        }
    
    def get_mood_trends(self, days: int = 30) -> Dict[str, List[int]]:
        """Get mood trends over time."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        # Group entries by date and mood
        mood_by_date = defaultdict(lambda: defaultdict(int))
        
        for entry in self.entries:
            entry_date = entry.created_at.date()
            if start_date <= entry_date <= end_date and entry.mood:
                mood_by_date[entry_date][entry.mood] += 1
        
        # Get all unique moods
        all_moods = set()
        for entry in self.entries:
            if entry.mood:
                all_moods.add(entry.mood)
        
        # Create trend data
        trends = {mood: [] for mood in all_moods}
        
        current_date = start_date
        while current_date <= end_date:
            for mood in all_moods:
                count = mood_by_date[current_date].get(mood, 0)
                trends[mood].append(count)
            current_date += timedelta(days=1)
        
        return trends
    
    def export_to_csv(self) -> str:
        """Export insights data to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(['Entry ID', 'Content', 'Mood', 'Category', 'Tags', 'Created At'])
        
        # Write data
        for entry in self.entries:
            tags_str = ', '.join(entry.tags) if entry.tags else ''
            writer.writerow([
                entry.id,
                entry.content,
                entry.mood or '',
                entry.category or '',
                tags_str,
                entry.created_at.isoformat()
            ])
        
        return output.getvalue()
    
    def export_insights_summary_csv(self) -> str:
        """Export a summary of insights to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Get all insights
        streak = self.calculate_streak()
        mood_breakdown = self.get_mood_breakdown()
        category_breakdown = self.get_category_breakdown()
        top_tags = self.get_top_tags()
        metrics = self.get_totals_and_metrics()
        
        # Write summary
        writer.writerow(['Insight Type', 'Value', 'Count'])
        writer.writerow(['Current Streak', f"{streak} days", ''])
        writer.writerow(['Total Entries', metrics['total_entries'], ''])
        writer.writerow(['Days Active', metrics['total_days_active'], ''])
        writer.writerow(['Avg Entries/Day', metrics['avg_entries_per_day'], ''])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Mood Breakdown', '', ''])
        for mood, count in mood_breakdown.items():
            writer.writerow(['', mood, count])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Category Breakdown', '', ''])
        for category, count in category_breakdown.items():
            writer.writerow(['', category, count])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Top Tags', '', ''])
        for tag, count in top_tags:
            writer.writerow(['', tag, count])
        
        return output.getvalue()


def create_sample_data() -> InsightData:
    """Create sample data for testing and demonstration."""
    sample_entries = [
        JournalEntry(
            id=1,
            content="Had a great day at work! Finished the project early.",
            mood="happy",
            category="work",
            tags=["productivity", "achievement"],
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        JournalEntry(
            id=2,
            content="Feeling a bit stressed about upcoming deadlines.",
            mood="anxious",
            category="work",
            tags=["stress", "deadlines"],
            created_at=datetime.utcnow() - timedelta(days=1)
        ),
        JournalEntry(
            id=3,
            content="Had a wonderful time with friends at the park.",
            mood="happy",
            category="social",
            tags=["friends", "outdoor", "fun"],
            created_at=datetime.utcnow()
        )
    ]
    
    return InsightData(sample_entries)