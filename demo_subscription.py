#!/usr/bin/env python3
"""
Demo script for Baddie AI Journal subscription system.

This script demonstrates the complete subscription workflow including:
- User signup with trial
- Trial period management
- Automatic upgrade to paid subscription
- Stripe integration capabilities
- Notification system
"""

import os
import sys
from datetime import datetime, UTC, timedelta

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import subscription modules directly to avoid dependency issues
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "baddie_journal")
)

from models.subscription import (  # noqa: E402
    Subscription,
    SubscriptionStatus,
    DEFAULT_PLANS,
)
from services.subscription_service import SubscriptionService  # noqa: E402
from services.notification_service import NotificationService  # noqa: E402


def demonstrate_subscription_plans():
    """Demonstrate available subscription plans."""
    print("💰 SUBSCRIPTION PLANS")
    print("=" * 50)

    for plan in DEFAULT_PLANS:
        print(f"\n📋 {plan.name}")
        print(f"   Price: ${plan.price_dollars:.2f}/{plan.billing_interval}")
        print(
            f"   Trial: {plan.trial_days} days"
            if plan.trial_days > 0
            else "   No trial"
        )
        print(f"   Type: {plan.plan_type.value}")

        # Show key features
        features = plan.features
        print("   Features:")
        for feature, value in features.items():
            if isinstance(value, bool):
                status = "✅" if value else "❌"
                print(f"     {status} {feature.replace('_', ' ').title()}")
            elif feature == "max_entries_per_day":
                if value == -1:
                    print("     ✅ Unlimited entries per day")
                else:
                    print(f"     📊 {value} entries per day")

    print("\n" + "=" * 50)


def demonstrate_user_signup():
    """Demonstrate user signup with trial."""
    print("\n👤 USER SIGNUP WITH TRIAL")
    print("=" * 50)

    # Initialize services
    notification_service = NotificationService()
    subscription_service = SubscriptionService(
        stripe_service=None,  # No Stripe for demo
        notification_service=notification_service,
    )

    # Create user with trial
    print("🔄 Creating new user with 7-day trial...")
    result = subscription_service.create_user_with_trial(
        email="baddie@example.com", name="Amazing Baddie"
    )

    if result["success"]:
        user_data = result["user"]
        subscription_data = result["subscription"]

        print("✅ User created successfully!")
        print(f"   User ID: {user_data['id']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Name: {user_data['name']}")
        print(f"   Created: {user_data['created_at']}")

        print("\n📅 Trial Subscription:")
        print(f"   Subscription ID: {subscription_data['id']}")
        print(f"   Status: {subscription_data['status']}")
        print(f"   Trial Start: {subscription_data['trial_start']}")
        print(f"   Trial End: {subscription_data['trial_end']}")
        print(f"   Days Left: {subscription_data['days_until_trial_end']}")

        return subscription_data
    else:
        print(f"❌ Failed to create user: {result['error']}")
        return None


def demonstrate_trial_management(subscription_data):
    """Demonstrate trial period management."""
    print("\n⏰ TRIAL MANAGEMENT")
    print("=" * 50)

    subscription_service = SubscriptionService()

    # Recreate subscription object
    subscription = Subscription(
        id=subscription_data["id"],
        user_id=subscription_data["user_id"],
        plan_id=subscription_data["plan_id"],
        status=SubscriptionStatus.TRIAL,
        trial_start=datetime.fromisoformat(subscription_data["trial_start"]),
        trial_end=datetime.fromisoformat(subscription_data["trial_end"]),
    )

    print("🔍 Checking subscription access...")
    access_info = subscription_service.check_subscription_access(subscription)

    print(f"   Has Access: {'✅' if access_info['has_access'] else '❌'}")
    print(f"   Is Trial: {'✅' if access_info['is_trial'] else '❌'}")
    print(f"   Needs Upgrade: {'⚠️' if access_info['needs_upgrade'] else '✅'}")
    print(f"   Plan: {access_info['plan_name']}")
    print(f"   Days Left: {access_info['trial_days_left']}")

    # Simulate different trial stages
    print("\n📅 Simulating trial progression...")

    # 3 days left
    subscription.trial_end = datetime.now(UTC) + timedelta(days=3)
    notification_service = NotificationService()
    notification_type = notification_service.should_send_trial_notification(
        subscription
    )
    if notification_type:
        print(f"   🔔 Notification: {notification_type.value}")

    # 1 day left
    subscription.trial_end = datetime.now(UTC) + timedelta(days=1)
    notification_type = notification_service.should_send_trial_notification(
        subscription
    )
    if notification_type:
        print(f"   🔔 Notification: {notification_type.value}")

    # Expired
    subscription.trial_end = datetime.now(UTC) - timedelta(hours=1)
    notification_type = notification_service.should_send_trial_notification(
        subscription
    )
    if notification_type:
        print(f"   🔔 Notification: {notification_type.value}")

    return subscription


def demonstrate_subscription_upgrade(subscription):
    """Demonstrate automatic upgrade from trial to paid."""
    print("\n⬆️ SUBSCRIPTION UPGRADE")
    print("=" * 50)

    subscription_service = SubscriptionService()

    print("🔄 Upgrading expired trial to paid subscription...")

    try:
        result = subscription_service.upgrade_trial_to_paid(subscription)

        if result["success"]:
            print("✅ Upgrade successful!")
            print(f"   New Status: {subscription.status.value}")
            print(f"   Plan: {result['upgraded_to_plan']['name']}")
            print(f"   Price: ${result['upgraded_to_plan']['price_dollars']:.2f}/month")
            print(f"   Period End: {subscription.current_period_end}")

            # Check access after upgrade
            access_info = subscription_service.check_subscription_access(subscription)
            print("\n📊 Post-upgrade access:")
            print(f"   Has Access: {'✅' if access_info['has_access'] else '❌'}")
            print(f"   Is Trial: {'❌' if not access_info['is_trial'] else '✅'}")
            print(
                f"   Needs Upgrade: {'❌' if not access_info['needs_upgrade'] else '⚠️'}"
            )

        else:
            print(f"❌ Upgrade failed: {result['error']}")

    except Exception as e:
        print(f"❌ Upgrade error: {str(e)}")

    return subscription


def demonstrate_stripe_integration():
    """Demonstrate Stripe integration capabilities."""
    print("\n💳 STRIPE INTEGRATION")
    print("=" * 50)

    # Check if Stripe is available
    try:
        import stripe  # noqa: F401

        stripe_available = True
    except ImportError:
        stripe_available = False

    if not stripe_available:
        print("⚠️  Stripe package not installed")
        print("   Install with: pip install stripe")
        print("   This demo shows integration capabilities without actual Stripe calls")

    # Check environment variables
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    print("\n🔧 Environment Configuration:")
    print(f"   Stripe Key: {'✅ Set' if stripe_key else '❌ Not set'}")
    print(f"   Webhook Secret: {'✅ Set' if webhook_secret else '❌ Not set'}")

    if stripe_available and stripe_key:
        print("\n🚀 Stripe service can be initialized!")
        print("   Features available:")
        print("   • Customer creation")
        print("   • Trial subscription with $1 charge")
        print("   • Automatic upgrade to $9.99/month")
        print("   • Webhook handling for subscription events")
        print("   • Payment failure notifications")
        print("   • Subscription cancellation")
    else:
        print("\n📋 To enable Stripe integration:")
        print("   1. Install Stripe: pip install stripe")
        print("   2. Set environment variables:")
        print("      export STRIPE_SECRET_KEY='sk_test_...'")
        print("      export STRIPE_WEBHOOK_SECRET='whsec_...'")
        print("   3. Configure webhook endpoints in Stripe dashboard")


def demonstrate_notification_system():
    """Demonstrate the notification system."""
    print("\n📢 NOTIFICATION SYSTEM")
    print("=" * 50)

    notification_service = NotificationService()

    print("📧 Available notification templates:")

    templates = [
        ("Trial Starting", "Welcome message with trial details"),
        ("Trial Expiring (3 days)", "Reminder about upcoming upgrade"),
        ("Trial Expiring (1 day)", "Final reminder before upgrade"),
        ("Trial Expired", "Welcome to paid subscription"),
        ("Upgrade Successful", "Confirmation of plan upgrade"),
        ("Payment Failed", "Payment issue notification"),
        ("Subscription Cancelled", "Cancellation confirmation"),
        ("Subscription Reactivated", "Welcome back message"),
    ]

    for name, description in templates:
        print(f"   ✉️  {name}: {description}")

    print("\n🎨 Notification features:")
    print("   • Personalized messaging with 'baddie' branding")
    print("   • Action buttons for subscription management")
    print("   • Contextual timing based on subscription status")
    print("   • Support for email, SMS, and in-app notifications")

    # Show sample notification
    print("\n📝 Sample notification (Trial Expiring):")
    print("-" * 40)
    from services.notification_service import NotificationType

    template = notification_service.get_notification_content(
        NotificationType.TRIAL_EXPIRING_3_DAYS
    )

    print(f"Subject: {template.subject}")
    print(f"\nMessage:\n{template.message[:200]}...")
    if template.action_text:
        print(f"\nAction: [{template.action_text}] → {template.action_url}")


def main():
    """Run the complete subscription demo."""
    print("🚀 Baddie AI Journal Subscription System Demo")
    print("=" * 60)

    try:
        # Step 1: Show available plans
        demonstrate_subscription_plans()

        # Step 2: User signup with trial
        subscription_data = demonstrate_user_signup()
        if not subscription_data:
            return False

        # Step 3: Trial management
        subscription = demonstrate_trial_management(subscription_data)

        # Step 4: Automatic upgrade
        demonstrate_subscription_upgrade(subscription)

        # Step 5: Stripe integration
        demonstrate_stripe_integration()

        # Step 6: Notification system
        demonstrate_notification_system()

        print("\n🎉 Demo completed successfully!")
        print("\n📋 Subscription System Features:")
        print("   ✅ $1 seven-day trial period")
        print("   ✅ Automatic upgrade to $9.99/month")
        print("   ✅ Tiered plans (Basic, Pro, Enterprise)")
        print("   ✅ Stripe payment integration")
        print("   ✅ Trial expiry notifications")
        print("   ✅ Subscription management")
        print("   ✅ Webhook handling")
        print("   ✅ Cancellation support")

        print("\n🔧 Next steps:")
        print("   1. Set up Stripe account and get API keys")
        print("   2. Configure webhook endpoints")
        print("   3. Integrate with your web application")
        print("   4. Set up email/notification service")
        print("   5. Add database persistence layer")

        return True

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
