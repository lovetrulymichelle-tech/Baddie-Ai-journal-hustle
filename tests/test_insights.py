"""
Unit tests for the insights helpers.
"""

import pytest
from datetime import datetime, timedelta
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper


class TestInsightsHelper:
    """Test suite for the InsightsHelper class."""
    
    def setup_method(self):
        """Set up test data before each test method."""
        self.base_date = datetime(2024, 1, 1, 12, 0, 0)
        
        # Create test entries with various dates, moods, categories, and tags
        self.test_entries = [
            JournalEntry(
                id=1,
                content="First entry",
                mood="happy",
                category="personal",
                tags=["motivation", "goals"],
                created_at=self.base_date
            ),
            JournalEntry(
                id=2,
                content="Second entry",
                mood="excited",
                category="work",
                tags=["productivity", "goals"],
                created_at=self.base_date + timedelta(days=1)
            ),
            JournalEntry(
                id=3,
                content="Third entry",
                mood="content",
                category="personal",
                tags=["reflection", "gratitude"],
                created_at=self.base_date + timedelta(days=2)
            ),
            JournalEntry(
                id=4,
                content="Fourth entry",
                mood="happy",
                category="health",
                tags=["exercise", "motivation"],
                created_at=self.base_date + timedelta(days=2)  # Same day as entry 3
            ),
            JournalEntry(
                id=5,
                content="Fifth entry",
                mood="calm",
                category="personal",
                tags=["meditation", "mindfulness"],
                created_at=self.base_date + timedelta(days=4)  # Gap of 1 day
            ),
        ]
        
        self.insight_data = InsightData(entries=self.test_entries)
        self.helper = InsightsHelper(self.insight_data)
    
    def test_calculate_streak_with_consecutive_days(self):
        """Test streak calculation with consecutive entries."""
        # Create entries for consecutive days leading up to today
        today = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        consecutive_entries = [
            JournalEntry(1, "Today", "happy", "personal", [], today),
            JournalEntry(2, "Yesterday", "good", "work", [], today - timedelta(days=1)),
            JournalEntry(3, "Day before", "calm", "health", [], today - timedelta(days=2)),
        ]
        
        helper = InsightsHelper(InsightData(entries=consecutive_entries))
        streak = helper.calculate_streak()
        
        assert streak == 3
    
    def test_calculate_streak_with_gap(self):
        """Test streak calculation when there's a gap in entries."""
        today = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        entries_with_gap = [
            JournalEntry(1, "Today", "happy", "personal", [], today),
            JournalEntry(2, "Yesterday", "good", "work", [], today - timedelta(days=1)),
            # Gap of one day
            JournalEntry(3, "Three days ago", "calm", "health", [], today - timedelta(days=3)),
        ]
        
        helper = InsightsHelper(InsightData(entries=entries_with_gap))
        streak = helper.calculate_streak()
        
        assert streak == 2
    
    def test_calculate_streak_no_recent_entries(self):
        """Test streak calculation when there are no recent entries."""
        old_date = datetime.now() - timedelta(days=10)
        old_entries = [
            JournalEntry(1, "Old entry", "happy", "personal", [], old_date),
        ]
        
        helper = InsightsHelper(InsightData(entries=old_entries))
        streak = helper.calculate_streak()
        
        assert streak == 0
    
    def test_calculate_streak_empty_entries(self):
        """Test streak calculation with no entries."""
        helper = InsightsHelper(InsightData(entries=[]))
        streak = helper.calculate_streak()
        
        assert streak == 0
    
    def test_get_daily_counts_default_period(self):
        """Test daily counts for default 30-day period."""
        daily_counts = self.helper.get_daily_counts()
        
        # Should return 30 days of data
        assert len(daily_counts) == 30
        
        # All dates should be strings in ISO format
        for date_str in daily_counts.keys():
            datetime.fromisoformat(date_str)  # Should not raise exception
        
        # All counts should be non-negative integers
        for count in daily_counts.values():
            assert isinstance(count, int)
            assert count >= 0
    
    def test_get_daily_counts_custom_period(self):
        """Test daily counts for custom period."""
        daily_counts = self.helper.get_daily_counts(days=7)
        
        # Should return 7 days of data
        assert len(daily_counts) == 7
    
    def test_get_daily_counts_with_entries_in_range(self):
        """Test daily counts when entries fall within the date range."""
        # Create helper with entries from recent dates
        today = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        recent_entries = [
            JournalEntry(1, "Today", "happy", "personal", [], today),
            JournalEntry(2, "Today again", "good", "work", [], today),
            JournalEntry(3, "Yesterday", "calm", "health", [], today - timedelta(days=1)),
        ]
        
        helper = InsightsHelper(InsightData(entries=recent_entries))
        daily_counts = helper.get_daily_counts(days=3)
        
        today_str = today.date().isoformat()
        yesterday_str = (today - timedelta(days=1)).date().isoformat()
        
        assert daily_counts[today_str] == 2
        assert daily_counts[yesterday_str] == 1
    
    def test_get_mood_breakdown(self):
        """Test mood breakdown calculation."""
        mood_breakdown = self.helper.get_mood_breakdown()
        
        expected_moods = {
            "happy": 2,
            "excited": 1,
            "content": 1,
            "calm": 1
        }
        
        assert mood_breakdown == expected_moods
    
    def test_get_mood_breakdown_empty_entries(self):
        """Test mood breakdown with no entries."""
        helper = InsightsHelper(InsightData(entries=[]))
        mood_breakdown = helper.get_mood_breakdown()
        
        assert mood_breakdown == {}
    
    def test_get_mood_breakdown_with_empty_moods(self):
        """Test mood breakdown when some entries have empty moods."""
        entries_with_empty_moods = [
            JournalEntry(1, "Entry 1", "happy", "personal", [], self.base_date),
            JournalEntry(2, "Entry 2", "", "work", [], self.base_date),
            JournalEntry(3, "Entry 3", None, "health", [], self.base_date),
        ]
        
        helper = InsightsHelper(InsightData(entries=entries_with_empty_moods))
        mood_breakdown = helper.get_mood_breakdown()
        
        assert mood_breakdown == {"happy": 1}
    
    def test_get_category_breakdown(self):
        """Test category breakdown calculation."""
        category_breakdown = self.helper.get_category_breakdown()
        
        expected_categories = {
            "personal": 3,
            "work": 1,
            "health": 1
        }
        
        assert category_breakdown == expected_categories
    
    def test_get_category_breakdown_empty_entries(self):
        """Test category breakdown with no entries."""
        helper = InsightsHelper(InsightData(entries=[]))
        category_breakdown = helper.get_category_breakdown()
        
        assert category_breakdown == {}
    
    def test_get_top_tags_default_limit(self):
        """Test top tags with default limit."""
        top_tags = self.helper.get_top_tags()
        
        # Check that we have the right number of tags
        assert len(top_tags) == 8
        
        # Check that the first two tags have count 2 (order may vary for ties)
        first_two_counts = [count for tag, count in top_tags[:2]]
        assert all(count == 2 for count in first_two_counts)
        
        # Check that tags with count 2 are goals and motivation
        first_two_tags = {tag for tag, count in top_tags[:2]}
        assert first_two_tags == {"goals", "motivation"}
        
        # Check that remaining tags have count 1
        remaining_counts = [count for tag, count in top_tags[2:]]
        assert all(count == 1 for count in remaining_counts)
        
        # Check that all expected tags are present
        all_tags = {tag for tag, count in top_tags}
        expected_all_tags = {"goals", "motivation", "productivity", "reflection", 
                           "gratitude", "exercise", "meditation", "mindfulness"}
        assert all_tags == expected_all_tags
    
    def test_get_top_tags_custom_limit(self):
        """Test top tags with custom limit."""
        top_tags = self.helper.get_top_tags(limit=3)
        
        assert len(top_tags) == 3
        
        # First two should be tied at 2 occurrences
        tag_names = [tag[0] for tag in top_tags]
        assert "goals" in tag_names
        assert "motivation" in tag_names
    
    def test_get_top_tags_empty_entries(self):
        """Test top tags with no entries."""
        helper = InsightsHelper(InsightData(entries=[]))
        top_tags = helper.get_top_tags()
        
        assert top_tags == []
    
    def test_get_top_tags_entries_without_tags(self):
        """Test top tags when entries have no tags."""
        entries_without_tags = [
            JournalEntry(1, "Entry 1", "happy", "personal", [], self.base_date),
            JournalEntry(2, "Entry 2", "good", "work", None, self.base_date),
        ]
        
        helper = InsightsHelper(InsightData(entries=entries_without_tags))
        top_tags = helper.get_top_tags()
        
        assert top_tags == []
    
    def test_get_totals(self):
        """Test totals calculation."""
        totals = self.helper.get_totals()
        
        expected_totals = {
            'total_entries': 5,
            'unique_moods': 4,  # happy, excited, content, calm
            'unique_categories': 3,  # personal, work, health
            'unique_tags': 8,  # motivation, goals, productivity, reflection, gratitude, exercise, meditation, mindfulness
        }
        
        assert totals == expected_totals
    
    def test_get_totals_empty_entries(self):
        """Test totals with no entries."""
        helper = InsightsHelper(InsightData(entries=[]))
        totals = helper.get_totals()
        
        expected_totals = {
            'total_entries': 0,
            'unique_moods': 0,
            'unique_categories': 0,
            'unique_tags': 0,
        }
        
        assert totals == expected_totals
    
    def test_get_totals_with_duplicates(self):
        """Test totals calculation with duplicate moods/categories/tags."""
        # This is already tested in the main test, but let's be explicit
        totals = self.helper.get_totals()
        
        # Even though "happy" appears twice, it should only count as 1 unique mood
        # Same for "personal" category and tags like "goals" and "motivation"
        assert totals['unique_moods'] == 4
        assert totals['unique_categories'] == 3
    
    def test_get_writing_frequency(self):
        """Test writing frequency calculation."""
        frequency = self.helper.get_writing_frequency()
        
        # Entries span from base_date to base_date + 4 days = 5 days total
        # 5 entries over 5 days = 1.0 entries per day
        expected_frequency = 5.0 / 5.0
        
        assert frequency == expected_frequency
    
    def test_get_writing_frequency_single_day(self):
        """Test writing frequency when all entries are on the same day."""
        single_day_entries = [
            JournalEntry(1, "Entry 1", "happy", "personal", [], self.base_date),
            JournalEntry(2, "Entry 2", "good", "work", [], self.base_date),
            JournalEntry(3, "Entry 3", "calm", "health", [], self.base_date),
        ]
        
        helper = InsightsHelper(InsightData(entries=single_day_entries))
        frequency = helper.get_writing_frequency()
        
        # 3 entries on 1 day = 3.0 entries per day
        assert frequency == 3.0
    
    def test_get_writing_frequency_empty_entries(self):
        """Test writing frequency with no entries."""
        helper = InsightsHelper(InsightData(entries=[]))
        frequency = helper.get_writing_frequency()
        
        assert frequency == 0.0
    
    def test_insight_data_with_none_entries(self):
        """Test InsightData initialization with None entries."""
        insight_data = InsightData(entries=None)
        helper = InsightsHelper(insight_data)
        
        assert helper.entries == []
        assert helper.calculate_streak() == 0
        assert helper.get_totals()['total_entries'] == 0
    
    def test_journal_entry_with_none_tags(self):
        """Test JournalEntry initialization with None tags."""
        entry = JournalEntry(
            id=1,
            content="Test entry",
            mood="happy",
            category="personal",
            tags=None,
            created_at=self.base_date
        )
        
        assert entry.tags == []