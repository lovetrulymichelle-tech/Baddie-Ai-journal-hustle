"""
Baddie AI Journal Hustle - A Python-based journaling application with AI-powered insights.

This package provides:
- JournalEntry and InsightData models for journaling
- User, Subscription, and SubscriptionPlan models for subscription management
- InsightsHelper for analytics calculations
- Swarms-powered AI analysis capabilities
- Subscription services for trial and billing management
"""

__version__ = "0.1.0"

from .models import JournalEntry, InsightData, User, Subscription, SubscriptionPlan
from .insights import InsightsHelper
from .swarms_integration import JournalAnalysisSwarm, SwarmAnalysisResult
from .services import StripeService, NotificationService, SubscriptionService

__all__ = [
    "JournalEntry", "InsightData", "User", "Subscription", "SubscriptionPlan",
    "InsightsHelper", "JournalAnalysisSwarm", "SwarmAnalysisResult",
    "StripeService", "NotificationService", "SubscriptionService"
]
