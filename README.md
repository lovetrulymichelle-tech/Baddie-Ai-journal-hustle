## Insights Feature

The Insights feature provides analytics on your journal entries to help you track patterns, moods, and productivity over time.

### What Insights Show You
- **Streaks:** See how many consecutive days you’ve written entries.
- **Daily Counts:** Track your journaling frequency over the last 30 days (customizable).
- **Mood & Category Breakdown:** Visualize the distribution of your moods and categories.
- **Top Tags:** Discover which tags you use most (set your own limit for top results).
- **Totals & Metrics:** Total entries, unique tags/categories, and average writing frequency.

### How It Works
- Data is analyzed in real-time from your journal entries.
- All times are stored and calculated in UTC (Coordinated Universal Time) for consistency across time zones.
- CSV export is available for deeper analysis or backup.

### Getting Started

#### Installation
```bash
pip install -e .
```

#### Using the CLI
The Baddie AI Journal comes with a powerful command-line interface:

```bash
# Add a new journal entry
baddie-journal add "Had a great day!" happy personal "motivation,gratitude"

# List your recent entries
baddie-journal list --limit 5

# View insights and analytics
baddie-journal insights --days 7

# Search your entries
baddie-journal search "productivity"

# Export your data
baddie-journal export journal_backup.csv

# Delete an entry
baddie-journal delete 1

# Run the demo
baddie-journal demo
```

### Example Usage (Code)
```python
from datetime import datetime
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper
from baddie_journal.storage import JsonStorage

# Using storage for persistence
storage = JsonStorage("my_journal.json")

# Create and save entries
entry1 = JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.utcnow())
entry2 = JournalEntry(2, "Productive work", "focused", "work", ["productivity"], datetime.utcnow())

storage.save_entry(entry1)
storage.save_entry(entry2)

# Generate insights
insight_data = storage.get_insight_data()
helper = InsightsHelper(insight_data)

print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")
print(f"Top tags: {helper.get_top_tags(5)}")

# Export data
helper.export_to_csv("my_journal_export.csv")
```

### Interpreting Your Insights
- **Streaks:** Longer streaks mean more consistent journaling.
- **Mood breakdown:** Shows your emotional trends—use to spot highs/lows or triggers.
- **Top tags:** Reveals what topics or feelings dominate your journaling.

### Export & Privacy
- You can export your insights as a CSV.
- Analytics are private and visible only to you.

---

For questions, feedback, or to suggest new insights, open an issue or contact support.
