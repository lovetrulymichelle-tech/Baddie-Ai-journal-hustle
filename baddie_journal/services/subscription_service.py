"""
Core subscription service for Baddie AI Journal Hustle.

This module provides the main business logic for managing subscriptions,
trials, upgrades, and subscription lifecycle events.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
import uuid

from models.subscription import (
    User,
    Subscription,
    SubscriptionPlan,
    SubscriptionStatus,
    DEFAULT_PLANS,
)
from services.stripe_service import StripeService, StripeError
from services.notification_service import NotificationService

logger = logging.getLogger(__name__)


class SubscriptionError(Exception):
    """Custom exception for subscription-related errors."""

    pass


class SubscriptionService:
    """
    Core service for managing user subscriptions.

    Handles trial creation, upgrades, cancellations, and subscription
    lifecycle management with Stripe integration.
    """

    def __init__(
        self,
        stripe_service: Optional[StripeService] = None,
        notification_service: Optional[NotificationService] = None,
    ):
        """
        Initialize subscription service.

        Args:
            stripe_service: Stripe service instance
            notification_service: Notification service instance
        """
        self.stripe_service = stripe_service
        self.notification_service = notification_service
        self.plans = {plan.id: plan for plan in DEFAULT_PLANS}
        logger.info("Subscription service initialized")

    def get_available_plans(self) -> List[SubscriptionPlan]:
        """Get all available subscription plans."""
        return [plan for plan in self.plans.values() if plan.is_active]

    def get_plan_by_id(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """Get subscription plan by ID."""
        return self.plans.get(plan_id)

    def get_trial_plan(self) -> SubscriptionPlan:
        """Get the trial plan."""
        trial_plan = self.get_plan_by_id("trial-7day")
        if not trial_plan:
            raise SubscriptionError("Trial plan not found")
        return trial_plan

    def get_basic_plan(self) -> SubscriptionPlan:
        """Get the basic monthly plan."""
        basic_plan = self.get_plan_by_id("basic-monthly")
        if not basic_plan:
            raise SubscriptionError("Basic plan not found")
        return basic_plan

    def create_user_with_trial(
        self, email: str, name: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new user and start their trial subscription.

        Args:
            email: User's email address
            name: User's display name
            user_id: Optional user ID (generated if not provided)

        Returns:
            Dictionary with user and subscription data
        """
        if not user_id:
            user_id = str(uuid.uuid4())

        # Create user
        user = User(id=user_id, email=email, name=name)

        try:
            # Create Stripe customer if Stripe service is available
            if self.stripe_service:
                stripe_customer_id = self.stripe_service.create_customer(user)
                user.stripe_customer_id = stripe_customer_id

            # Create trial subscription
            subscription = self.create_trial_subscription(user)
            user.current_subscription_id = subscription.id

            # Send welcome notification
            if self.notification_service:
                self.notification_service.send_trial_starting_notification(
                    user, subscription
                )

            logger.info(
                f"Created user {user.id} with trial subscription {subscription.id}"
            )

            return {
                "user": user.to_dict(),
                "subscription": subscription.to_dict(),
                "success": True,
            }

        except (StripeError, SubscriptionError) as e:
            logger.error(f"Failed to create user with trial: {str(e)}")
            return {
                "user": None,
                "subscription": None,
                "success": False,
                "error": str(e),
            }

    def create_trial_subscription(self, user: User) -> Subscription:
        """
        Create a trial subscription for a user.

        Args:
            user: User to create subscription for

        Returns:
            Created subscription
        """
        trial_plan = self.get_trial_plan()
        subscription_id = str(uuid.uuid4())

        # Create subscription
        subscription = Subscription(
            id=subscription_id,
            user_id=user.id,
            plan_id=trial_plan.id,
            status=SubscriptionStatus.TRIAL,
        )

        # Start trial period
        subscription.start_trial(trial_plan.trial_days)

        # Create Stripe subscription if service is available
        if self.stripe_service and user.stripe_customer_id:
            try:
                stripe_data = self.stripe_service.create_trial_subscription(
                    user.stripe_customer_id,
                    self.get_basic_plan(),  # Plan to upgrade to after trial
                    trial_plan.trial_days,
                )
                subscription.stripe_subscription_id = stripe_data["subscription_id"]

                logger.info(
                    f"Created Stripe trial subscription {stripe_data['subscription_id']}"
                )

            except StripeError as e:
                logger.error(f"Failed to create Stripe subscription: {str(e)}")
                # Continue with local subscription even if Stripe fails

        return subscription

    def upgrade_trial_to_paid(self, subscription: Subscription) -> Dict[str, Any]:
        """
        Upgrade a trial subscription to paid subscription.

        Args:
            subscription: Trial subscription to upgrade

        Returns:
            Dictionary with upgrade result
        """
        if subscription.status != SubscriptionStatus.TRIAL:
            raise SubscriptionError("Can only upgrade trial subscriptions")

        if not subscription.is_trial_expired:
            raise SubscriptionError("Trial has not expired yet")

        basic_plan = self.get_basic_plan()

        try:
            # Upgrade in Stripe if available
            if self.stripe_service and subscription.stripe_subscription_id:
                stripe_data = self.stripe_service.upgrade_subscription_after_trial(
                    subscription.stripe_subscription_id, basic_plan
                )

                # Update subscription with new billing period
                subscription.upgrade_from_trial(stripe_data["current_period_end"])
            else:
                # Upgrade locally without Stripe
                new_period_end = datetime.now(timezone.utc) + timedelta(
                    days=30
                )  # 30 days from now
                subscription.upgrade_from_trial(new_period_end)

            # Update plan ID
            subscription.plan_id = basic_plan.id

            logger.info(
                f"Upgraded subscription {subscription.id} from trial to {basic_plan.id}"
            )

            return {
                "subscription": subscription.to_dict(),
                "success": True,
                "upgraded_to_plan": basic_plan.to_dict(),
            }

        except StripeError as e:
            logger.error(f"Failed to upgrade subscription {subscription.id}: {str(e)}")
            return {
                "subscription": subscription.to_dict(),
                "success": False,
                "error": str(e),
            }

    def cancel_subscription(
        self, subscription: Subscription, at_period_end: bool = True
    ) -> Dict[str, Any]:
        """
        Cancel a subscription.

        Args:
            subscription: Subscription to cancel
            at_period_end: Whether to cancel at period end

        Returns:
            Dictionary with cancellation result
        """
        try:
            # Cancel in Stripe if available
            if self.stripe_service and subscription.stripe_subscription_id:
                self.stripe_service.cancel_subscription(
                    subscription.stripe_subscription_id, at_period_end
                )

            # Update local subscription
            subscription.cancel_subscription(at_period_end)

            logger.info(f"Cancelled subscription {subscription.id}")

            return {
                "subscription": subscription.to_dict(),
                "success": True,
                "cancelled_at_period_end": at_period_end,
            }

        except StripeError as e:
            logger.error(f"Failed to cancel subscription {subscription.id}: {str(e)}")
            return {
                "subscription": subscription.to_dict(),
                "success": False,
                "error": str(e),
            }

    def check_subscription_access(self, subscription: Subscription) -> Dict[str, Any]:
        """
        Check if subscription provides access to features.

        Args:
            subscription: Subscription to check

        Returns:
            Dictionary with access information
        """
        has_access = subscription.is_subscription_active

        # Check if trial has expired and needs upgrade
        needs_upgrade = (
            subscription.status == SubscriptionStatus.TRIAL
            and subscription.is_trial_expired
        )

        # Get plan features
        plan = self.get_plan_by_id(subscription.plan_id)
        features = plan.features if plan else {}

        return {
            "has_access": has_access,
            "needs_upgrade": needs_upgrade,
            "subscription_status": subscription.status.value,
            "is_trial": subscription.status == SubscriptionStatus.TRIAL,
            "trial_days_left": subscription.days_until_trial_end,
            "features": features,
            "plan_name": plan.name if plan else "Unknown",
        }

    def process_trial_expirations(self, subscriptions: List[Subscription]) -> List[str]:
        """
        Process trial subscriptions that have expired.

        Args:
            subscriptions: List of subscriptions to check

        Returns:
            List of subscription IDs that were upgraded
        """
        upgraded_subscriptions = []

        for subscription in subscriptions:
            if (
                subscription.status == SubscriptionStatus.TRIAL
                and subscription.is_trial_expired
            ):

                try:
                    result = self.upgrade_trial_to_paid(subscription)
                    if result["success"]:
                        upgraded_subscriptions.append(subscription.id)

                        # Send upgrade notification
                        if self.notification_service:
                            # In a real implementation, you'd get the user from the database
                            logger.info(
                                f"Should send upgrade notification for subscription {subscription.id}"
                            )

                except SubscriptionError as e:
                    logger.error(
                        f"Failed to upgrade expired trial {subscription.id}: {str(e)}"
                    )

        return upgraded_subscriptions

    def handle_stripe_webhook(self, event_data: Dict[str, Any]) -> bool:
        """
        Handle Stripe webhook events.

        Args:
            event_data: Webhook event data from Stripe service

        Returns:
            True if event was handled successfully
        """
        event_type = event_data.get("event_type")
        subscription_id = event_data.get("subscription_id")

        if not subscription_id:
            logger.warning(f"No subscription ID in webhook event: {event_type}")
            return False

        logger.info(
            f"Processing webhook event {event_type} for subscription {subscription_id}"
        )

        # In a real implementation, you would:
        # 1. Look up the subscription in your database
        # 2. Update the subscription status based on the event
        # 3. Send notifications as needed

        if event_type == "payment_succeeded":
            logger.info(f"Payment succeeded for subscription {subscription_id}")
            return True

        elif event_type == "payment_failed":
            logger.info(f"Payment failed for subscription {subscription_id}")
            # Send payment failed notification
            return True

        elif event_type == "subscription_updated":
            logger.info(f"Subscription updated: {subscription_id}")
            return True

        elif event_type == "subscription_deleted":
            logger.info(f"Subscription deleted: {subscription_id}")
            return True

        elif event_type == "trial_will_end":
            logger.info(f"Trial ending soon for subscription {subscription_id}")
            # Send trial ending notification
            return True

        logger.warning(f"Unhandled webhook event type: {event_type}")
        return False
