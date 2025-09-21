# Subscription System Implementation

This document describes the backend subscription logic implementation for Baddie AI Journal.

## Overview

The subscription system supports a **$1 seven-day trial** that automatically upgrades users to **$9.99/month** after the trial period. It includes comprehensive Stripe integration and foundation for future tiered plans.

## Key Features

### Trial System
- **$1 Trial**: 7-day trial period with minimal upfront cost
- **Automatic Upgrade**: Seamless transition to $9.99/month Basic plan
- **Trial Notifications**: Proactive communication at 3 days, 1 day, and expiry
- **Access Control**: Trial users get limited features during trial period

### Subscription Plans

#### Current Plans
1. **Trial (7-day)**: $1.00 one-time
   - 10 entries per day limit
   - Basic insights only
   - No AI analysis or data export

2. **Basic Monthly**: $9.99/month
   - Unlimited entries
   - Full AI analysis
   - Data export capabilities
   - Basic support

3. **Pro Monthly**: $19.99/month  
   - All Basic features
   - Advanced AI analysis
   - Priority support
   - Custom themes

4. **Enterprise Monthly**: $49.99/month
   - All Pro features
   - Team collaboration
   - Advanced analytics
   - API access

### Stripe Integration
- **Customer Management**: Automatic Stripe customer creation
- **Payment Processing**: Secure trial and subscription billing
- **Webhook Handling**: Real-time subscription status updates
- **Cancellation Support**: Graceful subscription cancellation

### Notification System
- **Trial Welcome**: Onboarding message with trial details
- **Expiry Warnings**: 3-day and 1-day advance notifications
- **Upgrade Confirmation**: Success message for paid upgrade
- **Payment Issues**: Failure notifications with retry guidance
- **Cancellation**: Confirmation and retention messaging

## Implementation Architecture

### Models (`baddie_journal/models/`)

#### User Model
```python
@dataclass
class User:
    id: str
    email: str 
    name: str
    stripe_customer_id: Optional[str]
    current_subscription_id: Optional[str]
    created_at: Optional[datetime]
    is_active: bool = True
```

#### Subscription Model
```python
@dataclass  
class Subscription:
    id: str
    user_id: str
    plan_id: str
    status: SubscriptionStatus  # TRIAL, ACTIVE, EXPIRED, CANCELLED
    stripe_subscription_id: Optional[str]
    trial_start: Optional[datetime]
    trial_end: Optional[datetime]
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    
    # Key methods:
    def start_trial(self, trial_days: int = 7)
    def upgrade_from_trial(self, new_period_end: datetime)
    def cancel_subscription(self, at_period_end: bool = True)
```

#### SubscriptionPlan Model
```python
@dataclass
class SubscriptionPlan:
    id: str
    name: str
    plan_type: SubscriptionPlanType
    price_cents: int
    billing_interval: str
    trial_days: int
    stripe_price_id: Optional[str]
    features: Dict[str, Any]
```

### Services (`baddie_journal/services/`)

#### SubscriptionService
Core business logic for subscription management:
- User creation with trial
- Trial to paid upgrades  
- Subscription access control
- Plan management

#### StripeService
Stripe payment integration:
- Customer creation
- Trial subscription setup ($1 charge)
- Automatic upgrade to $9.99/month
- Webhook event handling
- Cancellation processing

#### NotificationService
User communication system:
- Template-based messaging
- Trial expiry notifications
- Upgrade and payment notifications
- Branded "baddie" messaging style

## Usage Examples

### Creating User with Trial
```python
from baddie_journal.services import SubscriptionService

service = SubscriptionService()
result = service.create_user_with_trial(
    email="user@example.com",
    name="New User"
)

if result['success']:
    user = result['user']
    subscription = result['subscription']
    # User now has 7-day trial access
```

### Checking Subscription Access
```python
access_info = service.check_subscription_access(subscription)

if access_info['has_access']:
    # User can use the application
    features = access_info['features']
    
if access_info['needs_upgrade']:
    # Trial has expired, trigger upgrade flow
    service.upgrade_trial_to_paid(subscription)
```

### Stripe Integration
```python
from baddie_journal.services import StripeService

stripe_service = StripeService(
    api_key=os.getenv('STRIPE_SECRET_KEY'),
    webhook_secret=os.getenv('STRIPE_WEBHOOK_SECRET')
)

# Create customer and trial subscription
customer_id = stripe_service.create_customer(user)
stripe_data = stripe_service.create_trial_subscription(
    customer_id, 
    basic_plan,
    trial_days=7
)
```

### Webhook Handling
```python
# In your web application webhook endpoint
@app.route('/webhooks/stripe', methods=['POST'])
def handle_stripe_webhook():
    payload = request.get_data()
    signature = request.headers.get('stripe-signature')
    
    try:
        event_data = stripe_service.handle_webhook_event(payload, signature)
        if event_data:
            subscription_service.handle_stripe_webhook(event_data)
        
        return 'OK', 200
    except Exception as e:
        return str(e), 400
```

## Configuration

### Environment Variables
```bash
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_...           # Your Stripe secret key
STRIPE_WEBHOOK_SECRET=whsec_...         # Webhook endpoint secret

# Application Configuration  
SECRET_KEY=your-app-secret              # Application secret key
SQLALCHEMY_DATABASE_URI=postgresql://...  # Database connection
```

### Stripe Dashboard Setup
1. Create products for each subscription plan
2. Set up webhook endpoints for:
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `customer.subscription.trial_will_end`

## Testing

### Run Subscription Tests
```bash
python3 test_subscription.py
```

### Run Demo
```bash
python3 demo_subscription.py
```

### Test Coverage
- ✅ Subscription model functionality
- ✅ Trial period management  
- ✅ Automatic upgrade logic
- ✅ Notification system
- ✅ Plan configuration
- ✅ Complete trial workflow
- ✅ Stripe integration (with mocks)

## Database Integration

The current implementation uses in-memory dataclasses. For production, integrate with your database layer:

```python
# Example SQLAlchemy integration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create tables for User, Subscription, SubscriptionPlan
# Implement repository pattern for data access
# Add database persistence to SubscriptionService
```

## Deployment Checklist

- [ ] Set up Stripe account and get API keys
- [ ] Configure webhook endpoints in Stripe dashboard  
- [ ] Set environment variables in production
- [ ] Implement database persistence layer
- [ ] Set up email notification service (SendGrid, Mailgun, etc.)
- [ ] Add authentication and session management
- [ ] Implement payment method management UI
- [ ] Add subscription management dashboard
- [ ] Set up monitoring and error tracking
- [ ] Test webhook delivery and retry logic

## Security Considerations

- Store Stripe keys securely in environment variables
- Validate webhook signatures to prevent forgery
- Use HTTPS for all payment-related endpoints
- Implement proper authentication for subscription management
- Log subscription events for audit trail
- Handle PCI compliance requirements appropriately

## Future Enhancements

The system is designed to support future expansion:

- **Additional Plan Tiers**: Easy to add new subscription levels
- **Annual Billing**: Support for yearly subscriptions with discounts
- **Usage-Based Billing**: Track and bill for specific feature usage
- **Promo Codes**: Discount and coupon system
- **Dunning Management**: Advanced payment retry logic
- **Churn Reduction**: Cancellation flow with retention offers