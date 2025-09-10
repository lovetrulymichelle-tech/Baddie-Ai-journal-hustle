#!/usr/bin/env python3
"""
Demo script that demonstrates the exact usage shown in the README.
"""

from datetime import datetime
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper

# Sample entries (as shown in README)
entries = [
    JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.utcnow()),
    JournalEntry(2, "Productive work", "focused", "work", ["productivity"], datetime.utcnow())
]

helper = InsightsHelper(InsightData(entries))
print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")
print(f"Top tags: {helper.get_top_tags(5)}")