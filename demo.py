#!/usr/bin/env python3
"""
Demo script for Baddie AI Journal Hustle with Swarms integration.

This script demonstrates the core functionality including:
- Creating sample journal entries
- Basic insights analysis
- Swarms-powered AI analysis (if API key is available)
"""

import os
import sys
from datetime import datetime, UTC, timedelta

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from baddie_journal.models import JournalEntry, InsightData  # noqa: E402
from baddie_journal.insights import InsightsHelper  # noqa: E402

# Optional swarms integration
try:
    from baddie_journal.swarms_integration import JournalAnalysisSwarm  # noqa: E402

    SWARMS_AVAILABLE = True
except ImportError:
    SWARMS_AVAILABLE = False
    JournalAnalysisSwarm = None


def create_sample_data() -> InsightData:
    """Create sample journal entries for demonstration."""
    print("🔄 Creating sample journal entries...")

    # Sample entries spanning a few days
    entries = [
        JournalEntry(
            id=1,
            content=(
                "Started my day with meditation and felt really centered. Work was productive "
                "and I accomplished all my goals. Feeling grateful for this positive momentum."
            ),
            mood="happy",
            category="personal",
            tags=["meditation", "productivity", "gratitude"],
            timestamp=datetime.now(UTC) - timedelta(days=5),
        ),
        JournalEntry(
            id=2,
            content=(
                "Had a challenging day at work with lots of meetings. Felt overwhelmed "
                "but managed to push through. Need to work on time management."
            ),
            mood="stressed",
            category="work",
            tags=["meetings", "overwhelmed", "time-management"],
            timestamp=datetime.now(UTC) - timedelta(days=4),
        ),
        JournalEntry(
            id=3,
            content=(
                "Great workout this morning! Ran 5k and felt amazing afterward. "
                "Energy levels are high and I'm motivated to tackle the day."
            ),
            mood="energetic",
            category="health",
            tags=["exercise", "running", "motivation"],
            timestamp=datetime.now(UTC) - timedelta(days=3),
        ),
        JournalEntry(
            id=4,
            content=(
                "Spent quality time with family today. Had deep conversations and felt really "
                "connected. These moments are what matter most."
            ),
            mood="content",
            category="personal",
            tags=["family", "connection", "relationships"],
            timestamp=datetime.now(UTC) - timedelta(days=2),
        ),
        JournalEntry(
            id=5,
            content=(
                "Feeling a bit down today. Not sure why, just one of those days. "
                "Tried to stay positive but it's been difficult."
            ),
            mood="melancholy",
            category="personal",
            tags=["reflection", "emotions"],
            timestamp=datetime.now(UTC) - timedelta(days=1),
        ),
        JournalEntry(
            id=6,
            content=(
                "New day, new perspective! Yesterday's mood has lifted. Started a new "
                "project at work and feeling excited about the possibilities."
            ),
            mood="optimistic",
            category="work",
            tags=["new-project", "excitement", "fresh-start"],
            timestamp=datetime.now(UTC),
        ),
    ]

    print(f"✅ Created {len(entries)} sample journal entries")
    return InsightData(entries)


def demonstrate_basic_insights(insight_data: InsightData):
    """Demonstrate basic insights functionality."""
    print("\n📊 BASIC INSIGHTS ANALYSIS")
    print("=" * 50)

    helper = InsightsHelper(insight_data)

    # Calculate basic metrics
    print(f"📝 Current streak: {helper.calculate_streak()} days")
    print(f"📊 Total entries: {insight_data.total_entries()}")
    print(
        f"📈 Average frequency (30 days): {helper.get_writing_frequency(30):.1f} entries/day"
    )

    # Mood breakdown
    mood_breakdown = helper.get_mood_breakdown()
    print("\n😊 Mood breakdown:")
    for mood, count in mood_breakdown.items():
        percentage = (count / insight_data.total_entries()) * 100
        print(f"  {mood}: {count} entries ({percentage:.1f}%)")

    # Top tags
    top_tags = helper.get_top_tags(5)
    print("\n🏷️  Top tags:")
    for tag, count in top_tags:
        print(f"  #{tag}: {count} times")

    # Generate summary report
    print("\n📋 SUMMARY REPORT")
    print("-" * 30)
    report = helper.generate_summary_report()
    print(report)


def demonstrate_swarms_analysis(insight_data: InsightData):
    """Demonstrate Swarms AI analysis if API key is available."""
    print("\n🤖 SWARMS AI ANALYSIS")
    print("=" * 50)

    if not SWARMS_AVAILABLE:
        print("⚠️  Swarms framework not available. Skipping AI analysis.")
        print("   To enable AI analysis, install: pip install swarms>=6.0.0")
        return

    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OpenAI API key not found. Skipping AI analysis.")
        print("   To enable AI analysis, set the OPENAI_API_KEY environment variable.")
        return

    try:
        print("🔄 Initializing Journal Analysis Swarm...")
        swarm = JournalAnalysisSwarm(api_key=api_key)

        print("🔄 Performing comprehensive AI analysis...")
        result = swarm.perform_comprehensive_analysis(insight_data)

        print("✅ AI Analysis completed!")
        print(f"📅 Generated at: {result.generated_at}")

        # Display mood analysis
        print("\n😊 MOOD ANALYSIS:")
        print("-" * 20)
        if "error" not in result.mood_analysis:
            if "dominant_moods" in result.mood_analysis:
                print(
                    f"Dominant moods: {', '.join(result.mood_analysis['dominant_moods'])}"
                )
            if "mood_stability" in result.mood_analysis:
                print(f"Mood stability: {result.mood_analysis['mood_stability']}")
            if "insights" in result.mood_analysis:
                print("Key insights:")
                for insight in result.mood_analysis["insights"]:
                    print(f"  • {insight}")
        else:
            print(f"❌ {result.mood_analysis['error']}")

        # Display pattern insights
        print("\n🔍 PATTERN INSIGHTS:")
        print("-" * 20)
        if "error" not in result.pattern_insights:
            if "recurring_themes" in result.pattern_insights:
                print(
                    f"Recurring themes: {', '.join(result.pattern_insights['recurring_themes'])}"
                )
            if "writing_patterns" in result.pattern_insights:
                print(
                    f"Writing patterns: {result.pattern_insights['writing_patterns']}"
                )
        else:
            print(f"❌ {result.pattern_insights['error']}")

        # Display growth insights
        print("\n🌱 PERSONAL GROWTH INSIGHTS:")
        print("-" * 30)
        if "error" not in result.personal_growth_insights:
            if "strengths" in result.personal_growth_insights:
                print("Identified strengths:")
                for strength in result.personal_growth_insights["strengths"]:
                    print(f"  • {strength}")
            if "improvement_areas" in result.personal_growth_insights:
                print("Areas for improvement:")
                for area in result.personal_growth_insights["improvement_areas"]:
                    print(f"  • {area}")
        else:
            print(f"❌ {result.personal_growth_insights['error']}")

        # Display recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 20)
        if result.recommendations:
            for i, rec in enumerate(result.recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  No recommendations generated")

    except Exception as e:
        print(f"❌ Swarms analysis failed: {str(e)}")
        print("   This might be due to API key issues or network connectivity.")


def main():
    """Main demonstration function."""
    print("🌟 BADDIE AI JOURNAL HUSTLE - SWARMS DEMO")
    print("=" * 50)

    # Create sample data
    insight_data = create_sample_data()

    # Demonstrate basic insights
    demonstrate_basic_insights(insight_data)

    # Demonstrate swarms analysis
    demonstrate_swarms_analysis(insight_data)

    print("\n✨ Demo completed!")
    print(
        "To run with your own data, create JournalEntry objects and use InsightData to wrap them."
    )
    print("For AI analysis, make sure to set your OPENAI_API_KEY environment variable.")


if __name__ == "__main__":
    main()
