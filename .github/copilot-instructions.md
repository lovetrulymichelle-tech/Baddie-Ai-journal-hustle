# Baddie AI Journal Hustle

Baddie AI Journal Hustle is a Python-based journaling application with AI-powered insights, mood tracking, subscription features, and analytics. The application is a fully deployable Flask web application with database support, Swarms AI integration, and subscription management.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Current Repository State

**FULLY FUNCTIONAL**: This repository contains a complete, deployable web application with comprehensive features including Flask web framework, database integration, subscription system, and AI analysis capabilities.

### Production-Ready Components
- **Flask Web Application**: `app.py` with full web interface and routes
- **Database Layer**: `database.py` with SQLAlchemy integration and PostgreSQL support  
- **Core Models**: Journal entries, insights, users, and subscription models
- **Subscription System**: Complete subscription management with trial and paid tiers
- **AI Integration**: Swarms framework integration for advanced journal analysis
- **Deployment Configuration**: `Procfile`, `requirements.txt`, ready for Railway deployment
- **Web Templates**: Complete HTML templates in `templates/` directory
- **Testing Suite**: Comprehensive test files for all major components

## Working Effectively

### Environment Setup
- Python 3.12.3 is available and working
- pip 24.0 is available and working  
- git is available at `/usr/bin/git`
- Virtual environment creation works: `python3 -m venv venv`

### Development Environment Setup

**Virtual Environment Setup (REQUIRED):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows
```

**Dependencies Installation:**
```bash
pip install -r requirements.txt
```
- Installs Flask, SQLAlchemy, PostgreSQL drivers, Gunicorn and core dependencies
- Optional AI dependencies (swarms, openai) are handled gracefully if missing
- **Note**: If network timeouts occur, retry the installation or install individual packages

**Testing:**
```bash
# Run all basic functionality tests
python test_swarms.py

# Run comprehensive subscription system tests  
python test_subscription.py

# Run deployment verification
python check_deployment.py

# Demo the full application
python demo.py
```
- NEVER CANCEL: Test suite may take 5-15 minutes. Set timeout to 30+ minutes.
- pytest is NOT installed - use direct Python script execution

**Application Deployment:**
```bash
# Local development server
python app.py

# Production server (used by Procfile)
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 60
```

**Linting/Formatting:**
- No specific linting tools configured yet - code follows PEP 8 standards
- Can add flake8, black, or ruff if needed for code quality

## Application Architecture (Current Implementation)

The application is built with a modular Flask architecture:

### Core Components (Production Ready)
- **Flask Web Application** (`app.py`): Complete web server with routes, templates, and API endpoints
- **Database Layer** (`database.py`): SQLAlchemy integration with PostgreSQL and SQLite fallback
- **Journal Models** (`baddie_journal/models/journal.py`): JournalEntry and InsightData classes
- **Subscription Models** (`baddie_journal/models/subscription.py`): User, Subscription, SubscriptionPlan classes  
- **InsightsHelper** (`baddie_journal/insights.py`): Analytics calculations (streaks, mood breakdowns, top tags)
- **Swarms AI Integration** (`baddie_journal/swarms_integration.py`): Multi-agent AI analysis system
- **Subscription Services** (`baddie_journal/services/`): Complete subscription management with Stripe integration
- **Templates** (`templates/`): Complete HTML interface (base, index, entries, insights, error pages)

### Key Features (Fully Implemented)
- **Web Interface**: Complete HTML templates with forms and dashboards  
- **Journal Management**: Create, view, search journal entries
- **Analytics Dashboard**: Streak tracking, mood distribution, tag analysis, CSV export
- **Subscription System**: 7-day trials, tiered plans ($9.99 basic, $19.99 pro, $49.99 enterprise) 
- **AI Analysis**: Multi-agent Swarms integration for mood analysis, pattern recognition, growth insights
- **Database Integration**: PostgreSQL for production, SQLite fallback for development
- **Deployment Ready**: Gunicorn WSGI server, Railway/Heroku Procfile
- **UTC Time Handling**: All timestamps stored in UTC for consistency

### Current Project Structure
```
├── app.py                      # Main Flask web application  
├── database.py                 # Database connection and fallback logic
├── Procfile                    # Railway/Heroku deployment config
├── requirements.txt            # Production dependencies
├── check_deployment.py         # Deployment verification script
├── demo.py                     # Full feature demonstration
├── migrate_sqlite_to_postgres.py  # Database migration tool
├── templates/                  # Complete web interface
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page with journal entry form
│   ├── entries.html           # List and manage journal entries
│   ├── insights.html          # Analytics dashboard
│   └── error.html             # Error page handling
├── baddie_journal/             # Core business logic package
│   ├── __init__.py            # Package initialization and exports
│   ├── insights.py            # Analytics and calculations engine
│   ├── swarms_integration.py  # AI analysis with multiple agents
│   ├── models/                # Data models
│   │   ├── journal.py         # JournalEntry, InsightData
│   │   └── subscription.py    # User, Subscription, SubscriptionPlan
│   └── services/              # Business logic services
│       ├── subscription_service.py    # Subscription management
│       ├── stripe_service.py          # Payment processing
│       └── notification_service.py    # Email notifications
├── test_swarms.py             # Core functionality tests
├── test_subscription.py       # Subscription system tests
└── demo_subscription.py       # Subscription workflow demonstration
```

### Example Usage Pattern (Current API)
```python
from datetime import datetime, UTC
from baddie_journal import JournalEntry, InsightData, InsightsHelper

# Create journal entries - Note: Use datetime.now(UTC) instead of deprecated utcnow()
entries = [
    JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.now(UTC)),
    JournalEntry(2, "Productive work", "focused", "work", ["productivity"], datetime.now(UTC))
]

# Basic analytics
insight_data = InsightData(entries)  
helper = InsightsHelper(insight_data)
print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")  
print(f"Top tags: {helper.get_top_tags(5)}")

# AI Analysis (requires OPENAI_API_KEY environment variable)
from baddie_journal import JournalAnalysisSwarm
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"
swarm = JournalAnalysisSwarm()
result = swarm.perform_comprehensive_analysis(insight_data)
print("🧠 Mood Analysis:", result.mood_analysis)
print("🔍 Pattern Recognition:", result.pattern_insights)  
print("🌱 Growth Coaching:", result.personal_growth_insights)
print("💡 AI Recommendations:", result.recommendations)

# Subscription System
from baddie_journal.services.subscription_service import SubscriptionService

service = SubscriptionService()
result = service.create_user_with_trial(
    email="user@example.com", 
    name="User Name"
)
print(f"Trial created: {result['success']}")
```

## Validation

**Standard Development Workflow:**
1. Create and activate virtual environment: `python3 -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt` 
3. Run deployment verification: `python check_deployment.py` (should pass all checks)
4. Run core tests: `python test_swarms.py` (tests models, insights, AI integration)
5. Run subscription tests: `python test_subscription.py` (comprehensive subscription workflow tests)
6. Test web application: `python app.py` (starts Flask development server on localhost:5000)
7. Run full demo: `python demo.py` (demonstrates all features)

**Testing Guidelines:**
- NEVER CANCEL test runs - they may take 15+ minutes to complete (set timeout to 30+ minutes)
- Tests use direct Python execution, not pytest framework
- All tests include proper error handling and detailed output
- Tests validate both success cases and error conditions

**Core User Workflows to Always Test:**
- Creating journal entries with different moods and tags
- Generating insights and analytics (streak, mood breakdown, top tags)
- Exporting data to CSV
- Verifying streak calculations across different time periods
- Subscription trial creation and management
- AI analysis workflow (with and without API key)
- Web interface functionality (forms, navigation, dashboards)

**Environment Variables (Production):**
- `SECRET_KEY`: Flask secret key for sessions (required)
- `SQLALCHEMY_DATABASE_URI`: Database connection string (optional, defaults to SQLite)
- `OPENAI_API_KEY`: For AI analysis features (optional)
- `STRIPE_SECRET_KEY`: For subscription payments (optional)  
- `STRIPE_WEBHOOK_SECRET`: For webhook verification (optional)
- `PORT`: Application port (optional, defaults to 5000)

## Common Tasks

### Deployment Verification
```bash
python check_deployment.py
```
**Expected output:** All checks should pass - Python version, dependencies, environment variables, app structure, imports, and database connection.

### Current Repository Contents
```
├── app.py                    # Flask web application (7977 bytes)  
├── Procfile                  # Railway deployment config
├── requirements.txt          # Production dependencies (506 bytes)
├── database.py               # Database layer with PostgreSQL/SQLite
├── templates/                # Complete HTML interface
├── baddie_journal/           # Core business logic package  
├── check_deployment.py       # Deployment verification script
├── demo.py                   # Full application demonstration  
├── demo_subscription.py      # Subscription workflow demo
├── test_swarms.py           # Core functionality tests
├── test_subscription.py     # Subscription system tests
├── migrate_sqlite_to_postgres.py  # Database migration utility
└── DEPLOYMENT_*.md          # Comprehensive deployment documentation
```

### Available Demo Scripts
- `python demo.py` - Complete feature demonstration (journal + analytics + AI)
- `python demo_subscription.py` - Subscription system demonstration  
- `python test_swarms.py` - Core functionality validation
- `python test_subscription.py` - Comprehensive subscription workflow testing

### Database Management
- **Local Development**: Uses SQLite (`journal.db`) by default
- **Production**: Configured for PostgreSQL with automatic fallback
- **Migration**: Use `migrate_sqlite_to_postgres.py` to move data to production database

### Dependencies Summary (requirements.txt)
- **Core Web**: Flask>=2.3.0, gunicorn>=20.1.0
- **Database**: sqlalchemy>=2.0.0, psycopg2-binary>=2.9.0  
- **Utilities**: python-dateutil>=2.8.0
- **Optional AI**: swarms>=6.0.0, openai>=1.0.0 (graceful fallback if missing)
- **Optional Payments**: stripe>=8.0.0 (graceful fallback if missing)
- **Optional Analytics**: pandas>=2.0.0 (has fallback implementation)

## Development Workflow

**For New Feature Development:**
1. Create virtual environment: `python3 -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`  
4. Run deployment verification: `python check_deployment.py` (all checks should pass)
5. Run existing tests to ensure baseline: `python test_swarms.py && python test_subscription.py`
6. Make changes to code
7. Test changes immediately: run relevant test scripts and `python demo.py`
8. Verify web interface: `python app.py` and test in browser at localhost:5000
9. Run full test suite again to prevent regressions - NEVER CANCEL: Set timeout to 30+ minutes
10. Update documentation if API changes are made

**For Bug Fixes:**
1. Reproduce the issue with a test case first or identify in existing tests
2. Follow the development workflow above
3. Verify the fix resolves the specific issue using demo scripts
4. Ensure no regressions in existing functionality
5. Consider adding specific test cases for the bug

**For Deployment Updates:**
1. Test locally: `python app.py`
2. Run deployment verification: `python check_deployment.py`
3. Verify all required environment variables are documented
4. Test database migration if schema changes were made
5. Update Procfile if startup procedure changed

## Important Notes

- **NEVER CANCEL** any test runs - they may take 15+ minutes to complete
- Always use virtual environments to avoid dependency conflicts  
- All timestamps are handled in UTC as per application design
- The application focuses on personal journaling with privacy as a priority
- Analytics are private and visible only to the user
- CSV export functionality maintains user privacy and data security
- **Flask web application is fully functional** and can be deployed immediately
- **Database layer supports both PostgreSQL (production) and SQLite (development)** with automatic fallback
- **Subscription system is production-ready** with Stripe integration (when configured)
- **AI features gracefully degrade** when API keys or optional dependencies are missing
- **All tests use direct Python execution** - pytest is not configured
- **Deployment verification script** (`check_deployment.py`) should always pass before deployment

## AI Features Integration

**Swarms AI Analysis:**
- Multi-agent system with 4 specialized agents: Mood Analyzer, Pattern Recognizer, Growth Coach, Recommendation Specialist
- Requires `OPENAI_API_KEY` environment variable
- Gracefully falls back to basic analytics if API key or dependencies missing
- Test with: `python demo.py` (shows both basic and AI analysis)

**Subscription Features:**
- Complete subscription management system with trial periods ($1 for 7 days)
- Tiered pricing: Basic ($9.99), Pro ($19.99), Enterprise ($49.99)  
- Stripe integration for payments (requires `STRIPE_SECRET_KEY`)
- Email notifications for trial expiry and upgrades
- Test with: `python test_subscription.py` and `python demo_subscription.py`