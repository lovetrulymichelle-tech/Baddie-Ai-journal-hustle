# How to Preview the Baddie AI Journal Insights Feature

This repository contains a working implementation of the journal insights feature described in the main README.md.

## Quick Start

Run the preview with sample data:

```bash
python3 preview_insights.py
```

This will:
- Generate 20 sample journal entries with realistic data
- Display comprehensive insights including streaks, mood breakdowns, category analysis, and top tags
- Offer to export the insights to a CSV file

## What You'll See

The preview demonstrates all the features mentioned in the README:

- **Current Streak**: Days of consecutive journaling
- **Overview Metrics**: Total entries, date range, averages, and unique counts
- **Mood Breakdown**: Distribution of moods with percentages
- **Category Breakdown**: Distribution of categories with percentages  
- **Top Tags**: Most frequently used tags
- **Daily Activity**: Entry counts for the last 7 days
- **CSV Export**: Complete insights data in spreadsheet format

## Code Structure

- `baddie_journal/models.py` - JournalEntry and InsightData classes
- `baddie_journal/insights.py` - InsightsHelper class with all analysis methods
- `preview_insights.py` - Interactive preview script with sample data

## Dependencies

No external dependencies required! The implementation uses only Python standard library modules.

## Example Output

```
🌟 BADDIE AI JOURNAL - INSIGHTS PREVIEW 🌟
==================================================

📊 OVERVIEW:
   Total Entries: 20
   Date Range: 28 days
   Average Entries/Day: 0.71
   Unique Moods: 9
   Unique Categories: 9
   Unique Tags: 34

🔥 CURRENT STREAK: 2 days

😊 MOOD BREAKDOWN:
   Happy: 5 (25.0%)
   Focused: 4 (20.0%)
   Energetic: 3 (15.0%)
   ...
```

The preview shows exactly how the insights feature would work with real journal data!