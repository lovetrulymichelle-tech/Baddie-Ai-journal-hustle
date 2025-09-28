"""
Services package for Baddie AI Journal Hustle.

This package contains business logic services:
- StripeService: Stripe payment integration
- NotificationService: Trial/upgrade notifications
- SubscriptionService: Core subscription management
"""

from .stripe_service import StripeService
from .notification_service import NotificationService
from .subscription_service import SubscriptionService

__all__ = ["StripeService", "NotificationService", "SubscriptionService"]
