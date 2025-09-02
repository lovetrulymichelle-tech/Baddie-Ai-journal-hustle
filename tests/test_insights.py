"""Tests for the insights module."""

import pytest
from datetime import datetime, timedelta
from baddie_journal.insights import InsightsHelper, create_sample_data
from baddie_journal.models import JournalEntry, InsightData


class TestInsightsHelper:
    """Test cases for InsightsHelper class."""
    
    def test_insights_helper_creation(self, insight_data):
        """Test creating InsightsHelper instance."""
        helper = InsightsHelper(insight_data)
        assert helper.data == insight_data
        assert helper.entries == insight_data.entries
    
    def test_calculate_streak_with_consecutive_days(self):
        """Test streak calculation with consecutive days."""
        # Create entries for the last 3 consecutive days
        today = datetime.utcnow().date()
        entries = [
            JournalEntry(1, "Day 1", "happy", "test", [], datetime.combine(today - timedelta(days=2), datetime.min.time())),
            JournalEntry(2, "Day 2", "happy", "test", [], datetime.combine(today - timedelta(days=1), datetime.min.time())),
            JournalEntry(3, "Day 3", "happy", "test", [], datetime.combine(today, datetime.min.time()))
        ]
        
        data = InsightData(entries)
        helper = InsightsHelper(data)
        streak = helper.calculate_streak()
        
        assert streak == 3
    
    def test_calculate_streak_no_entries(self):
        """Test streak calculation with no entries."""
        data = InsightData([])
        helper = InsightsHelper(data)
        assert helper.calculate_streak() == 0
    
    def test_get_mood_breakdown(self, insight_data):
        """Test mood breakdown calculation."""
        helper = InsightsHelper(insight_data)
        mood_breakdown = helper.get_mood_breakdown()
        
        expected = {"happy": 2, "anxious": 1, "focused": 1}
        assert mood_breakdown == expected
    
    def test_get_category_breakdown(self, insight_data):
        """Test category breakdown calculation."""
        helper = InsightsHelper(insight_data)
        category_breakdown = helper.get_category_breakdown()
        
        expected = {"work": 2, "social": 1, "personal": 1}
        assert category_breakdown == expected
    
    def test_get_top_tags(self, insight_data):
        """Test top tags calculation."""
        helper = InsightsHelper(insight_data)
        top_tags = helper.get_top_tags(10)
        
        # Check that productivity appears twice
        tag_dict = dict(top_tags)
        assert tag_dict["productivity"] == 2
        
        # Check that all other tags appear once
        expected_tags = {"achievement", "stress", "deadlines", "friends", "fun", "morning"}
        for tag in expected_tags:
            assert tag_dict.get(tag, 0) == 1
    
    def test_get_top_tags_with_limit(self, insight_data):
        """Test top tags with limit."""
        helper = InsightsHelper(insight_data)
        top_tags = helper.get_top_tags(3)
        
        assert len(top_tags) <= 3
        
        # Check that results are sorted by count (descending)
        for i in range(1, len(top_tags)):
            assert top_tags[i-1][1] >= top_tags[i][1]
    
    def test_get_totals_and_metrics(self, insight_data):
        """Test totals and metrics calculation."""
        helper = InsightsHelper(insight_data)
        metrics = helper.get_totals_and_metrics()
        
        assert metrics["total_entries"] == 4
        assert metrics["unique_tags"] == 7  # All unique tags
        assert metrics["unique_categories"] == 3
        assert metrics["unique_moods"] == 3
        assert metrics["total_days_active"] == 4
        assert isinstance(metrics["avg_entries_per_day"], float)
        assert metrics["first_entry_date"] == "2023-01-01"
        assert metrics["last_entry_date"] == "2023-01-04"
    
    def test_get_totals_and_metrics_empty(self):
        """Test totals and metrics with empty data."""
        data = InsightData([])
        helper = InsightsHelper(data)
        metrics = helper.get_totals_and_metrics()
        
        assert metrics["total_entries"] == 0
        assert metrics["unique_tags"] == 0
        assert metrics["unique_categories"] == 0
        assert metrics["unique_moods"] == 0
        assert metrics["avg_entries_per_day"] == 0.0
        assert metrics["first_entry_date"] is None
        assert metrics["last_entry_date"] is None
        assert metrics["total_days_active"] == 0
    
    def test_export_to_csv(self, insight_data):
        """Test CSV export functionality."""
        helper = InsightsHelper(insight_data)
        csv_data = helper.export_to_csv()
        
        lines = csv_data.strip().split('\n')
        assert len(lines) == 5  # Header + 4 entries
        
        # Check header
        header = lines[0]
        assert "Entry ID" in header
        assert "Content" in header
        assert "Mood" in header
        assert "Category" in header
        assert "Tags" in header
        assert "Created At" in header
        
        # Check first data row
        first_row = lines[1]
        assert "1" in first_row
        assert "Great day at work!" in first_row
    
    def test_export_insights_summary_csv(self, insight_data):
        """Test insights summary CSV export."""
        helper = InsightsHelper(insight_data)
        csv_data = helper.export_insights_summary_csv()
        
        assert "Current Streak" in csv_data
        assert "Total Entries" in csv_data
        assert "Mood Breakdown" in csv_data
        assert "Category Breakdown" in csv_data
        assert "Top Tags" in csv_data
    
    def test_get_daily_counts(self, insight_data):
        """Test daily counts calculation."""
        helper = InsightsHelper(insight_data)
        daily_counts = helper.get_daily_counts(30)
        
        # Should return dict with ISO date strings as keys
        assert isinstance(daily_counts, dict)
        assert len(daily_counts) == 30
        
        # All values should be integers >= 0
        for count in daily_counts.values():
            assert isinstance(count, int)
            assert count >= 0
    
    def test_get_mood_trends(self, insight_data):
        """Test mood trends calculation."""
        helper = InsightsHelper(insight_data)
        trends = helper.get_mood_trends(30)
        
        assert isinstance(trends, dict)
        # Should include all moods present in data
        assert "happy" in trends
        assert "anxious" in trends
        assert "focused" in trends
        
        # Each trend should be a list of 30 values
        for mood, trend_data in trends.items():
            assert len(trend_data) == 30
            assert all(isinstance(count, int) for count in trend_data)


class TestCreateSampleData:
    """Test cases for create_sample_data function."""
    
    def test_create_sample_data(self):
        """Test sample data creation."""
        sample_data = create_sample_data()
        
        assert isinstance(sample_data, InsightData)
        assert len(sample_data.entries) == 3
        
        # Check that all entries are valid
        for entry in sample_data.entries:
            assert isinstance(entry, JournalEntry)
            assert entry.content
            assert entry.mood
            assert entry.category
            assert isinstance(entry.tags, list)
            assert isinstance(entry.created_at, datetime)