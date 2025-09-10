# Copilot Instructions for Baddie AI Journal

## Overview
The Baddie AI Journal is a Python Flask application focused on AI-powered journaling with comprehensive insights and analytics. This repository leverages best practices for modern Python development, SQLAlchemy ORM, and automated testing.

## Project Structure
```
baddie-ai-journal-hustle/
├── baddie_journal/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── models.py           # SQLAlchemy models and data classes
│   ├── insights.py         # Analytics and insights engine
│   ├── app.py              # Flask application factory
│   └── templates/          # Jinja2 templates
├── tests/                  # Test suite
├── .github/                # GitHub workflows and templates
├── pyproject.toml          # Modern Python packaging
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Development Environment Setup

### Prerequisites
- Python 3.8+ (tested with 3.12)
- pip or uv for package management
- SQLite (for development) or PostgreSQL (for production)

### Installation Steps
```bash
# Clone repository
git clone https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle.git
cd Baddie-Ai-journal-hustle

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Or install from requirements
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy pre-commit
```

### Database Setup
```bash
# Development database (SQLite)
python -c "from baddie_journal.models import create_database_engine, create_tables; engine = create_database_engine(); create_tables(engine)"

# Production database (PostgreSQL)
export DATABASE_URL="postgresql://user:pass@localhost/baddie_journal"
python -c "from baddie_journal.models import create_database_engine, create_tables; engine = create_database_engine(); create_tables(engine)"
```

## Development Workflow

### Running the Application
```bash
# Development server
python -m baddie_journal.app

# Or using Flask CLI
export FLASK_APP=baddie_journal.app
flask run --debug

# Production server (example)
gunicorn baddie_journal.app:create_app()
```

### Testing Strategy
This project uses **pytest** with comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=baddie_journal --cov-report=html

# Run specific test file
pytest tests/test_insights.py

# Run specific test
pytest tests/test_insights.py::TestInsightsHelper::test_calculate_streak
```

### Code Quality Tools
```bash
# Format code
black baddie_journal/ tests/

# Lint code
flake8 baddie_journal/ tests/

# Type checking
mypy baddie_journal/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## Core Architecture

### Models (`baddie_journal/models.py`)
- **JournalEntryDB**: SQLAlchemy model for database persistence
- **JournalEntry**: Data class for insights calculations
- **InsightData**: Container for journal entries with filtering capabilities

### Insights Engine (`baddie_journal/insights.py`)
- **InsightsHelper**: Core analytics class with methods:
  - `calculate_streak()`: Consecutive days journaling
  - `get_mood_breakdown()`: Mood distribution analysis
  - `get_top_tags()`: Most used tags
  - `export_to_csv()`: Data export functionality

### Flask Application (`baddie_journal/app.py`)
- Application factory pattern
- RESTful API endpoints (`/api/insights`, `/api/export/csv`)
- Dashboard UI with responsive design
- Health check endpoint for monitoring

## API Endpoints

### GET /
Dashboard view with insights visualization

### GET /api/insights
Returns comprehensive insights data:
```json
{
  "streak": 5,
  "daily_counts": {"2025-01-01": 2, ...},
  "mood_breakdown": {"happy": 10, "anxious": 3},
  "category_breakdown": {"work": 8, "personal": 5},
  "top_tags": [["productivity", 12], ["exercise", 8]],
  "metrics": {
    "total_entries": 25,
    "unique_tags": 15,
    "avg_entries_per_day": 1.2
  }
}
```

### GET /api/export/csv
Export data as CSV:
- `?type=entries`: Raw journal entries
- `?type=summary`: Insights summary

### GET /api/health
Health check endpoint for monitoring

## Database Schema

### JournalEntryDB Table
```sql
CREATE TABLE journal_entries (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    mood VARCHAR(50),
    category VARCHAR(50),
    tags JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Performance Considerations

### Query Optimization
- Use `filter_by_date_range()` for time-bounded queries
- Implement database indexing on `created_at` and `category`
- Consider pagination for large datasets

### Caching Strategy
- Cache insights calculations for recent data
- Use Redis for production caching
- Implement cache invalidation on new entries

### Analytics Performance
```python
# Efficient date filtering
start_date = datetime.now() - timedelta(days=30)
recent_data = insight_data.filter_by_date_range(start_date, datetime.now())
helper = InsightsHelper(recent_data)
```

## Build and Deploy

### CI/CD Pipeline
See `.github/workflows/ci.yml` for automated:
- Dependency caching
- Testing with coverage
- Code quality checks
- Security scanning
- Build artifacts

### Production Deployment
```bash
# Build for production
pip install --no-dev
export FLASK_ENV=production
export DATABASE_URL="postgresql://..."

# Run with Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 baddie_journal.app:create_app()
```

### Environment Variables
```bash
# Required
DATABASE_URL=sqlite:///journal.db  # or PostgreSQL URL
SECRET_KEY=your-secret-key

# Optional
FLASK_ENV=production
FLASK_DEBUG=false
```

## Known Limitations and Timeouts

### Current Limitations
1. **Authentication**: No user authentication system (single-user mode)
2. **Real-time Updates**: Dashboard requires manual refresh
3. **File Uploads**: No support for image or file attachments
4. **Mobile App**: Web-only interface (responsive design)
5. **Advanced Analytics**: Limited to basic insights (no ML predictions)

### Timeout Configurations
```python
# Flask app timeouts
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Database connection timeout
engine = create_engine(database_url, pool_timeout=30, pool_recycle=3600)

# Request timeout for insights API
@app.route('/api/insights')
def api_insights():
    # Complex queries should complete within 10 seconds
    pass
```

### Performance Limits
- **Max Entries**: Optimized for up to 10,000 journal entries
- **Insights Calculation**: 30-day lookback performs best
- **CSV Export**: Large exports (>1MB) may timeout

## Copilot Agent Configuration

### Automation Capabilities
When operating in agent mode, Copilot can:

1. **Issue Management**: Automatically create issues for bugs found in tests
2. **Code Review**: Suggest improvements based on test coverage and code quality
3. **Dependency Updates**: Monitor and update package versions
4. **Documentation**: Auto-generate docstrings and update README
5. **Testing**: Create additional test cases for edge cases

### Smart Suggestions
Copilot excels at:
- **SQLAlchemy Queries**: Optimizing database queries and relationships
- **Flask Routing**: Suggesting RESTful API improvements
- **Data Analysis**: Enhancing insights calculations and statistics
- **Testing**: Generating comprehensive test scenarios
- **Error Handling**: Adding robust exception handling

### Repository Owner Configuration
For **lovetrulymichelle-tech** as repository owner:

1. **Enable Agent Mode**: 
   - Go to repository Settings → Copilot
   - Enable "Copilot agent assistance"
   - Set permissions for automated PRs and issue management

2. **Custom Instructions**: 
   - Focus on Python/Flask best practices
   - Prioritize data privacy and security
   - Maintain high test coverage (>95%)
   - Follow SQLAlchemy 2.0+ patterns

### Manual Validation Scenarios

Before accepting Copilot suggestions, validate:

1. **Database Changes**: Always test migrations on sample data
2. **API Modifications**: Verify backward compatibility
3. **Security Updates**: Review authentication and data access
4. **Performance Changes**: Benchmark insights calculations
5. **UI Changes**: Test responsive design on mobile

### Workflow Integration
```yaml
# Example: Auto-merge safe updates
on:
  pull_request:
    types: [opened]
    
jobs:
  copilot-review:
    if: github.actor == 'github-copilot[bot]'
    steps:
      - name: Auto-approve safe changes
        if: contains(github.event.pull_request.title, '[safe]')
        run: gh pr review --approve
```

## Contributing Guidelines

### Code Style
- Use Black for formatting (line length: 88)
- Follow PEP 8 naming conventions
- Type hints required for all public functions
- Docstrings for all classes and methods

### Git Workflow
```bash
# Feature development
git checkout -b feature/insights-enhancement
git commit -m "feat: add mood trend analysis"

# Bug fixes
git checkout -b fix/streak-calculation
git commit -m "fix: handle timezone edge cases in streak"
```

### Pull Request Process
1. Create feature branch from main
2. Add tests for new functionality
3. Ensure all tests pass and coverage >95%
4. Update documentation if needed
5. Request review from repository owner

## Support and Resources

### Getting Help
- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: GitHub Discussions for questions and ideas
- **Documentation**: Check README.md and inline code docs

### Useful Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/)
- [Python Packaging Guide](https://packaging.python.org/)

### Community
- Follow Python/Flask best practices
- Prioritize user privacy and data security
- Maintain backward compatibility when possible
- Document all breaking changes

---

*This repository is optimized for GitHub Copilot agent assistance. When in doubt, refer to test cases and existing code patterns for guidance.*