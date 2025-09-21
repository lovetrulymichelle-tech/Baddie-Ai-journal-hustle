"""
Subscription models for Baddie AI Journal Hustle.

This module defines subscription-related data structures:
- User: User account with subscription tracking
- SubscriptionPlan: Available subscription tiers
- Subscription: User's current subscription state
"""

from dataclasses import dataclass
from datetime import datetime, UTC, timedelta
from typing import Optional, Dict, Any
from enum import Enum


class SubscriptionStatus(Enum):
    """Subscription status enumeration."""
    TRIAL = "trial"
    ACTIVE = "active" 
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"


class SubscriptionPlanType(Enum):
    """Subscription plan types."""
    TRIAL = "trial"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class SubscriptionPlan:
    """
    Represents a subscription plan with pricing and features.
    
    Attributes:
        id: Unique identifier for the plan
        name: Display name of the plan
        plan_type: Type of plan (trial, basic, pro, enterprise)
        price_cents: Price in cents (e.g., 999 for $9.99)
        billing_interval: Billing frequency (monthly, yearly)
        trial_days: Number of trial days (0 if no trial)
        stripe_price_id: Stripe price ID for this plan
        features: Dictionary of plan features and limits
        is_active: Whether this plan is currently offered
    """
    id: str
    name: str
    plan_type: SubscriptionPlanType
    price_cents: int
    billing_interval: str  # "monthly", "yearly"
    trial_days: int
    stripe_price_id: Optional[str]
    features: Dict[str, Any]
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(UTC)
    
    @property
    def price_dollars(self) -> float:
        """Get price in dollars."""
        return self.price_cents / 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'plan_type': self.plan_type.value,
            'price_cents': self.price_cents,
            'price_dollars': self.price_dollars,
            'billing_interval': self.billing_interval,
            'trial_days': self.trial_days,
            'stripe_price_id': self.stripe_price_id,
            'features': self.features,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class User:
    """
    Represents a user account with subscription information.
    
    Attributes:
        id: Unique user identifier
        email: User's email address
        name: User's display name
        stripe_customer_id: Stripe customer ID for billing
        current_subscription_id: ID of current subscription
        created_at: Account creation timestamp
        last_login_at: Last login timestamp
        is_active: Whether the account is active
    """
    id: str
    email: str
    name: str
    stripe_customer_id: Optional[str] = None
    current_subscription_id: Optional[str] = None
    created_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    is_active: bool = True
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(UTC)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'stripe_customer_id': self.stripe_customer_id,
            'current_subscription_id': self.current_subscription_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'is_active': self.is_active
        }


@dataclass
class Subscription:
    """
    Represents a user's subscription with trial and billing logic.
    
    Attributes:
        id: Unique subscription identifier
        user_id: ID of the user who owns this subscription
        plan_id: ID of the subscription plan
        status: Current subscription status
        stripe_subscription_id: Stripe subscription ID
        trial_start: When trial period started
        trial_end: When trial period ends
        current_period_start: Start of current billing period
        current_period_end: End of current billing period
        cancel_at_period_end: Whether to cancel at period end
        cancelled_at: When subscription was cancelled
        created_at: When subscription was created
    """
    id: str
    user_id: str
    plan_id: str
    status: SubscriptionStatus
    stripe_subscription_id: Optional[str] = None
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    cancelled_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set creation timestamp and trial period if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(UTC)
    
    @property
    def is_trial_active(self) -> bool:
        """Check if trial period is currently active."""
        if self.status != SubscriptionStatus.TRIAL:
            return False
        
        if not self.trial_start or not self.trial_end:
            return False
        
        now = datetime.now(UTC)
        return self.trial_start <= now <= self.trial_end
    
    @property
    def is_trial_expired(self) -> bool:
        """Check if trial period has expired."""
        if not self.trial_end:
            return False
        
        return datetime.now(UTC) > self.trial_end
    
    @property
    def days_until_trial_end(self) -> Optional[int]:
        """Get number of days until trial ends."""
        if not self.trial_end:
            return None
        
        now = datetime.now(UTC)
        if now > self.trial_end:
            return 0
        
        delta = self.trial_end - now
        # Use ceiling to ensure we round up partial days
        return max(0, delta.days + (1 if delta.seconds > 0 else 0))
    
    @property
    def is_subscription_active(self) -> bool:
        """Check if subscription is currently active (trial or paid)."""
        return self.status in [SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE]
    
    def start_trial(self, trial_days: int = 7) -> None:
        """Start trial period for specified number of days."""
        now = datetime.now(UTC)
        self.trial_start = now
        self.trial_end = now + timedelta(days=trial_days)
        self.status = SubscriptionStatus.TRIAL
        self.current_period_start = now
        self.current_period_end = self.trial_end
    
    def upgrade_from_trial(self, new_period_end: datetime) -> None:
        """Upgrade subscription from trial to active paid subscription."""
        if self.status != SubscriptionStatus.TRIAL:
            raise ValueError("Can only upgrade from trial status")
        
        self.status = SubscriptionStatus.ACTIVE
        self.current_period_start = datetime.now(UTC)
        self.current_period_end = new_period_end
        self.cancel_at_period_end = False
    
    def cancel_subscription(self, at_period_end: bool = True) -> None:
        """Cancel the subscription."""
        if at_period_end:
            self.cancel_at_period_end = True
        else:
            self.status = SubscriptionStatus.CANCELLED
            self.cancelled_at = datetime.now(UTC)
    
    def expire_subscription(self) -> None:
        """Mark subscription as expired."""
        self.status = SubscriptionStatus.EXPIRED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'status': self.status.value,
            'stripe_subscription_id': self.stripe_subscription_id,
            'trial_start': self.trial_start.isoformat() if self.trial_start else None,
            'trial_end': self.trial_end.isoformat() if self.trial_end else None,
            'current_period_start': self.current_period_start.isoformat() if self.current_period_start else None,
            'current_period_end': self.current_period_end.isoformat() if self.current_period_end else None,
            'cancel_at_period_end': self.cancel_at_period_end,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_trial_active': self.is_trial_active,
            'is_trial_expired': self.is_trial_expired,
            'days_until_trial_end': self.days_until_trial_end,
            'is_subscription_active': self.is_subscription_active
        }


# Default subscription plans
DEFAULT_PLANS = [
    SubscriptionPlan(
        id="trial-7day",
        name="7-Day Trial",
        plan_type=SubscriptionPlanType.TRIAL,
        price_cents=100,  # $1.00
        billing_interval="one_time",
        trial_days=7,
        stripe_price_id=None,  # Set via environment or config
        features={
            "max_entries_per_day": 10,
            "basic_insights": True,
            "ai_analysis": False,
            "export_data": False
        }
    ),
    SubscriptionPlan(
        id="basic-monthly",
        name="Basic Monthly",
        plan_type=SubscriptionPlanType.BASIC,
        price_cents=999,  # $9.99
        billing_interval="monthly",
        trial_days=0,
        stripe_price_id=None,  # Set via environment or config
        features={
            "max_entries_per_day": -1,  # unlimited
            "basic_insights": True,
            "ai_analysis": True,
            "export_data": True,
            "priority_support": False
        }
    ),
    SubscriptionPlan(
        id="pro-monthly",
        name="Pro Monthly",
        plan_type=SubscriptionPlanType.PRO,
        price_cents=1999,  # $19.99
        billing_interval="monthly",
        trial_days=0,
        stripe_price_id=None,  # Set via environment or config
        features={
            "max_entries_per_day": -1,  # unlimited
            "basic_insights": True,
            "ai_analysis": True,
            "advanced_ai_analysis": True,
            "export_data": True,
            "priority_support": True,
            "custom_themes": True
        }
    ),
    SubscriptionPlan(
        id="enterprise-monthly",
        name="Enterprise Monthly",
        plan_type=SubscriptionPlanType.ENTERPRISE,
        price_cents=4999,  # $49.99
        billing_interval="monthly",
        trial_days=0,
        stripe_price_id=None,  # Set via environment or config
        features={
            "max_entries_per_day": -1,  # unlimited
            "basic_insights": True,
            "ai_analysis": True,
            "advanced_ai_analysis": True,
            "export_data": True,
            "priority_support": True,
            "custom_themes": True,
            "team_collaboration": True,
            "advanced_analytics": True,
            "api_access": True
        }
    )
]