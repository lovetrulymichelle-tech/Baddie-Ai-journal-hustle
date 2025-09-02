# Baddie AI Journal 🔥

An AI-powered journaling application with comprehensive insights and analytics to help you track patterns, moods, and productivity over time.

## Features

### 🔥 Insights Dashboard
- **Streaks:** Track consecutive days of journaling
- **Daily Counts:** Monitor journaling frequency over customizable time periods
- **Mood & Category Analytics:** Visualize emotional trends and category breakdowns
- **Tag Analytics:** Discover your most-used tags and topics
- **Comprehensive Metrics:** Total entries, unique tags/categories, and averages

### 📊 Data Export
- Export raw journal entries as CSV
- Export insights summary for analysis
- Privacy-focused: all data remains private

### 🚀 Modern Architecture
- Flask web application with responsive design
- SQLAlchemy ORM for database management
- RESTful API endpoints
- Comprehensive test suite (>95% coverage)
- Production-ready with Docker support

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle.git
cd Baddie-Ai-journal-hustle

# Install the application
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

### Running the Application
```bash
# Development server
python run.py

# Or using Flask CLI
export FLASK_APP=baddie_journal.app
flask run --debug
```

Visit `http://localhost:5000` to access the insights dashboard.

## API Usage

### Get Insights Data
```bash
curl http://localhost:5000/api/insights
```

### Export Data
```bash
# Export journal entries
curl http://localhost:5000/api/export/csv?type=entries -o entries.csv

# Export insights summary
curl http://localhost:5000/api/export/csv?type=summary -o summary.csv
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

## Programming Interface

### Core Models
```python
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper
from datetime import datetime

# Create journal entries
entries = [
    JournalEntry(
        id=1,
        content="Great day at work!",
        mood="happy",
        category="work",
        tags=["productivity", "achievement"],
        created_at=datetime.utcnow()
    )
]

# Analyze insights
data = InsightData(entries)
helper = InsightsHelper(data)

# Get analytics
print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")
print(f"Top tags: {helper.get_top_tags(10)}")
```

### Advanced Filtering
```python
# Filter by date range
recent_data = data.filter_by_date_range(
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31)
)

# Filter by mood or category
happy_entries = data.filter_by_mood("happy")
work_entries = data.filter_by_category("work")

# Export to CSV
csv_data = helper.export_to_csv()
summary_csv = helper.export_insights_summary_csv()
```

## Development

### Setup Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=baddie_journal --cov-report=html
```

### Code Quality
```bash
# Format code
black baddie_journal/ tests/

# Lint code
flake8 baddie_journal/ tests/

# Type checking
mypy baddie_journal/
```

### Database Management
```python
from baddie_journal.models import create_database_engine, create_tables

# Create database and tables
engine = create_database_engine("sqlite:///journal.db")
create_tables(engine)
```

## Production Deployment

### Docker
```bash
# Build image
docker build -t baddie-ai-journal .

# Run container
docker run -p 5000:5000 -e DATABASE_URL="sqlite:///journal.db" baddie-ai-journal
```

### Environment Variables
```bash
DATABASE_URL=sqlite:///journal.db  # or PostgreSQL URL
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

## Architecture

### Project Structure
```
baddie_journal/
├── models.py           # Database models and data classes
├── insights.py         # Analytics engine
├── app.py             # Flask application
└── templates/         # HTML templates

tests/                 # Comprehensive test suite
.github/              # CI/CD workflows and templates
```

### Database Schema
- **journal_entries**: Core table for journal data
  - id, content, mood, category, tags (JSON)
  - created_at, updated_at timestamps

### API Endpoints
- `GET /` - Dashboard interface
- `GET /api/insights` - Comprehensive analytics data
- `GET /api/export/csv` - Data export (entries or summary)
- `GET /api/health` - Health check

## Performance & Limits

### Optimizations
- Efficient date filtering for time-bounded queries
- Optimized insights calculations for up to 10,000 entries
- Database indexing on frequently queried fields
- Caching strategy for recent insights

### Current Limitations
- Single-user mode (no authentication system)
- Web-only interface (responsive design)
- 30-day lookback performs best for insights
- No real-time dashboard updates

## Contributing

We welcome contributions! Please see our comprehensive issue templates:
- 🐛 [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- ✨ [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)
- 📊 [Insights Enhancement](.github/ISSUE_TEMPLATE/insights_enhancement.md)

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass (>95% coverage)
5. Submit a pull request

## Copilot Integration

This repository is optimized for GitHub Copilot agent assistance:
- Comprehensive [Copilot instructions](.github/copilot-instructions.md)
- Automated code quality checks
- Smart suggestions for Python/Flask patterns
- Agent mode configuration for repository owner

## License

This project is open source. See LICENSE file for details.

## Support

- 📝 [GitHub Issues](https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle/issues)
- 💬 [GitHub Discussions](https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle/discussions)
- 📚 [Documentation](.github/copilot-instructions.md)

---

*Built with ❤️ for better self-reflection and personal growth through journaling.*