# Baddie AI Journal Hustle 👑

**Transform your life with AI-powered journaling - the smart platform that turns your thoughts into actionable insights.**

🌐 **[View Live Landing Page](./index.html)** | 📊 **Smart Analytics** | 🔥 **Streak Tracking** | 🎯 **Goal Setting**

## 🚀 Landing Page

Our beautiful, responsive landing page showcases the power of Baddie AI Journal Hustle:

- **Modern Design**: Clean, gradient-based UI with smooth animations
- **Responsive Layout**: Optimized for desktop, tablet, and mobile devices
- **Interactive Elements**: Engaging hover effects and button animations
- **Brand Identity**: Custom logo and consistent visual design
- **Call-to-Actions**: Strategic placement to drive user engagement

### Features Highlighted:
- 📊 Smart Analytics & Insights
- 🔥 Streak Tracking & Motivation
- 🎯 AI-Powered Goal Recommendations
- 🏷️ Intelligent Tag Classification
- 📱 Mobile-First Responsive Design
- 🔒 Privacy & Security Focus

## 💡 Insights Feature

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

### Example Usage
```python
from datetime import datetime
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper

# Sample entries
entries = [
    JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.utcnow()),
    JournalEntry(2, "Productive work", "focused", "work", ["productivity"], datetime.utcnow())
]

helper = InsightsHelper(InsightData(entries))
print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")
print(f"Top tags: {helper.get_top_tags(5)}")
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

## 🏗️ Project Structure

```
Baddie-Ai-journal-hustle/
├── index.html          # Main landing page
├── styles.css          # CSS styles and responsive design
├── script.js           # JavaScript for interactivity
├── assets/
│   └── logo.svg        # Brand logo
├── issues/             # Project issues and documentation
└── README.md           # This file
```

## 🔧 Development

To run the landing page locally:

1. Clone the repository
2. Open `index.html` in your browser, or
3. Run a local server: `python3 -m http.server 8000`
4. Navigate to `http://localhost:8000`

## 🎨 Design Features

- **Color Scheme**: Purple gradient (#667eea to #764ba2) with clean whites and grays
- **Typography**: Modern Poppins font family for readability
- **Animations**: Smooth CSS transitions and JavaScript-powered interactions
- **Icons**: Emoji-based icons for visual appeal and accessibility
- **Layout**: CSS Grid and Flexbox for responsive design

---

**© 2024 Baddie AI Journal Hustle. All rights reserved.**
