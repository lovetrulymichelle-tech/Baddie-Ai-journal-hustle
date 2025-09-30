#!/usr/bin/env python3
"""
Comprehensive tests for Baddie AI Journal subscription system.

This script tests the subscription models, services, and business logic
including trial periods, upgrades, and payment integration.
"""

import sys
import os
from datetime import datetime, timedelta, timezone
import logging

# Configure logging for tests
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import subscription modules directly to avoid pandas dependency
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "baddie_journal")
)

from models.subscription import (  # noqa: E402
    User,
    Subscription,
    SubscriptionPlan,
    SubscriptionStatus,
    SubscriptionPlanType,
    DEFAULT_PLANS,
)
from services.subscription_service import SubscriptionService  # noqa: E402
from services.notification_service import (
    NotificationService,
    NotificationType,
)  # noqa: E402


def test_subscription_models():
    """Test the subscription models functionality."""
    print("🧪 Testing Subscription Models...")

    # Test SubscriptionPlan
    plan = SubscriptionPlan(
        id="test-plan",
        name="Test Plan",
        plan_type=SubscriptionPlanType.BASIC,
        price_cents=999,
        billing_interval="monthly",
        trial_days=7,
        stripe_price_id="price_test123",
        features={"max_entries": 100},
    )

    assert plan.price_dollars == 9.99
    assert plan.is_active
    plan_dict = plan.to_dict()
    assert plan_dict["price_dollars"] == 9.99
    assert plan_dict["plan_type"] == "basic"
    print("  ✅ SubscriptionPlan creation and serialization")

    # Test User
    user = User(id="user123", email="test@example.com", name="Test User")

    assert user.is_active
    assert user.created_at is not None
    user_dict = user.to_dict()
    assert user_dict["email"] == "test@example.com"
    print("  ✅ User creation and serialization")

    # Test Subscription
    subscription = Subscription(
        id="sub123",
        user_id="user123",
        plan_id="test-plan",
        status=SubscriptionStatus.TRIAL,
    )

    # Test trial functionality
    subscription.start_trial(7)
    assert subscription.is_trial_active
    assert subscription.is_subscription_active
    # Trial end calculation may vary by milliseconds, so check within range
    days_left = subscription.days_until_trial_end
    assert days_left is not None and 6 <= days_left <= 7
    print("  ✅ Subscription trial functionality")

    # Test upgrade functionality
    future_date = datetime.now(timezone.utc) + timedelta(days=30)
    subscription.upgrade_from_trial(future_date)
    assert subscription.status == SubscriptionStatus.ACTIVE
    assert not subscription.is_trial_active
    print("  ✅ Subscription upgrade functionality")

    # Test cancellation
    subscription.cancel_subscription(at_period_end=True)
    assert subscription.cancel_at_period_end
    print("  ✅ Subscription cancellation")

    print("✅ Subscription models tests passed\n")


def test_notification_service():
    """Test the notification service functionality."""
    print("🧪 Testing Notification Service...")

    service = NotificationService()

    # Test template loading
    templates = service.templates
    assert NotificationType.TRIAL_STARTING in templates
    assert NotificationType.TRIAL_EXPIRING_3_DAYS in templates
    assert NotificationType.UPGRADE_SUCCESSFUL in templates
    print("  ✅ Notification templates loaded")

    # Test trial notification logic
    user = User(id="user123", email="test@example.com", name="Test User")

    # Test trial with 3 days left
    trial_start = datetime.now(timezone.utc) - timedelta(days=4)
    trial_end = datetime.now(timezone.utc) + timedelta(days=3)
    subscription = Subscription(
        id="sub123",
        user_id="user123",
        plan_id="trial-7day",
        status=SubscriptionStatus.TRIAL,
        trial_start=trial_start,
        trial_end=trial_end,
    )

    notification_type = service.should_send_trial_notification(subscription)
    print(
        f"  Debug: Days left = {subscription.days_until_trial_end}, Notification = {notification_type}"
    )
    assert notification_type == NotificationType.TRIAL_EXPIRING_3_DAYS
    print("  ✅ Trial expiring notification (3 days)")

    # Test trial with 1 day left
    subscription.trial_end = datetime.now(timezone.utc) + timedelta(days=1)
    notification_type = service.should_send_trial_notification(subscription)
    assert notification_type == NotificationType.TRIAL_EXPIRING_1_DAY
    print("  ✅ Trial expiring notification (1 day)")

    # Test expired trial
    subscription.trial_end = datetime.now(timezone.utc) - timedelta(hours=1)
    notification_type = service.should_send_trial_notification(subscription)
    assert notification_type == NotificationType.TRIAL_EXPIRED
    print("  ✅ Trial expired notification")

    # Test sending notifications
    success = service.send_trial_starting_notification(user, subscription)
    assert success
    print("  ✅ Notification sending")

    print("✅ Notification service tests passed\n")


def test_subscription_service():
    """Test the subscription service functionality."""
    print("🧪 Testing Subscription Service...")

    # Initialize service without Stripe for testing
    notification_service = NotificationService()
    service = SubscriptionService(
        stripe_service=None,  # No Stripe for tests
        notification_service=notification_service,
    )

    # Test plan management
    plans = service.get_available_plans()
    assert len(plans) > 0
    print("  ✅ Plan retrieval")

    trial_plan = service.get_trial_plan()
    assert trial_plan.plan_type == SubscriptionPlanType.TRIAL
    assert trial_plan.trial_days == 7
    print("  ✅ Trial plan retrieval")

    basic_plan = service.get_basic_plan()
    assert basic_plan.plan_type == SubscriptionPlanType.BASIC
    assert basic_plan.price_cents == 999
    print("  ✅ Basic plan retrieval")

    # Test user creation with trial
    result = service.create_user_with_trial(email="test@example.com", name="Test User")

    assert result["success"]
    assert result["user"] is not None
    assert result["subscription"] is not None

    user_data = result["user"]
    subscription_data = result["subscription"]

    assert user_data["email"] == "test@example.com"
    assert subscription_data["status"] == "trial"
    print("  ✅ User creation with trial")

    # Test subscription access checking
    subscription = Subscription(
        id=subscription_data["id"],
        user_id=user_data["id"],
        plan_id=subscription_data["plan_id"],
        status=SubscriptionStatus.TRIAL,
        trial_start=datetime.fromisoformat(subscription_data["trial_start"]),
        trial_end=datetime.fromisoformat(subscription_data["trial_end"]),
    )

    access_info = service.check_subscription_access(subscription)
    assert access_info["has_access"]
    assert access_info["is_trial"]
    assert not access_info["needs_upgrade"]
    print("  ✅ Subscription access checking")

    # Test expired trial upgrade
    subscription.trial_end = datetime.now(timezone.utc) - timedelta(hours=1)
    access_info = service.check_subscription_access(subscription)
    assert access_info["needs_upgrade"]

    upgrade_result = service.upgrade_trial_to_paid(subscription)
    assert upgrade_result["success"]
    assert subscription.status == SubscriptionStatus.ACTIVE
    print("  ✅ Trial to paid upgrade")

    # Test subscription cancellation
    cancel_result = service.cancel_subscription(subscription, at_period_end=True)
    assert cancel_result["success"]
    assert subscription.cancel_at_period_end
    print("  ✅ Subscription cancellation")

    print("✅ Subscription service tests passed\n")


def test_default_plans():
    """Test the default subscription plans."""
    print("🧪 Testing Default Plans...")

    assert len(DEFAULT_PLANS) == 4

    # Check trial plan
    trial_plan = next((p for p in DEFAULT_PLANS if p.id == "trial-7day"), None)
    assert trial_plan is not None
    assert trial_plan.price_cents == 100  # $1.00
    assert trial_plan.trial_days == 7
    print("  ✅ Trial plan configuration")

    # Check basic plan
    basic_plan = next((p for p in DEFAULT_PLANS if p.id == "basic-monthly"), None)
    assert basic_plan is not None
    assert basic_plan.price_cents == 999  # $9.99
    assert basic_plan.billing_interval == "monthly"
    print("  ✅ Basic plan configuration")

    # Check pro plan
    pro_plan = next((p for p in DEFAULT_PLANS if p.id == "pro-monthly"), None)
    assert pro_plan is not None
    assert pro_plan.price_cents == 1999  # $19.99
    assert "advanced_ai_analysis" in pro_plan.features
    print("  ✅ Pro plan configuration")

    # Check enterprise plan
    enterprise_plan = next(
        (p for p in DEFAULT_PLANS if p.id == "enterprise-monthly"), None
    )
    assert enterprise_plan is not None
    assert enterprise_plan.price_cents == 4999  # $49.99
    assert "api_access" in enterprise_plan.features
    print("  ✅ Enterprise plan configuration")

    print("✅ Default plans tests passed\n")


def test_trial_workflow():
    """Test the complete trial workflow."""
    print("🧪 Testing Complete Trial Workflow...")

    service = SubscriptionService()

    # Step 1: Create user with trial
    result = service.create_user_with_trial(
        email="workflow@example.com", name="Workflow Test User"
    )
    assert result["success"]

    user_data = result["user"]
    subscription_data = result["subscription"]
    print("  ✅ Step 1: User created with trial")

    # Step 2: Check trial is active
    subscription = Subscription(
        id=subscription_data["id"],
        user_id=user_data["id"],
        plan_id=subscription_data["plan_id"],
        status=SubscriptionStatus.TRIAL,
        trial_start=datetime.fromisoformat(subscription_data["trial_start"]),
        trial_end=datetime.fromisoformat(subscription_data["trial_end"]),
    )

    access = service.check_subscription_access(subscription)
    assert access["has_access"]
    assert access["is_trial"]
    print("  ✅ Step 2: Trial is active and accessible")

    # Step 3: Simulate trial expiration
    subscription.trial_end = datetime.now(timezone.utc) - timedelta(hours=1)

    access = service.check_subscription_access(subscription)
    assert access["needs_upgrade"]
    print("  ✅ Step 3: Trial expiration detected")

    # Step 4: Automatic upgrade
    upgrade_result = service.upgrade_trial_to_paid(subscription)
    assert upgrade_result["success"]
    assert subscription.status == SubscriptionStatus.ACTIVE
    print("  ✅ Step 4: Automatic upgrade to paid")

    # Step 5: Check ongoing access
    access = service.check_subscription_access(subscription)
    assert access["has_access"]
    assert not access["is_trial"]
    assert not access["needs_upgrade"]
    print("  ✅ Step 5: Paid subscription active")

    print("✅ Complete trial workflow tests passed\n")


def main():
    """Run all subscription tests."""
    print("🚀 Running Baddie AI Journal Subscription Tests\n")

    try:
        test_subscription_models()
        test_notification_service()
        test_subscription_service()
        test_default_plans()
        test_trial_workflow()

        print(
            "🎉 All subscription tests passed! Subscription system is working correctly."
        )
        print("\n📋 Test Summary:")
        print("  ✅ Subscription models (User, Subscription, SubscriptionPlan)")
        print("  ✅ Notification service (trial expiry, upgrade notifications)")
        print("  ✅ Subscription service (trial creation, upgrades, cancellation)")
        print("  ✅ Default plans configuration ($1 trial, $9.99 basic, tiered plans)")
        print("  ✅ Complete trial workflow (signup → trial → auto-upgrade)")
        print("\n🔧 Ready for Stripe integration with environment variables:")
        print("  • STRIPE_SECRET_KEY - Your Stripe secret key")
        print("  • STRIPE_WEBHOOK_SECRET - Your webhook endpoint secret")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
