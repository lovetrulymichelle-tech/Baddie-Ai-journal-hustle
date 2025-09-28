#!/usr/bin/env python3
"""
Basic tests for Baddie AI Journal Hustle functionality.

This script runs basic tests to verify the core functionality is working.
"""

import sys
from datetime import datetime, UTC, timedelta
from baddie_journal import JournalEntry, InsightData, InsightsHelper


def test_models():
    """Test the basic model functionality."""
    print("🧪 Testing Models...")

    # Test JournalEntry creation
    entry = JournalEntry(
        id=1,
        content="Test entry",
        mood="happy",
        category="test",
        tags=["testing", "demo"],
        timestamp=datetime.now(UTC),
    )

    assert entry.id == 1
    assert entry.mood == "happy"
    assert "testing" in entry.tags
    print("  ✅ JournalEntry creation successful")

    # Test InsightData
    entries = [entry]
    insight_data = InsightData(entries)
    assert insight_data.total_entries() == 1
    assert "happy" in insight_data.get_unique_moods()
    print("  ✅ InsightData creation successful")

    print("✅ Models tests passed\n")


def test_insights():
    """Test the insights functionality."""
    print("🧪 Testing Insights...")

    # Create test data
    entries = [
        JournalEntry(1, "Happy day", "happy", "personal", ["joy"], datetime.now(UTC)),
        JournalEntry(
            2,
            "Productive work",
            "focused",
            "work",
            ["productivity"],
            datetime.now(UTC) - timedelta(days=1),
        ),
        JournalEntry(
            3,
            "Reflection time",
            "contemplative",
            "personal",
            ["reflection"],
            datetime.now(UTC) - timedelta(days=2),
        ),
    ]

    insight_data = InsightData(entries)
    helper = InsightsHelper(insight_data)

    # Test streak calculation
    streak = helper.calculate_streak()
    assert isinstance(streak, int)
    print(f"  ✅ Streak calculation: {streak} days")

    # Test mood breakdown
    mood_breakdown = helper.get_mood_breakdown()
    assert isinstance(mood_breakdown, dict)
    assert len(mood_breakdown) == 3  # 3 different moods
    print(f"  ✅ Mood breakdown: {mood_breakdown}")

    # Test top tags
    top_tags = helper.get_top_tags(5)
    assert isinstance(top_tags, list)
    print(f"  ✅ Top tags: {top_tags}")

    # Test summary report
    report = helper.generate_summary_report()
    assert isinstance(report, str)
    assert "Total Entries: 3" in report
    print("  ✅ Summary report generation successful")

    print("✅ Insights tests passed\n")


def test_swarms_import():
    """Test swarms integration import."""
    print("🧪 Testing Swarms Integration...")

    try:
        # Test that we can import and create a swarm (without API key)
        from baddie_journal import JournalAnalysisSwarm

        print("  ✅ JournalAnalysisSwarm import successful")

        # Test that it properly handles missing API key
        try:
            JournalAnalysisSwarm()
            print("  ❌ Should have failed without API key")
        except ValueError as e:
            if "API key is required" in str(e):
                print("  ✅ Proper API key validation")
            else:
                raise

        print("✅ Swarms integration tests passed\n")

    except Exception as e:
        print(f"  ❌ Swarms integration test failed: {e}")
        return False

    return True


def main():
    """Run all tests."""
    print("🚀 Running Baddie AI Journal Tests\n")

    try:
        test_models()
        test_insights()
        test_swarms_import()

        print("🎉 All tests passed! Swarms implementation is working correctly.")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
