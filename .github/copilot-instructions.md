# Baddie AI Journal Hustle

Baddie AI Journal Hustle is a Python-based journaling application with AI-powered insights, mood tracking, and analytics features. The application provides streak tracking, mood analysis, tagging systems, and CSV export capabilities.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Current Repository State

**IMPORTANT**: This repository is currently in early development stage with minimal code. Most build and test commands will not work until the core application code is implemented.

### Existing Files
- `README.md` - Documents the Insights feature and planned functionality
- `.gitignore` - Standard Python gitignore configuration  
- `issues/10.md` - Brief referral program documentation
- No source code, dependencies, or build configuration files exist yet

## Working Effectively

### Environment Setup
- Python 3.12.3 is available and working
- pip 24.0 is available and working
- git is available at `/usr/bin/git`
- Virtual environment creation works: `python3 -m venv venv`

### When Code is Added - Future Instructions

**Virtual Environment Setup:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows
```

**Expected Dependencies Installation (when requirements.txt exists):**
```bash
pip install -r requirements.txt
```

**Expected Build Process (when setup.py/pyproject.toml exists):**
```bash
pip install -e .
# OR
python setup.py develop
```

**Expected Testing (when tests exist):**
```bash
python -m pytest
# OR
python -m unittest discover
```
- NEVER CANCEL: Test suite may take 5-15 minutes. Set timeout to 30+ minutes.

**Expected Linting (when configured):**
```bash
python -m flake8
# OR
python -m pylint baddie_journal/
# OR  
python -m ruff check
```

**Expected Formatting (when configured):**
```bash
python -m black .
# OR
python -m autopep8 --in-place --recursive .
```

## Application Architecture (Planned)

Based on README.md, the application will include:

### Core Components
- **JournalEntry Model**: Stores individual journal entries with mood, category, tags, and timestamps
- **InsightData Model**: Aggregates and analyzes journal entries  
- **InsightsHelper**: Provides analytics calculations (streaks, mood breakdowns, top tags)

### Key Features
- **Streak Tracking**: Consecutive days of journaling
- **Mood Analysis**: Distribution and trends of emotional states
- **Tag Analytics**: Most frequently used tags and topics
- **CSV Export**: Data export for external analysis
- **UTC Time Handling**: All timestamps stored in UTC for consistency

### Example Usage Pattern (from README)
```python
from datetime import datetime, UTC
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper

# Sample entries - Note: Use datetime.now(UTC) instead of deprecated utcnow()
entries = [
    JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.now(UTC)),
    JournalEntry(2, "Productive work", "focused", "work", ["productivity"], datetime.now(UTC))
]

helper = InsightsHelper(InsightData(entries))
print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")  
print(f"Top tags: {helper.get_top_tags(5)}")
```

## Validation

**When Application Code Exists:**
- Always create and activate a virtual environment before making changes
- Always install dependencies with `pip install -r requirements.txt` after environment setup
- Always run the full test suite after making changes: `python -m pytest` - NEVER CANCEL: Set timeout to 30+ minutes
- Always run linting before committing: `python -m flake8` or equivalent
- Always test core user workflows:
  - Creating journal entries with different moods and tags
  - Generating insights and analytics
  - Exporting data to CSV
  - Verifying streak calculations

**Current State Validation:**
- Repository structure is minimal - only documentation exists
- No build or test commands will work until code is implemented
- Virtual environment creation and Python/pip functionality is verified working

## Common Tasks

### Current Repository Contents
```
ls -la
.
..
.git/
.github/
.gitignore
README.md  
issues/
  10.md
```

### README.md Summary
The README documents a planned Insights feature for journal analytics including:
- Streak tracking for consecutive journaling days
- Daily writing frequency over customizable periods  
- Mood and category distribution visualization
- Top tags analysis with configurable limits
- Total metrics and average frequency calculations
- UTC timestamp handling for cross-timezone consistency
- CSV export functionality for external analysis

### Expected Project Structure (when implemented)
```
baddie_journal/
  __init__.py
  models.py        # JournalEntry, InsightData classes
  insights.py      # InsightsHelper class
  main.py          # Application entry point
tests/
  test_models.py
  test_insights.py
requirements.txt
setup.py         # OR pyproject.toml
README.md
```

## Development Workflow

**For New Development:**
1. Create virtual environment: `python3 -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` (when file exists)
4. Run tests: `python -m pytest` (when tests exist) - NEVER CANCEL: Set timeout to 30+ minutes
5. Make changes
6. Run tests again to verify: `python -m pytest` - NEVER CANCEL: Set timeout to 30+ minutes  
7. Run linting: `python -m flake8` or equivalent (when configured)
8. Test actual functionality manually with sample journal entries

**For Bug Fixes:**
1. Reproduce the issue with a test case first
2. Follow the development workflow above
3. Verify the fix resolves the specific issue
4. Ensure no regressions in existing functionality

## Important Notes

- **NEVER CANCEL** any test runs - they may take 15+ minutes to complete
- Always use virtual environments to avoid dependency conflicts
- All timestamps should be handled in UTC as per application design
- The application focuses on personal journaling with privacy as a priority
- Analytics are intended to be private and visible only to the user
- CSV export functionality should maintain user privacy and data security