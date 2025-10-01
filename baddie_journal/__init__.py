"""
Baddie AI Journal Hustle - A Python-based journaling application with AI-powered insights.

This package provides:
- JournalEntry and InsightData models for journaling
- User, Subscription, and SubscriptionPlan models for subscription management
- ProductItem, ProductAnalysis, PricingGuidance models for thrift e-commerce
- InsightsHelper for analytics calculations
- Swarms-powered AI analysis capabilities (journal and thrift)
- Subscription services for trial and billing management
"""

__version__ = "0.1.0"

from .models import (
    JournalEntry,
    InsightData,
    User,
    Subscription,
    SubscriptionPlan,
    ProductItem,
    ProductAnalysis,
    PricingGuidance,
    ProductListing,
)
from .insights import InsightsHelper

# Optional imports - make them available only if dependencies are installed
try:
    from .swarms_integration import JournalAnalysisSwarm, SwarmAnalysisResult

    _swarms_available = True
except ImportError:
    _swarms_available = False
    JournalAnalysisSwarm = None
    SwarmAnalysisResult = None

try:
    from .thrift_swarms import ThriftContentSwarm, ThriftAnalysisResult

    _thrift_swarms_available = True
except ImportError:
    _thrift_swarms_available = False
    ThriftContentSwarm = None
    ThriftAnalysisResult = None

try:
    from .services import StripeService, NotificationService, SubscriptionService

    _services_available = True
except ImportError:
    _services_available = False
    StripeService = None
    NotificationService = None
    SubscriptionService = None

# Dynamic __all__ based on available components
__all__ = [
    "JournalEntry",
    "InsightData",
    "User",
    "Subscription",
    "SubscriptionPlan",
    "ProductItem",
    "ProductAnalysis",
    "PricingGuidance",
    "ProductListing",
    "InsightsHelper",
]

if _swarms_available:
    __all__.extend(["JournalAnalysisSwarm", "SwarmAnalysisResult"])

if _thrift_swarms_available:
    __all__.extend(["ThriftContentSwarm", "ThriftAnalysisResult"])

if _services_available:
    __all__.extend(["StripeService", "NotificationService", "SubscriptionService"])
