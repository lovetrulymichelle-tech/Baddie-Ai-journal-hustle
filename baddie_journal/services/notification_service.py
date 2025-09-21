"""
Notification service for Baddie AI Journal Hustle.

This module handles notifications for trial expiry, upgrade prompts,
subscription status changes, and payment issues.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, UTC, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum

from models.subscription import User, Subscription, SubscriptionStatus

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    """Types of notifications."""
    TRIAL_STARTING = "trial_starting"
    TRIAL_EXPIRING_3_DAYS = "trial_expiring_3_days"
    TRIAL_EXPIRING_1_DAY = "trial_expiring_1_day"
    TRIAL_EXPIRED = "trial_expired"
    UPGRADE_SUCCESSFUL = "upgrade_successful"
    PAYMENT_FAILED = "payment_failed"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    SUBSCRIPTION_REACTIVATED = "subscription_reactivated"


@dataclass
class NotificationTemplate:
    """Template for notification messages."""
    type: NotificationType
    subject: str
    message: str
    action_text: Optional[str] = None
    action_url: Optional[str] = None


class NotificationService:
    """
    Service for managing user notifications related to subscriptions.
    
    Handles email notifications, in-app notifications, and upgrade prompts
    for trial expiry and subscription changes.
    """
    
    def __init__(self, base_url: str = "https://app.baddiejournal.com"):
        """
        Initialize notification service.
        
        Args:
            base_url: Base URL for action links in notifications
        """
        self.base_url = base_url.rstrip('/')
        self.templates = self._load_notification_templates()
        logger.info("Notification service initialized")
    
    def _load_notification_templates(self) -> Dict[NotificationType, NotificationTemplate]:
        """Load notification templates."""
        return {
            NotificationType.TRIAL_STARTING: NotificationTemplate(
                type=NotificationType.TRIAL_STARTING,
                subject="Welcome to Baddie AI Journal! Your 7-Day Trial Has Started 🎉",
                message=(
                    "Hey gorgeous! 💖\n\n"
                    "Welcome to your Baddie AI Journal journey! Your 7-day trial for just $1 is now active.\n\n"
                    "During your trial, you can:\n"
                    "• Create unlimited journal entries\n"
                    "• Get basic insights about your mood and patterns\n" 
                    "• Experience the power of AI-driven self-reflection\n\n"
                    "After 7 days, you'll automatically upgrade to our Basic plan at $9.99/month "
                    "to continue your journaling journey with full features.\n\n"
                    "Ready to start journaling like the baddie you are? Let's go! ✨"
                ),
                action_text="Start Journaling",
                action_url=f"{self.base_url}/dashboard"
            ),
            
            NotificationType.TRIAL_EXPIRING_3_DAYS: NotificationTemplate(
                type=NotificationType.TRIAL_EXPIRING_3_DAYS,
                subject="Your Baddie Trial Expires in 3 Days! ⏰",
                message=(
                    "Hey baddie! 💕\n\n"
                    "Your amazing 7-day trial is almost over - just 3 days left!\n\n"
                    "We hope you're loving the insights and reflection tools. In 3 days, "
                    "you'll automatically upgrade to our Basic plan at $9.99/month to keep:\n\n"
                    "• Unlimited journal entries\n"
                    "• Full AI-powered insights\n"
                    "• Mood tracking and analytics\n"
                    "• Data export capabilities\n\n"
                    "Want to make changes to your subscription? You can manage it anytime."
                ),
                action_text="Manage Subscription", 
                action_url=f"{self.base_url}/subscription"
            ),
            
            NotificationType.TRIAL_EXPIRING_1_DAY: NotificationTemplate(
                type=NotificationType.TRIAL_EXPIRING_1_DAY,
                subject="Last Day of Your Baddie Trial! 🚨",
                message=(
                    "Baddie alert! 🔥\n\n"
                    "Your trial ends tomorrow! We hope these past 6 days have been transformative.\n\n"
                    "Tomorrow you'll automatically upgrade to Basic ($9.99/month) so you can continue:\n"
                    "• Your daily reflection practice\n"
                    "• Getting AI insights about your growth\n" 
                    "• Tracking your mood and patterns\n"
                    "• Building the journaling habit that serves you\n\n"
                    "Need to make changes? Click below to manage your subscription."
                ),
                action_text="Manage Subscription",
                action_url=f"{self.base_url}/subscription"
            ),
            
            NotificationType.TRIAL_EXPIRED: NotificationTemplate(
                type=NotificationType.TRIAL_EXPIRED,
                subject="Welcome to Baddie Basic! Your Journey Continues 🌟",
                message=(
                    "Congratulations, baddie! 🎊\n\n"
                    "You've completed your 7-day trial and we've upgraded you to Baddie Basic!\n\n"
                    "You now have access to:\n"
                    "• Unlimited daily journaling\n"
                    "• Full AI-powered insights and analysis\n"
                    "• Advanced mood tracking\n"
                    "• Export your journal data\n"
                    "• Priority customer support\n\n"
                    "Your subscription is $9.99/month and you can cancel anytime.\n\n"
                    "Keep journaling, keep growing, keep being the baddie you are! ✨"
                ),
                action_text="Continue Journaling",
                action_url=f"{self.base_url}/dashboard"
            ),
            
            NotificationType.UPGRADE_SUCCESSFUL: NotificationTemplate(
                type=NotificationType.UPGRADE_SUCCESSFUL,
                subject="Subscription Upgraded Successfully! 🎉",
                message=(
                    "Amazing news, baddie! ✨\n\n"
                    "Your subscription has been successfully upgraded! You now have access to "
                    "all the premium features to supercharge your journaling journey.\n\n"
                    "Keep being the intentional, self-aware baddie you are! 💪"
                ),
                action_text="Explore Features",
                action_url=f"{self.base_url}/features"
            ),
            
            NotificationType.PAYMENT_FAILED: NotificationTemplate(
                type=NotificationType.PAYMENT_FAILED,
                subject="Payment Issue - Let's Fix This! 💳",
                message=(
                    "Hey baddie! 💕\n\n"
                    "We had trouble processing your payment for Baddie AI Journal. "
                    "Don't worry - this happens sometimes!\n\n"
                    "To keep your journaling streak going, please update your payment method. "
                    "We'll try again automatically.\n\n"
                    "Your growth journey is too important to pause! 🌱"
                ),
                action_text="Update Payment",
                action_url=f"{self.base_url}/payment"
            ),
            
            NotificationType.SUBSCRIPTION_CANCELLED: NotificationTemplate(
                type=NotificationType.SUBSCRIPTION_CANCELLED,
                subject="Sorry to See You Go 💔",
                message=(
                    "Hey gorgeous! 💕\n\n"
                    "We're sad to see you cancel your Baddie AI Journal subscription. "
                    "Your access will continue until your current billing period ends.\n\n"
                    "Remember, your journey of self-reflection and growth doesn't have to stop here. "
                    "You can always come back when you're ready.\n\n"
                    "Keep being amazing, baddie! ✨"
                ),
                action_text="Reactivate Subscription",
                action_url=f"{self.base_url}/reactivate"
            ),
            
            NotificationType.SUBSCRIPTION_REACTIVATED: NotificationTemplate(
                type=NotificationType.SUBSCRIPTION_REACTIVATED,
                subject="Welcome Back, Baddie! 🎉",
                message=(
                    "Yay! Welcome back, baddie! 💖\n\n"
                    "We're so excited to have you back on your journaling journey. "
                    "Your subscription has been reactivated and you have full access to all features again.\n\n"
                    "Let's continue building those amazing habits and insights! ✨"
                ),
                action_text="Start Journaling",
                action_url=f"{self.base_url}/dashboard"
            )
        }
    
    def should_send_trial_notification(self, subscription: Subscription) -> Optional[NotificationType]:
        """
        Check if a trial notification should be sent.
        
        Args:
            subscription: Subscription to check
            
        Returns:
            NotificationType if notification should be sent, None otherwise
        """
        if subscription.status != SubscriptionStatus.TRIAL:
            return None
        
        days_left = subscription.days_until_trial_end
        if days_left is None:
            return None
        
        # Send notifications at specific intervals
        if days_left >= 3 and days_left < 4:
            return NotificationType.TRIAL_EXPIRING_3_DAYS
        elif days_left >= 1 and days_left < 2:
            return NotificationType.TRIAL_EXPIRING_1_DAY
        elif days_left <= 0:
            return NotificationType.TRIAL_EXPIRED
        
        return None
    
    def get_notification_content(self, notification_type: NotificationType) -> NotificationTemplate:
        """
        Get notification content for a specific type.
        
        Args:
            notification_type: Type of notification
            
        Returns:
            NotificationTemplate with content
        """
        return self.templates.get(notification_type)
    
    def send_notification(
        self, 
        user: User, 
        notification_type: NotificationType, 
        additional_context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send notification to user.
        
        Args:
            user: User to send notification to
            notification_type: Type of notification
            additional_context: Additional context for notification
            
        Returns:
            True if notification sent successfully, False otherwise
        """
        template = self.get_notification_content(notification_type)
        if not template:
            logger.error(f"No template found for notification type: {notification_type}")
            return False
        
        # In a real implementation, you would send actual email/SMS/push notifications
        # For now, we'll just log the notification
        logger.info(
            f"Sending {notification_type.value} notification to user {user.id} ({user.email})"
        )
        logger.info(f"Subject: {template.subject}")
        logger.info(f"Message: {template.message[:100]}...")
        
        if template.action_url:
            logger.info(f"Action URL: {template.action_url}")
        
        # Here you would integrate with:
        # - Email service (SendGrid, Mailgun, SES)
        # - SMS service (Twilio)
        # - Push notification service
        # - In-app notification system
        
        return True
    
    def send_trial_starting_notification(self, user: User, subscription: Subscription) -> bool:
        """Send notification when trial starts."""
        return self.send_notification(
            user, 
            NotificationType.TRIAL_STARTING,
            {'subscription_id': subscription.id}
        )
    
    def send_upgrade_notification(self, user: User, subscription: Subscription) -> bool:
        """Send notification when subscription is upgraded."""
        return self.send_notification(
            user,
            NotificationType.UPGRADE_SUCCESSFUL,
            {'subscription_id': subscription.id}
        )
    
    def send_payment_failed_notification(self, user: User, subscription: Subscription) -> bool:
        """Send notification when payment fails."""
        return self.send_notification(
            user,
            NotificationType.PAYMENT_FAILED,
            {'subscription_id': subscription.id}
        )
    
    def send_cancellation_notification(self, user: User, subscription: Subscription) -> bool:
        """Send notification when subscription is cancelled."""
        return self.send_notification(
            user,
            NotificationType.SUBSCRIPTION_CANCELLED,
            {'subscription_id': subscription.id}
        )
    
    def check_and_send_trial_notifications(self, subscriptions: List[Subscription]) -> List[str]:
        """
        Check multiple subscriptions and send appropriate trial notifications.
        
        Args:
            subscriptions: List of subscriptions to check
            
        Returns:
            List of subscription IDs for which notifications were sent
        """
        notifications_sent = []
        
        for subscription in subscriptions:
            notification_type = self.should_send_trial_notification(subscription)
            if notification_type:
                # In a real implementation, you'd get the user from the database
                # For now, we'll just log that a notification should be sent
                logger.info(
                    f"Should send {notification_type.value} notification for subscription {subscription.id}"
                )
                notifications_sent.append(subscription.id)
        
        return notifications_sent