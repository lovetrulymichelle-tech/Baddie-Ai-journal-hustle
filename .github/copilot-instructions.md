# Baddie AI Journal Hustle

Baddie AI Journal Hustle is a Python Flask web application for journaling with insights and analytics. The application allows users to create journal entries with moods, categories, and tags, then provides comprehensive analytics including streaks, mood breakdowns, and tag analysis.

**ALWAYS follow these instructions first and only fall back to search or additional exploration if the information here is incomplete or found to be in error.**

## Working Effectively

### Environment Setup
- **Python Version**: Use Python 3.12+ (available on the system)
- **Dependency Installation**: 
  - `pip3 install -r requirements.txt` -- takes 6-10 seconds. NEVER CANCEL.
  - Alternative: `pip3 install flask flask-sqlalchemy pytest`

### Building and Testing
- **Flask App Initialization**: `python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')"` -- takes < 1 second
- **Run Tests**: `PYTHONPATH=. pytest tests/ -v` -- takes 1-2 seconds. NEVER CANCEL.
- **Expected Test Results**: 6-7 tests should pass, 1 test may fail (streak calculation edge case - this is acceptable)

### Running the Application
- **Development Server**: `python3 app.py` -- starts immediately, runs on http://127.0.0.1:5000
- **API Testing**: Use `curl http://127.0.0.1:5000/api/insights` to test the API endpoint
- **Manual Testing**: Access http://127.0.0.1:5000 to see the web interface

## Validation Scenarios

**CRITICAL**: Always test these scenarios after making changes:

### Basic Functionality Test
1. Start the Flask app with `python3 app.py`
2. Test API endpoint: `curl -s http://127.0.0.1:5000/api/insights | python3 -m json.tool`
3. Add a test entry: `curl -X POST http://127.0.0.1:5000/add_entry -d "text=Test&mood=happy&category=Test&tags=validation"`
4. Verify entry was added by checking API again - totals should show 1 entry

### Test Suite Validation
1. Run the full test suite: `PYTHONPATH=. pytest tests/ -v`
2. Verify at least 6 out of 7 tests pass
3. All Flask routes should be accessible (test_flask_routes should pass)

### Database Operations
1. Verify database creation: Check that `instance/journal.db` is created when running the app
2. Test insights functions: All analytics functions should return data without errors
3. Test entry creation: Entries should be stored with proper mood, category, and tags

## Project Structure

### Key Files
- `app.py` - Main Flask application with routes and insights functions
- `requirements.txt` - Python dependencies (Flask, SQLAlchemy, pytest)
- `tests/test_insights.py` - Test suite for all functionality
- `tests/__init__.py` - Makes tests directory a Python package
- `.gitignore` - Python project gitignore (extensive, covers all Python patterns)
- `README.md` - Documentation about the Insights feature

### Database Schema
- **Entry Model**: id, text, mood, tags (comma-separated), category, created_at
- **Database**: SQLite (journal.db for persistent storage, :memory: for tests)

### Core Functions
- `compute_streak()` - Calculate consecutive days of journaling
- `daily_counts_last_n(days)` - Entry counts for last N days
- `mood_breakdown_last_30()` - Mood distribution analysis
- `category_breakdown_last_30()` - Category distribution analysis  
- `top_tags_last_60(limit)` - Most frequently used tags
- `totals()` - Total entries for last 7 and 30 days

## Routes and API

### Web Routes
- `/` - Home page with entry form and quick insights
- `/insights` - Full insights dashboard with analytics
- `/add_entry` (POST) - Add new journal entry

### API Endpoints  
- `/api/insights` - JSON endpoint returning all analytics data

## Common Commands Reference

### Repository Root Contents
```
.
..
.git/
.github/
  copilot-instructions.md
.gitignore
README.md
app.py
requirements.txt
tests/
  __init__.py
  test_insights.py
instance/
  journal.db (created when app runs)
__pycache__/ (created by Python)
.pytest_cache/ (created by pytest)
```

### Key Package Dependencies
```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1  
pytest==8.4.1
```

### Environment Variables
- `PYTHONPATH=.` - Required for running tests to import app module
- `FLASK_ENV=development` - Enables debug mode (optional)

## Development Workflow

### Making Changes
1. **ALWAYS run tests first**: `PYTHONPATH=. pytest tests/ -v` to understand current state
2. **Test the app**: Start app with `python3 app.py` and test basic functionality
3. **Make minimal changes**: Edit app.py or tests as needed
4. **Re-run tests**: Ensure tests still pass after changes
5. **Test manually**: Add entries and verify insights work correctly

### Adding New Features
1. **Add tests first**: Create tests in `tests/test_insights.py` for new functionality
2. **Implement in app.py**: Add new routes, functions, or models
3. **Test thoroughly**: Use both automated tests and manual validation
4. **Update this documentation**: If adding new commands or procedures

## Troubleshooting

### Common Issues
- **Import errors in tests**: Use `PYTHONPATH=. pytest tests/` 
- **Database issues**: Delete `instance/journal.db` and restart app to recreate
- **Port conflicts**: Flask runs on port 5000 by default
- **Test failures**: One test (streak calculation edge case) may fail - this is acceptable

### Performance Expectations
- **Dependency installation**: 6-10 seconds
- **App startup**: < 1 second  
- **Test suite**: 1-2 seconds
- **Database initialization**: < 1 second

## Security Notes
- **Development only**: This configuration is for development, not production
- **Database**: SQLite database is created in `instance/journal.db`
- **No authentication**: Current implementation has no user authentication

**NEVER CANCEL builds or tests - they complete quickly (under 10 seconds for all operations).**