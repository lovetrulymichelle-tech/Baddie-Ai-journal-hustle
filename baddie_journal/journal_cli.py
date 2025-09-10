"""
Enhanced Command Line Interface for the Baddie AI Journal application.

This module provides a full-featured CLI for managing journal entries and insights.
"""

import argparse
import json
import sys
from datetime import datetime
from baddie_journal.models import JournalEntry
from baddie_journal.insights import InsightsHelper
from baddie_journal.storage import JsonStorage


class JournalCLI:
    """Enhanced CLI for the Baddie AI Journal."""
    
    def __init__(self, storage_file: str = "my_journal.json"):
        """Initialize the CLI with storage."""
        self.storage = JsonStorage(storage_file)
    
    def add_entry(self, content: str, mood: str, category: str, tags: str = "") -> None:
        """Add a new journal entry."""
        try:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
            
            entry = JournalEntry(
                id=self.storage.get_next_id(),
                content=content,
                mood=mood,
                category=category,
                tags=tag_list,
                created_at=datetime.utcnow()
            )
            
            self.storage.save_entry(entry)
            print(f"✅ Journal entry #{entry.id} added successfully!")
            print(f"   Content: {content[:50]}{'...' if len(content) > 50 else ''}")
            print(f"   Mood: {mood} | Category: {category}")
            if tag_list:
                print(f"   Tags: {', '.join(tag_list)}")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def list_entries(self, limit: int = 10) -> None:
        """List recent journal entries."""
        entries = self.storage.load_entries_as_objects()
        
        if not entries:
            print("📝 No journal entries found. Add your first entry with 'add' command!")
            return
        
        # Show most recent entries first
        recent_entries = sorted(entries, key=lambda x: x.created_at, reverse=True)[:limit]
        
        print(f"\n📖 Your Recent Journal Entries (showing {len(recent_entries)} of {len(entries)}):")
        print("=" * 60)
        
        for entry in recent_entries:
            date_str = entry.created_at.strftime("%Y-%m-%d %H:%M")
            content_preview = entry.content[:80] + "..." if len(entry.content) > 80 else entry.content
            
            print(f"#{entry.id} | {date_str}")
            print(f"😊 {entry.mood} | 📁 {entry.category}")
            print(f"💬 {content_preview}")
            if entry.tags:
                print(f"🏷️  {', '.join(entry.tags)}")
            print("-" * 60)
    
    def show_insights(self, days: int = 30) -> None:
        """Show insights and analytics."""
        insight_data = self.storage.get_insight_data()
        
        if not insight_data.entries:
            print("📊 No entries found for insights. Start journaling to see analytics!")
            return
        
        helper = InsightsHelper(insight_data)
        
        print(f"\n🌟 Your Journal Insights (Last {days} days)")
        print("=" * 50)
        
        # Basic stats
        print(f"📊 Current streak: {helper.calculate_streak()} days")
        print(f"📈 Total entries: {len(insight_data.entries)}")
        
        # Mood breakdown
        print(f"\n😊 Mood breakdown:")
        mood_breakdown = helper.get_mood_breakdown()
        for mood, count in sorted(mood_breakdown.items(), key=lambda x: x[1], reverse=True):
            print(f"   {mood}: {count}")
        
        # Category breakdown
        print(f"\n📁 Category breakdown:")
        category_breakdown = helper.get_category_breakdown()
        for category, count in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
            print(f"   {category}: {count}")
        
        # Top tags
        print(f"\n🏷️ Top tags:")
        top_tags = helper.get_top_tags(10)
        for tag, count in top_tags[:5]:  # Show top 5
            print(f"   {tag}: {count}")
        
        # Daily activity
        daily_counts = helper.get_daily_counts(days)
        if daily_counts:
            total_days_with_entries = len(daily_counts)
            avg_per_active_day = sum(daily_counts.values()) / total_days_with_entries
            print(f"\n📅 Activity: {total_days_with_entries} days with entries")
            print(f"📊 Average entries per active day: {avg_per_active_day:.1f}")
    
    def export_data(self, filename: str = None) -> None:
        """Export journal data to CSV."""
        if not filename:
            filename = f"journal_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        insight_data = self.storage.get_insight_data()
        if not insight_data.entries:
            print("📊 No entries to export.")
            return
        
        helper = InsightsHelper(insight_data)
        helper.export_to_csv(filename)
        print(f"💾 Exported {len(insight_data.entries)} entries to {filename}")
    
    def delete_entry(self, entry_id: int) -> None:
        """Delete a journal entry."""
        if self.storage.delete_entry(entry_id):
            print(f"✅ Entry #{entry_id} deleted successfully.")
        else:
            print(f"❌ Entry #{entry_id} not found.")
    
    def search_entries(self, query: str) -> None:
        """Search entries by content, mood, category, or tags."""
        entries = self.storage.load_entries_as_objects()
        query_lower = query.lower()
        
        matching_entries = []
        for entry in entries:
            if (query_lower in entry.content.lower() or
                query_lower in entry.mood.lower() or
                query_lower in entry.category.lower() or
                any(query_lower in tag.lower() for tag in entry.tags)):
                matching_entries.append(entry)
        
        if not matching_entries:
            print(f"🔍 No entries found matching '{query}'")
            return
        
        print(f"\n🔍 Found {len(matching_entries)} entries matching '{query}':")
        print("=" * 60)
        
        for entry in sorted(matching_entries, key=lambda x: x.created_at, reverse=True):
            date_str = entry.created_at.strftime("%Y-%m-%d %H:%M")
            print(f"#{entry.id} | {date_str} | {entry.mood} | {entry.category}")
            print(f"💬 {entry.content}")
            if entry.tags:
                print(f"🏷️  {', '.join(entry.tags)}")
            print("-" * 60)


def create_parser():
    """Create argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Baddie AI Journal - Your personal journaling companion with insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Had a great day!" happy personal "motivation,gratitude"
  %(prog)s list --limit 5
  %(prog)s insights --days 7
  %(prog)s search "productivity"
  %(prog)s export journal_backup.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add entry command
    add_parser = subparsers.add_parser('add', help='Add a new journal entry')
    add_parser.add_argument('content', help='Journal entry content')
    add_parser.add_argument('mood', help='Your mood (e.g., happy, sad, excited)')
    add_parser.add_argument('category', help='Entry category (e.g., personal, work, health)')
    add_parser.add_argument('tags', nargs='?', default='', help='Comma-separated tags')
    
    # List entries command
    list_parser = subparsers.add_parser('list', help='List recent journal entries')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of entries to show (default: 10)')
    
    # Insights command
    insights_parser = subparsers.add_parser('insights', help='Show journal insights and analytics')
    insights_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze (default: 30)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export journal data to CSV')
    export_parser.add_argument('filename', nargs='?', help='Output filename (optional)')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a journal entry')
    delete_parser.add_argument('id', type=int, help='Entry ID to delete')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search journal entries')
    search_parser.add_argument('query', help='Search query')
    
    # Demo command
    subparsers.add_parser('demo', help='Run the insights demo')
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    cli = JournalCLI()
    
    try:
        if args.command == 'add':
            cli.add_entry(args.content, args.mood, args.category, args.tags)
        elif args.command == 'list':
            cli.list_entries(args.limit)
        elif args.command == 'insights':
            cli.show_insights(args.days)
        elif args.command == 'export':
            cli.export_data(args.filename)
        elif args.command == 'delete':
            cli.delete_entry(args.id)
        elif args.command == 'search':
            cli.search_entries(args.query)
        elif args.command == 'demo':
            # Import and run the original demo
            from .cli import demonstrate_insights
            demonstrate_insights()
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Keep journaling!")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())