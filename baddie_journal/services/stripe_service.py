"""
Stripe payment service for Baddie AI Journal Hustle.

This module provides integration with Stripe for subscription management,
trial billing, and webhook handling.
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime, UTC, timedelta
import logging

try:
    import stripe
except ImportError:
    stripe = None

from models.subscription import User, Subscription, SubscriptionPlan, SubscriptionStatus

logger = logging.getLogger(__name__)


class StripeError(Exception):
    """Custom exception for Stripe-related errors."""

    pass


class StripeService:
    """
    Service for managing Stripe payment operations.

    Handles subscription creation, trial billing, upgrades, cancellations,
    and webhook event processing.
    """

    def __init__(
        self, api_key: Optional[str] = None, webhook_secret: Optional[str] = None
    ):
        """
        Initialize Stripe service.

        Args:
            api_key: Stripe secret API key (defaults to STRIPE_SECRET_KEY env var)
            webhook_secret: Stripe webhook endpoint secret (defaults to STRIPE_WEBHOOK_SECRET env var)
        """
        if stripe is None:
            raise ImportError(
                "Stripe package not installed. Install with: pip install stripe"
            )

        self.api_key = api_key or os.getenv("STRIPE_SECRET_KEY")
        self.webhook_secret = webhook_secret or os.getenv("STRIPE_WEBHOOK_SECRET")

        if not self.api_key:
            raise ValueError(
                "Stripe API key is required. Set STRIPE_SECRET_KEY environment variable."
            )

        stripe.api_key = self.api_key
        logger.info("Stripe service initialized")

    def create_customer(self, user: User) -> str:
        """
        Create a Stripe customer for the user.

        Args:
            user: User object to create customer for

        Returns:
            Stripe customer ID
        """
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.name,
                metadata={"user_id": user.id, "created_via": "baddie_journal"},
            )
            logger.info(f"Created Stripe customer {customer.id} for user {user.id}")
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(
                f"Failed to create Stripe customer for user {user.id}: {str(e)}"
            )
            raise StripeError(f"Failed to create customer: {str(e)}")

    def create_trial_subscription(
        self, customer_id: str, plan: SubscriptionPlan, trial_days: int = 7
    ) -> Dict[str, Any]:
        """
        Create a trial subscription with $1 charge.

        Args:
            customer_id: Stripe customer ID
            plan: Subscription plan for after trial
            trial_days: Number of trial days (default: 7)

        Returns:
            Dictionary with subscription data
        """
        try:
            # Create the trial subscription
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"{plan.name} - 7-Day Trial",
                                "description": f"$1 trial period, then ${plan.price_dollars}/month",
                            },
                            "unit_amount": 100,  # $1.00 in cents
                            "recurring": {"interval": "month"},
                        }
                    }
                ],
                trial_period_days=trial_days,
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.payment_intent"],
                metadata={
                    "plan_id": plan.id,
                    "trial_amount_cents": "100",
                    "regular_amount_cents": str(plan.price_cents),
                },
            )

            logger.info(
                f"Created trial subscription {subscription.id} for customer {customer_id}"
            )

            return {
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret,
                "status": subscription.status,
                "trial_start": datetime.fromtimestamp(subscription.trial_start, tz=UTC),
                "trial_end": datetime.fromtimestamp(subscription.trial_end, tz=UTC),
                "current_period_start": datetime.fromtimestamp(
                    subscription.current_period_start, tz=UTC
                ),
                "current_period_end": datetime.fromtimestamp(
                    subscription.current_period_end, tz=UTC
                ),
            }

        except stripe.error.StripeError as e:
            logger.error(
                f"Failed to create trial subscription for customer {customer_id}: {str(e)}"
            )
            raise StripeError(f"Failed to create trial subscription: {str(e)}")

    def upgrade_subscription_after_trial(
        self, subscription_id: str, new_plan: SubscriptionPlan
    ) -> Dict[str, Any]:
        """
        Upgrade subscription from trial to paid plan.

        Args:
            subscription_id: Stripe subscription ID
            new_plan: New subscription plan

        Returns:
            Updated subscription data
        """
        try:
            # Update the subscription to the new plan price
            subscription = stripe.Subscription.modify(
                subscription_id,
                items=[
                    {
                        "id": stripe.Subscription.retrieve(subscription_id)
                        .items.data[0]
                        .id,
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": new_plan.name,
                                "description": f"${new_plan.price_dollars}/{new_plan.billing_interval}",
                            },
                            "unit_amount": new_plan.price_cents,
                            "recurring": {"interval": new_plan.billing_interval},
                        },
                    }
                ],
                proration_behavior="none",
                metadata={
                    "plan_id": new_plan.id,
                    "upgraded_from_trial": "true",
                    "upgrade_timestamp": str(int(datetime.now(UTC).timestamp())),
                },
            )

            logger.info(
                f"Upgraded subscription {subscription_id} to plan {new_plan.id}"
            )

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_start": datetime.fromtimestamp(
                    subscription.current_period_start, tz=UTC
                ),
                "current_period_end": datetime.fromtimestamp(
                    subscription.current_period_end, tz=UTC
                ),
            }

        except stripe.error.StripeError as e:
            logger.error(f"Failed to upgrade subscription {subscription_id}: {str(e)}")
            raise StripeError(f"Failed to upgrade subscription: {str(e)}")

    def cancel_subscription(
        self, subscription_id: str, at_period_end: bool = True
    ) -> Dict[str, Any]:
        """
        Cancel a Stripe subscription.

        Args:
            subscription_id: Stripe subscription ID
            at_period_end: Whether to cancel at period end (default: True)

        Returns:
            Cancelled subscription data
        """
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id, cancel_at_period_end=True
                )
                logger.info(
                    f"Scheduled subscription {subscription_id} for cancellation at period end"
                )
            else:
                subscription = stripe.Subscription.cancel(subscription_id)
                logger.info(f"Immediately cancelled subscription {subscription_id}")

            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "cancelled_at": (
                    datetime.fromtimestamp(subscription.canceled_at, tz=UTC)
                    if subscription.canceled_at
                    else None
                ),
                "current_period_end": datetime.fromtimestamp(
                    subscription.current_period_end, tz=UTC
                ),
            }

        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel subscription {subscription_id}: {str(e)}")
            raise StripeError(f"Failed to cancel subscription: {str(e)}")

    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Retrieve subscription details from Stripe.

        Args:
            subscription_id: Stripe subscription ID

        Returns:
            Subscription data
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)

            return {
                "subscription_id": subscription.id,
                "customer_id": subscription.customer,
                "status": subscription.status,
                "trial_start": (
                    datetime.fromtimestamp(subscription.trial_start, tz=UTC)
                    if subscription.trial_start
                    else None
                ),
                "trial_end": (
                    datetime.fromtimestamp(subscription.trial_end, tz=UTC)
                    if subscription.trial_end
                    else None
                ),
                "current_period_start": datetime.fromtimestamp(
                    subscription.current_period_start, tz=UTC
                ),
                "current_period_end": datetime.fromtimestamp(
                    subscription.current_period_end, tz=UTC
                ),
                "cancel_at_period_end": subscription.cancel_at_period_end,
                "cancelled_at": (
                    datetime.fromtimestamp(subscription.canceled_at, tz=UTC)
                    if subscription.canceled_at
                    else None
                ),
            }

        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve subscription {subscription_id}: {str(e)}")
            raise StripeError(f"Failed to retrieve subscription: {str(e)}")

    def handle_webhook_event(
        self, payload: str, signature: str
    ) -> Optional[Dict[str, Any]]:
        """
        Handle Stripe webhook events.

        Args:
            payload: Webhook payload
            signature: Stripe signature header

        Returns:
            Event data if handled, None otherwise
        """
        if not self.webhook_secret:
            logger.warning(
                "Webhook secret not configured, skipping signature verification"
            )
            return None

        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
        except ValueError as e:
            logger.error(f"Invalid webhook payload: {e}")
            raise StripeError(f"Invalid payload: {e}")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid webhook signature: {e}")
            raise StripeError(f"Invalid signature: {e}")

        event_type = event["type"]
        event_data = event["data"]["object"]

        logger.info(f"Received Stripe webhook event: {event_type}")

        # Handle specific events
        if event_type == "invoice.payment_succeeded":
            return self._handle_payment_succeeded(event_data)
        elif event_type == "invoice.payment_failed":
            return self._handle_payment_failed(event_data)
        elif event_type == "customer.subscription.updated":
            return self._handle_subscription_updated(event_data)
        elif event_type == "customer.subscription.deleted":
            return self._handle_subscription_deleted(event_data)
        elif event_type == "customer.subscription.trial_will_end":
            return self._handle_trial_will_end(event_data)

        logger.info(f"Unhandled webhook event type: {event_type}")
        return None

    def _handle_payment_succeeded(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful payment webhook."""
        subscription_id = event_data.get("subscription")

        return {
            "event_type": "payment_succeeded",
            "subscription_id": subscription_id,
            "amount_paid": event_data.get("amount_paid", 0),
            "timestamp": datetime.fromtimestamp(event_data.get("created", 0), tz=UTC),
        }

    def _handle_payment_failed(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle failed payment webhook."""
        subscription_id = event_data.get("subscription")

        return {
            "event_type": "payment_failed",
            "subscription_id": subscription_id,
            "amount_due": event_data.get("amount_due", 0),
            "timestamp": datetime.fromtimestamp(event_data.get("created", 0), tz=UTC),
        }

    def _handle_subscription_updated(
        self, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle subscription updated webhook."""
        subscription_id = event_data.get("id")

        return {
            "event_type": "subscription_updated",
            "subscription_id": subscription_id,
            "status": event_data.get("status"),
            "cancel_at_period_end": event_data.get("cancel_at_period_end"),
            "current_period_end": datetime.fromtimestamp(
                event_data.get("current_period_end", 0), tz=UTC
            ),
            "timestamp": datetime.now(UTC),
        }

    def _handle_subscription_deleted(
        self, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle subscription deleted webhook."""
        subscription_id = event_data.get("id")

        return {
            "event_type": "subscription_deleted",
            "subscription_id": subscription_id,
            "cancelled_at": datetime.fromtimestamp(
                event_data.get("canceled_at", 0), tz=UTC
            ),
            "timestamp": datetime.now(UTC),
        }

    def _handle_trial_will_end(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle trial ending soon webhook."""
        subscription_id = event_data.get("id")
        trial_end = event_data.get("trial_end")

        return {
            "event_type": "trial_will_end",
            "subscription_id": subscription_id,
            "trial_end": (
                datetime.fromtimestamp(trial_end, tz=UTC) if trial_end else None
            ),
            "timestamp": datetime.now(UTC),
        }
