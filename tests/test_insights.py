"""Tests for the insights module."""

import pytest
import tempfile
import os
import csv
from datetime import datetime, timedelta
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper


class TestInsightsHelper:
    """Test cases for InsightsHelper class."""
    
    def setup_method(self):
        """Set up test data for each test."""
        now = datetime.utcnow()
        
        # Create test entries with various dates
        self.entries = [
            JournalEntry(1, "Today's entry", "happy", "personal", ["motivation"], now),
            JournalEntry(2, "Yesterday's entry", "content", "work", ["productivity"], now - timedelta(days=1)),
            JournalEntry(3, "Two days ago", "tired", "personal", ["rest"], now - timedelta(days=2)),
            JournalEntry(4, "A week ago", "excited", "hobby", ["creativity", "fun"], now - timedelta(days=7)),
            JournalEntry(5, "Another today", "grateful", "personal", ["gratitude"], now),
        ]
        
        self.insight_data = InsightData(self.entries)
        self.helper = InsightsHelper(self.insight_data)
    
    def test_calculate_streak_with_consecutive_days(self):
        """Test streak calculation with consecutive days."""
        streak = self.helper.calculate_streak()
        # Should have 3 consecutive days (today, yesterday, day before)
        assert streak == 3
    
    def test_calculate_streak_empty_entries(self):
        """Test streak calculation with no entries."""
        empty_helper = InsightsHelper(InsightData([]))
        assert empty_helper.calculate_streak() == 0
    
    def test_get_daily_counts(self):
        """Test daily entry counts."""
        daily_counts = self.helper.get_daily_counts(days=30)
        
        # Should have counts for the days we have entries
        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        yesterday_str = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        assert daily_counts.get(today_str, 0) == 2  # Two entries today
        assert daily_counts.get(yesterday_str, 0) == 1  # One entry yesterday
    
    def test_get_mood_breakdown(self):
        """Test mood distribution analysis."""
        mood_breakdown = self.helper.get_mood_breakdown()
        
        # Check that all moods are accounted for
        expected_moods = {"happy": 1, "content": 1, "tired": 1, "excited": 1, "grateful": 1}
        assert mood_breakdown == expected_moods
    
    def test_get_category_breakdown(self):
        """Test category distribution analysis."""
        category_breakdown = self.helper.get_category_breakdown()
        
        # Check category distribution
        assert category_breakdown["personal"] == 3
        assert category_breakdown["work"] == 1
        assert category_breakdown["hobby"] == 1
    
    def test_get_top_tags(self):
        """Test top tags functionality."""
        top_tags = self.helper.get_top_tags(limit=10)  # Increased limit to get all tags
        
        # Should return list of tuples (tag, count)
        assert isinstance(top_tags, list)
        assert all(isinstance(item, tuple) and len(item) == 2 for item in top_tags)
        
        # Convert to dict for easier testing
        tag_dict = dict(top_tags)
        
        # Each tag should appear once in our test data
        expected_tags = {"motivation", "productivity", "rest", "creativity", "fun", "gratitude"}
        for tag in expected_tags:
            assert tag in tag_dict
            assert tag_dict[tag] == 1
    
    def test_get_totals_and_metrics(self):
        """Test totals and metrics calculation."""
        metrics = self.helper.get_totals_and_metrics()
        
        assert metrics["total_entries"] == 5
        assert metrics["unique_tags"] == 6  # All tags are unique in our test data
        assert metrics["unique_categories"] == 3  # personal, work, hobby
        assert metrics["unique_moods"] == 5  # All moods are unique
        assert metrics["date_range_days"] == 8  # 7 days + 1 (from a week ago to today)
        assert isinstance(metrics["average_entries_per_day"], float)
    
    def test_get_totals_and_metrics_empty(self):
        """Test metrics with empty data."""
        empty_helper = InsightsHelper(InsightData([]))
        metrics = empty_helper.get_totals_and_metrics()
        
        assert metrics["total_entries"] == 0
        assert metrics["unique_tags"] == 0
        assert metrics["unique_categories"] == 0
        assert metrics["unique_moods"] == 0
        assert metrics["average_entries_per_day"] == 0.0
        assert metrics["date_range_days"] == 0
    
    def test_export_to_csv(self):
        """Test CSV export functionality."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_filename = f.name
        
        try:
            # Export to CSV
            self.helper.export_to_csv(csv_filename)
            
            # Verify the CSV file was created and contains correct data
            assert os.path.exists(csv_filename)
            
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            # Should have same number of rows as entries
            assert len(rows) == len(self.entries)
            
            # Check that all expected columns are present
            expected_columns = {'id', 'content', 'mood', 'category', 'tags', 'created_at'}
            assert set(rows[0].keys()) == expected_columns
            
            # Check first row data (should be oldest entry due to sorting)
            first_row = rows[0]
            assert first_row['content'] == "A week ago"  # Oldest entry comes first after sorting
            assert first_row['mood'] == "excited"
            assert "creativity" in first_row['tags']
            
        finally:
            # Clean up
            if os.path.exists(csv_filename):
                os.unlink(csv_filename)
    
    def test_generate_full_report(self):
        """Test comprehensive report generation."""
        report = self.helper.generate_full_report()
        
        # Check that all expected sections are present
        expected_sections = {
            "streak", "daily_counts", "mood_breakdown", 
            "category_breakdown", "top_tags", "totals_and_metrics"
        }
        assert set(report.keys()) == expected_sections
        
        # Verify each section has data
        assert isinstance(report["streak"], int)
        assert isinstance(report["daily_counts"], dict)
        assert isinstance(report["mood_breakdown"], dict)
        assert isinstance(report["category_breakdown"], dict)
        assert isinstance(report["top_tags"], list)
        assert isinstance(report["totals_and_metrics"], dict)
    
    def test_case_insensitive_operations(self):
        """Test that mood and category operations are case-insensitive."""
        # Create entries with mixed case
        entries = [
            JournalEntry(1, "Test", "Happy", "PERSONAL", ["Tag1"], datetime.utcnow()),
            JournalEntry(2, "Test", "HAPPY", "personal", ["tag1"], datetime.utcnow()),
        ]
        
        insight_data = InsightData(entries)
        helper = InsightsHelper(insight_data)
        
        # Test mood breakdown (should be case-insensitive)
        mood_breakdown = helper.get_mood_breakdown()
        assert mood_breakdown["happy"] == 2  # Both "Happy" and "HAPPY" counted as "happy"
        
        # Test category breakdown
        category_breakdown = helper.get_category_breakdown()
        assert category_breakdown["personal"] == 2  # Both "PERSONAL" and "personal" counted