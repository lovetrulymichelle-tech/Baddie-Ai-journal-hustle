# Baddie AI Journal Hustle

💎 Baddie AI Journal — An assistant-style journaling app with moods, categories, affirmations, and smart exports.

**CRITICAL**: Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Repository Status

**IMPORTANT**: This repository is currently in a documentation/design phase. It contains design specifications and feature documentation but NO actual source code, build configurations, or runnable application.

## Current Repository Structure

```
.
├── .github/
│   └── copilot-instructions.md (this file)
├── .gitignore (comprehensive Python project gitignore)
├── README.md (Insights feature documentation)
└── issues/
    └── 10.md (referral program specifications)
```

## What You CAN Do

- Read and understand the feature specifications in README.md
- Review the Insights feature design and API examples
- Understand the intended Python architecture from code examples
- Modify documentation files
- Add new documentation or specification files
- Create project structure and configuration files when implementing

## What You CANNOT Do (Repository Limitations)

- **DO NOT** attempt to build the application - no build system exists
- **DO NOT** try to run tests - no test framework is configured
- **DO NOT** attempt to run the application - no source code exists
- **DO NOT** try to install dependencies - no requirements.txt or pyproject.toml exists
- **DO NOT** search for Python modules referenced in README.md - they don't exist yet

## Intended Architecture (From Documentation)

Based on README.md examples, the planned architecture includes:

```python
# Planned module structure (NOT YET IMPLEMENTED):
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper
```

### Key Components (Planned):
- **JournalEntry**: Model for individual journal entries with mood, category, tags, timestamp
- **InsightData**: Container for journal entry collections
- **InsightsHelper**: Analytics engine for streaks, mood breakdowns, top tags

### Features (Planned):
- Streak tracking for consecutive journaling days
- Mood and category distribution analytics
- Tag frequency analysis
- CSV export functionality
- UTC timestamp handling for timezone consistency

## Development Guidelines

### When Implementing Code:
- Use Python as the primary language (based on .gitignore and examples)
- Follow the architecture outlined in README.md examples
- **IMPORTANT**: Use `datetime.now(datetime.UTC)` instead of deprecated `datetime.utcnow()`
- Implement UTC timezone handling for all timestamps
- Create modular structure: `baddie_journal.models`, `baddie_journal.insights`
- Include CSV export functionality
- Support real-time analytics from journal entry data

### Project Setup Commands (When Implementing):
```bash
# Create Python project structure
mkdir -p baddie_journal/{models,insights}
touch baddie_journal/__init__.py
touch baddie_journal/models/__init__.py  
touch baddie_journal/insights/__init__.py

# Create basic project files
touch requirements.txt
touch pyproject.toml
touch setup.py

# Install testing dependencies (NEVER CANCEL: may take 2-5 minutes)
pip install pytest pytest-cov

# Create test structure
mkdir -p tests
touch tests/__init__.py
touch tests/test_models.py
touch tests/test_insights.py
```

### Validation Steps (When Code Exists):
- **NEVER CANCEL**: Initial setup may take 5-10 minutes depending on dependencies
- **NEVER CANCEL**: pip install pytest may take 2-5 minutes (timeout: 10+ minutes)
- Always run `python -m pytest` to execute tests (timeout: 15+ minutes)
- Use `python -m baddie_journal.insights` for testing analytics functionality
- Validate CSV export by running sample data through InsightsHelper
- Test timezone handling with various UTC timestamps
- **CRITICAL**: Always test with sample journal entries before making changes

## Common Tasks

### Repository Exploration
```bash
# Current repository contents
ls -la
# Output:
# .github/
# .gitignore
# README.md
# issues/

# View feature documentation
cat README.md

# Check referral program specs
cat issues/10.md
```

### File Contents Reference

#### README.md Summary
- Describes Insights feature for journal analytics
- Shows example Python API usage
- Covers streaks, mood breakdowns, top tags analysis
- Includes CSV export and UTC timezone handling
- References non-existent modules: baddie_journal.models, baddie_journal.insights

#### .gitignore Summary
- Comprehensive Python project gitignore
- Excludes __pycache__, .venv, build artifacts
- Includes modern Python tooling: UV, Poetry, PDM, Pixi
- Excludes IDE files: .vscode, .idea, Cursor
- Prepared for Python development workflow

## Expected Timeline for Implementation

When implementing the actual codebase:
- **Project setup**: 5-10 minutes (create files, virtual environment)
- **Core models implementation**: 30-60 minutes 
- **Insights analytics engine**: 60-90 minutes
- **Testing suite**: 30-45 minutes
- **CSV export functionality**: 15-30 minutes
- **NEVER CANCEL**: Full test suite may take 10-15 minutes on first run

## Validation Scenarios (When Code Exists)

**CRITICAL**: Always run these validation scenarios after making changes:

1. **Basic Journal Entry Creation**:
   ```python
   # Test creating journal entries with different moods and categories
   # Note: Use datetime.now(datetime.UTC) instead of deprecated utcnow()
   from datetime import datetime, UTC
   entry = JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.now(UTC))
   ```

2. **Insights Calculation**:
   ```python
   # Test streak calculation, mood breakdown, and top tags
   helper = InsightsHelper(InsightData(entries))
   assert helper.calculate_streak() >= 0
   assert helper.get_mood_breakdown() is not None
   ```

3. **CSV Export**:
   ```python
   # Verify CSV export produces valid output
   csv_data = helper.export_to_csv()
   assert csv_data.startswith("timestamp,mood,category")
   ```

## Error Prevention

- **DO NOT** assume any Python modules exist - check first
- **DO NOT** try to import baddie_journal modules until they're implemented  
- **DO NOT** attempt to run application commands until source code exists
- **ALWAYS** validate that files exist before referencing them in code
- **REMEMBER**: This is currently documentation-only, treat it as such

## Future Implementation Notes

When ready to implement:
1. Start with basic project structure and dependencies
2. Implement core models (JournalEntry, InsightData) first
3. Build analytics engine (InsightsHelper) incrementally  
4. Add comprehensive test coverage
5. Implement CSV export last
6. **CRITICAL**: Set timeouts of 60+ minutes for initial builds and 30+ minutes for test runs

---

For questions about features or implementation approach, refer to README.md examples and issue specifications in the issues/ directory.