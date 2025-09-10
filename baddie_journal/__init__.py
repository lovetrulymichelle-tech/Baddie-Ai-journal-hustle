"""
Baddie AI Journal - A journaling application with AI-powered insights.

This package provides tools for managing journal entries and generating
analytics to help users track patterns, moods, and productivity over time.
"""

__version__ = "0.1.0"
__author__ = "Baddie AI Journal Team"

from .models import JournalEntry, InsightData
from .insights import InsightsHelper

__all__ = ["JournalEntry", "InsightData", "InsightsHelper"]