"""
Baddie AI Journal Hustle - A Python-based journaling application with AI-powered insights.

This package provides:
- JournalEntry and InsightData models
- InsightsHelper for analytics calculations
- Swarms-powered AI analysis capabilities
"""

__version__ = "0.1.0"

from .models import JournalEntry, InsightData
from .insights import InsightsHelper
from .swarms_integration import JournalAnalysisSwarm, SwarmAnalysisResult

__all__ = ["JournalEntry", "InsightData", "InsightsHelper", "JournalAnalysisSwarm", "SwarmAnalysisResult"]