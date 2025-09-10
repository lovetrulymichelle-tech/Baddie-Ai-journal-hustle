"""
Command Line Interface for the Baddie AI Journal application.

This module provides a simple CLI for testing and demonstrating the journal functionality.
"""

import json
from datetime import datetime
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper


def create_sample_data():
    """Create sample journal entries for demonstration."""
    now = datetime.utcnow()
    
    sample_entries = [
        JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], now),
        JournalEntry(2, "Productive work", "focused", "work", ["productivity"], now),
        JournalEntry(3, "Feeling grateful for my family", "grateful", "personal", ["gratitude", "family"], now),
        JournalEntry(4, "Completed my project!", "excited", "work", ["achievement", "productivity"], now),
        JournalEntry(5, "Relaxing evening", "peaceful", "personal", ["relaxation"], now),
    ]
    
    return sample_entries


def demonstrate_insights():
    """Demonstrate the insights functionality."""
    print("🌟 Baddie AI Journal - Insights Demo 🌟")
    print("=" * 50)
    
    # Create sample data
    entries = create_sample_data()
    insight_data = InsightData(entries)
    helper = InsightsHelper(insight_data)
    
    # Generate insights
    print(f"\n📊 Current streak: {helper.calculate_streak()} days")
    
    print(f"\n😊 Mood breakdown:")
    mood_breakdown = helper.get_mood_breakdown()
    for mood, count in mood_breakdown.items():
        print(f"  {mood}: {count}")
    
    print(f"\n📁 Category breakdown:")
    category_breakdown = helper.get_category_breakdown()
    for category, count in category_breakdown.items():
        print(f"  {category}: {count}")
    
    print(f"\n🏷️ Top tags:")
    top_tags = helper.get_top_tags(5)
    for tag, count in top_tags:
        print(f"  {tag}: {count}")
    
    print(f"\n📈 Metrics:")
    metrics = helper.get_totals_and_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Generate and display full report
    print(f"\n📋 Full Report (JSON):")
    report = helper.generate_full_report()
    print(json.dumps(report, indent=2, default=str))
    
    # Demonstrate CSV export
    csv_filename = "sample_journal_export.csv"
    helper.export_to_csv(csv_filename)
    print(f"\n💾 Data exported to: {csv_filename}")


def main():
    """Main CLI entry point."""
    try:
        demonstrate_insights()
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    print("\n✅ Demo completed successfully!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())