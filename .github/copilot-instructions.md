# Baddie AI Journal - Copilot Instructions

Baddie AI Journal is a Python Flask web application for journaling with analytics and insights features. The application uses SQLAlchemy for database operations, supports moods/categories/tags for entries, and provides analytics dashboards.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Setup (CRITICAL - DO THIS FIRST)
**NEVER CANCEL: Each step typically takes 5-30 seconds for local operations, up to 5 minutes for network operations. Set timeout to 360+ seconds for pip installs.**

- Install Python dependencies and set up virtual environment:
  - `python3 -m venv venv` -- creates virtual environment (takes ~3 seconds)
  - `source venv/bin/activate` -- activates virtual environment 
  - `pip install flask flask-sqlalchemy pytest black flake8` -- **FAILS due to network limitations. See workarounds below.**
  - `pip freeze > requirements.txt` -- saves dependencies list

**NETWORK LIMITATION WORKAROUND**: pip install commands fail due to firewall restrictions in this environment. Alternative approaches:
  - Use system Python with basic functionality: `python3 -c "import sqlite3; print('Basic Python works')"`
  - Create minimal app without external dependencies first
  - When network access is available, install packages individually with extended timeouts: `pip install --timeout=300 flask`

### Core Development Commands

- **Build/Setup**: 
  - `source venv/bin/activate` -- always activate virtual environment first
  - `pip install -r requirements.txt` -- **FAILS due to network limitations. Use workarounds above.**

- **Run the application**:
  - ALWAYS run the setup steps first (or use system Python)
  - Create `app.py` with Flask application if it doesn't exist
  - `python app.py` -- starts development server on http://127.0.0.1:5000
  - Press Ctrl+C to stop the server
  - **Without Flask**: Create basic Python scripts for testing logic

- **Testing**:
  - `pytest` -- **REQUIRES pytest installation. May fail due to network limitations.**
  - `python -m unittest` -- Alternative using built-in unittest module  
  - `python tests/test_*.py` -- Run individual test files manually
  - **NEVER CANCEL: Test suites may take 1-5 minutes depending on database operations. Set timeout to 10+ minutes.**

- **Code Quality**:
  - `python -m py_compile *.py` -- Basic syntax checking (built-in)
  - `black .` -- **REQUIRES black installation. May fail due to network limitations.**
  - `flake8 .` -- **REQUIRES flake8 installation. May fail due to network limitations.**
  - **ALWAYS run syntax checks before committing changes**

## Project Structure

**Current State**: This repository is in early development. The core application code needs to be implemented.

**Expected Structure**:
```
/
├── app.py              # Main Flask application (TO BE CREATED)
├── requirements.txt    # Python dependencies
├── tests/              # Test directory 
│   └── test_insights.py # Tests for insights features (exists in other branches)
├── static/             # CSS, JS, images (TO BE CREATED)
├── templates/          # HTML templates (TO BE CREATED)
└── .github/
    └── copilot-instructions.md # This file
```

**Database Model** (based on test files in other branches):
- **Entry**: Main journal entry model with fields:
  - `id` (Integer, primary key)
  - `text` (Text, required)
  - `mood` (String, optional)
  - `tags` (Text, comma-separated)
  - `category` (String, optional)
  - `created_at` (DateTime, auto-generated)

## Validation

## Validation

- **Manual Testing**: After making changes, always test functionality:
  - Use built-in Python first: `python3 script.py`
  - Test database operations with SQLite: `python3 -c "import sqlite3; print('SQLite works')"`
  - If Flask is available: Navigate to http://127.0.0.1:5000 or use `curl http://127.0.0.1:5000`
  - Test basic functionality like creating entries, viewing analytics

- **Development Workflow**: 
  - Start with basic Python approach (no external dependencies)
  - Make code changes
  - Run `python3 -m py_compile *.py` for syntax checking
  - Run `python3 -m unittest test_*.py` for testing
  - When external packages available, upgrade to Flask approach
  - Commit changes

## Known Limitations and Workarounds

- **Network Access**: pip install commands fail due to firewall limitations. 
  - **Workaround**: Use basic Python functionality with built-in modules
  - **Workaround**: When network access is available, use extended timeouts: `pip install --timeout=300 package_name`
  - **Workaround**: Create simple scripts without external dependencies first

- **Core Application Missing**: The main `app.py` file doesn't exist yet. When creating it, start with basic Python structure:
```python
# Basic version without Flask (when network/packages unavailable)
import sqlite3
from datetime import datetime

class Entry:
    def __init__(self, text, mood=None, tags=None, category=None):
        self.text = text
        self.mood = mood  
        self.tags = tags or ""
        self.category = category or "Personal"
        self.created_at = datetime.utcnow()

# Flask version (when packages available)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50))
    tags = db.Column(db.Text)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

- **Tests Reference Non-existent Code**: Test files in the `add/insights-tests-pytest` branch reference functions like `compute_streak()`, `daily_counts_last_n()` etc. that need to be implemented in `app.py`

- **No Database Migrations**: Currently using SQLite with `db.create_all()`. For production, consider Flask-Migrate

- **No Frontend**: Templates and static files need to be created for the web interface

## Analytics Functions (TO BE IMPLEMENTED)

Based on test files, these functions should be implemented in `app.py`:
- `compute_streak()` - Calculate consecutive days of journaling
- `daily_counts_last_n(days)` - Count entries per day for last N days  
- `mood_breakdown_last_30()` - Mood distribution for last 30 days
- `category_breakdown_last_30()` - Category distribution for last 30 days
- `top_tags_last_60(limit)` - Most frequently used tags
- `totals()` - Total entries for last 7 and 30 days

## Time Expectations

- Virtual environment creation: ~3 seconds
- Package installation: **FAILS due to network limitations - See workarounds**
- Code syntax checking (py_compile): ~0.1 seconds
- Basic Python script execution: ~0.1 seconds  
- Running unittest tests: ~0.1 seconds (simple tests), up to 5 minutes with database operations
- Creating test database with SQLite: ~0.01 seconds

**CRITICAL**: Always use timeouts of 60+ seconds for local operations and 360+ seconds for network operations. NEVER CANCEL long-running operations.

## Common Tasks Reference

### Repository Status
```bash
# Current branch has minimal files
ls -la
# .
# ..
# .git/
# .gitignore
# README.md  
# .github/
```

### Python Environment Check
```bash
python3 --version  # Python 3.12.3
pip3 --version     # pip 24.0
which python3      # /usr/bin/python3
```

### Dependencies List
Core dependencies for this project:
- flask (3.1.2+)
- flask-sqlalchemy (3.1.1+) 
- pytest (8.4.1+)
- black (25.1.0+)
- flake8 (7.3.0+)