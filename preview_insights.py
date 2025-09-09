#!/usr/bin/env python3
"""
Preview script for the Baddie AI Journal Insights feature.
This script demonstrates the insights functionality with sample data.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add the current directory to Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper


def create_sample_data() -> list[JournalEntry]:
    """Create sample journal entries for demonstration."""
    sample_entries = []
    
    # Define sample data
    moods = ['happy', 'excited', 'focused', 'relaxed', 'motivated', 'grateful', 
             'contemplative', 'energetic', 'peaceful', 'confident']
    categories = ['personal', 'work', 'fitness', 'relationships', 'goals', 
                  'creativity', 'learning', 'travel', 'health', 'reflection']
    
    sample_contents_and_tags = [
        ("Great day at work! Finished the big project.", ['productivity', 'achievement', 'work']),
        ("Morning run felt amazing today.", ['fitness', 'exercise', 'morning']),
        ("Had a wonderful dinner with friends.", ['social', 'friends', 'food']),
        ("Finally started reading that book I bought.", ['reading', 'books', 'learning']),
        ("Meditation session helped me center myself.", ['mindfulness', 'meditation', 'peace']),
        ("Productive coding session today.", ['programming', 'productivity', 'tech']),
        ("Visited the art museum - so inspiring!", ['art', 'culture', 'inspiration']),
        ("Cooked a new recipe and it turned out great!", ['cooking', 'creativity', 'food']),
        ("Video call with family was heartwarming.", ['family', 'connection', 'love']),
        ("Worked on my side project for 2 hours.", ['sideproject', 'programming', 'goals']),
        ("Beautiful sunset walk in the park.", ['nature', 'walking', 'beauty']),
        ("Finished organizing my workspace.", ['organization', 'productivity', 'space']),
        ("Had an insightful conversation with a mentor.", ['mentorship', 'learning', 'growth']),
        ("Yoga class was exactly what I needed.", ['yoga', 'fitness', 'mindfulness']),
        ("Wrote in my gratitude journal.", ['gratitude', 'writing', 'reflection']),
        ("Successful presentation at work today.", ['work', 'achievement', 'confidence']),
        ("Tried a new coffee shop - great atmosphere.", ['coffee', 'exploration', 'atmosphere']),
        ("Movie night with my partner was perfect.", ['relationship', 'entertainment', 'connection']),
        ("Morning pages helped clear my mind.", ['writing', 'clarity', 'morning']),
        ("Completed my first 5K run!", ['fitness', 'achievement', 'running'])
    ]
    
    # Create entries for the last 30 days
    base_date = datetime.now()
    
    for i in range(20):  # Create 20 sample entries
        # Random date within last 30 days
        days_back = random.randint(0, 29)
        entry_date = base_date - timedelta(days=days_back)
        
        # Add some random time variance
        entry_date = entry_date.replace(
            hour=random.randint(8, 22),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        
        content, tags = random.choice(sample_contents_and_tags)
        mood = random.choice(moods)
        category = random.choice(categories)
        
        entry = JournalEntry(
            id=i + 1,
            content=content,
            mood=mood,
            category=category,
            tags=tags,
            created_at=entry_date
        )
        
        sample_entries.append(entry)
    
    return sample_entries


def print_insights_preview(helper: InsightsHelper):
    """Print a formatted preview of the insights."""
    print("🌟 BADDIE AI JOURNAL - INSIGHTS PREVIEW 🌟")
    print("=" * 50)
    
    # Basic metrics
    metrics = helper.get_totals_and_metrics()
    print(f"\n📊 OVERVIEW:")
    print(f"   Total Entries: {metrics['total_entries']}")
    print(f"   Date Range: {metrics['date_range_days']} days")
    print(f"   Average Entries/Day: {metrics['average_entries_per_day']}")
    print(f"   Unique Moods: {metrics['unique_moods']}")
    print(f"   Unique Categories: {metrics['unique_categories']}")
    print(f"   Unique Tags: {metrics['unique_tags']}")
    
    # Streak
    streak = helper.calculate_streak()
    print(f"\n🔥 CURRENT STREAK: {streak} days")
    
    # Mood breakdown
    mood_breakdown = helper.get_mood_breakdown()
    print(f"\n😊 MOOD BREAKDOWN:")
    for mood, count in sorted(mood_breakdown.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / metrics['total_entries']) * 100
        print(f"   {mood.capitalize()}: {count} ({percentage:.1f}%)")
    
    # Category breakdown
    category_breakdown = helper.get_category_breakdown()
    print(f"\n📂 CATEGORY BREAKDOWN:")
    for category, count in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / metrics['total_entries']) * 100
        print(f"   {category.capitalize()}: {count} ({percentage:.1f}%)")
    
    # Top tags
    top_tags = helper.get_top_tags(8)
    print(f"\n🏷️  TOP TAGS:")
    for tag, count in top_tags:
        print(f"   #{tag}: {count} times")
    
    # Daily activity (last 7 days)
    daily_counts = helper.get_daily_counts(7)
    print(f"\n📅 LAST 7 DAYS ACTIVITY:")
    for date_str, count in sorted(daily_counts.items(), reverse=True)[:7]:
        print(f"   {date_str}: {count} entries")


def main():
    """Main function to run the insights preview."""
    print("Creating sample journal data...")
    
    # Create sample data
    sample_entries = create_sample_data()
    
    # Create insights helper
    insight_data = InsightData(sample_entries)
    helper = InsightsHelper(insight_data)
    
    # Display insights
    print_insights_preview(helper)
    
    # Offer CSV export
    print(f"\n" + "=" * 50)
    export_choice = input("\nWould you like to export insights to CSV? (y/n): ").strip().lower()
    
    if export_choice == 'y':
        csv_content = helper.export_to_csv()
        filename = f"insights_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as f:
            f.write(csv_content)
        
        print(f"✅ Insights exported to: {filename}")
    
    print("\n🎉 Thanks for previewing the Baddie AI Journal Insights feature!")
    print("This preview shows how the insights would work with your actual journal data.")


if __name__ == "__main__":
    main()