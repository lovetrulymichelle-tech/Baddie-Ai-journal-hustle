"""
Insights helper for analyzing journal entries.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import Counter
import csv
from io import StringIO

from .models import InsightData, JournalEntry


class InsightsHelper:
    """Helper class for generating insights from journal entries."""
    
    def __init__(self, insight_data: InsightData):
        self.insight_data = insight_data
    
    def calculate_streak(self) -> int:
        """Calculate the current streak of consecutive days with journal entries."""
        entries = sorted(self.insight_data.get_all_entries(), 
                        key=lambda x: x.created_at, reverse=True)
        
        if not entries:
            return 0
        
        # Get dates of entries (without time)
        entry_dates = [entry.created_at.date() for entry in entries]
        unique_dates = sorted(set(entry_dates), reverse=True)
        
        if not unique_dates:
            return 0
        
        # Start from today and count backwards
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        for date in unique_dates:
            if date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif date == current_date:
                continue  # Skip if same date
            else:
                break  # Gap found, streak ends
        
        return streak
    
    def get_daily_counts(self, days: int = 30) -> Dict[str, int]:
        """Get daily entry counts for the last N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        entries = self.insight_data.get_entries_by_date_range(start_date, end_date)
        
        # Count entries by date
        daily_counts = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            daily_counts[date_str] = 0
            current_date += timedelta(days=1)
        
        for entry in entries:
            date_str = entry.created_at.strftime('%Y-%m-%d')
            if date_str in daily_counts:
                daily_counts[date_str] += 1
        
        return daily_counts
    
    def get_mood_breakdown(self) -> Dict[str, int]:
        """Get breakdown of moods across all entries."""
        entries = self.insight_data.get_all_entries()
        moods = [entry.mood for entry in entries]
        return dict(Counter(moods))
    
    def get_category_breakdown(self) -> Dict[str, int]:
        """Get breakdown of categories across all entries."""
        entries = self.insight_data.get_all_entries()
        categories = [entry.category for entry in entries]
        return dict(Counter(categories))
    
    def get_top_tags(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Get the most frequently used tags."""
        entries = self.insight_data.get_all_entries()
        all_tags = []
        
        for entry in entries:
            all_tags.extend(entry.tags)
        
        tag_counts = Counter(all_tags)
        return tag_counts.most_common(limit)
    
    def get_totals_and_metrics(self) -> Dict[str, any]:
        """Get total entries, unique tags/categories, and average frequency."""
        entries = self.insight_data.get_all_entries()
        
        if not entries:
            return {
                'total_entries': 0,
                'unique_tags': 0,
                'unique_categories': 0,
                'unique_moods': 0,
                'average_entries_per_day': 0.0,
                'date_range_days': 0
            }
        
        # Calculate date range
        sorted_entries = sorted(entries, key=lambda x: x.created_at)
        first_entry = sorted_entries[0].created_at
        last_entry = sorted_entries[-1].created_at
        date_range = (last_entry - first_entry).days + 1
        
        # Get unique values
        all_tags = set()
        all_categories = set()
        all_moods = set()
        
        for entry in entries:
            all_tags.update(entry.tags)
            all_categories.add(entry.category)
            all_moods.add(entry.mood)
        
        avg_per_day = len(entries) / max(date_range, 1)
        
        return {
            'total_entries': len(entries),
            'unique_tags': len(all_tags),
            'unique_categories': len(all_categories),
            'unique_moods': len(all_moods),
            'average_entries_per_day': round(avg_per_day, 2),
            'date_range_days': date_range
        }
    
    def export_to_csv(self) -> str:
        """Export insights data to CSV format."""
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(['Metric', 'Value'])
        
        # Basic metrics
        metrics = self.get_totals_and_metrics()
        for key, value in metrics.items():
            writer.writerow([key.replace('_', ' ').title(), value])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Current Streak (days)', self.calculate_streak()])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Mood', 'Count'])
        mood_breakdown = self.get_mood_breakdown()
        for mood, count in mood_breakdown.items():
            writer.writerow([mood, count])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Category', 'Count'])
        category_breakdown = self.get_category_breakdown()
        for category, count in category_breakdown.items():
            writer.writerow([category, count])
        
        writer.writerow([])  # Empty row
        writer.writerow(['Top Tags', 'Count'])
        top_tags = self.get_top_tags(10)
        for tag, count in top_tags:
            writer.writerow([tag, count])
        
        return output.getvalue()