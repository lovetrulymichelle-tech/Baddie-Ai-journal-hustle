# Baddie AI Journal Hustle

[![CI](https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle/actions/workflows/ci.yml/badge.svg)](https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle/actions/workflows/ci.yml)

## 🆕 Swarms AI Integration

Baddie AI Journal Hustle now features **Swarms AI integration** for advanced journal analysis using multiple specialized AI agents!

### What is Swarms?
Swarms is a powerful multi-agent AI framework that enables multiple AI agents to work together on complex tasks. In our journal application, we use specialized agents to analyze different aspects of your journal entries.

### AI Agent Specialists
Our swarm includes four specialized agents:

1. **🧠 Mood Analyzer**: Expert at identifying emotional patterns, mood trends, and triggers
2. **🔍 Pattern Recognizer**: Specialist in behavioral patterns, habits, and recurring themes  
3. **🌱 Growth Coach**: Focused on personal development opportunities and achievements
4. **💡 Recommendation Specialist**: Generates actionable recommendations for improvement

### Quick Start with Swarms
```python
from baddie_journal import JournalAnalysisSwarm, JournalEntry, InsightData
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Create your journal data
entries = [
    JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.now(UTC)),
    # ... more entries
]
insight_data = InsightData(entries)

# Initialize and run the swarm
swarm = JournalAnalysisSwarm()
result = swarm.perform_comprehensive_analysis(insight_data)

# Get AI insights
print("🧠 Mood Analysis:", result.mood_analysis)
print("🔍 Pattern Insights:", result.pattern_insights)  
print("🌱 Growth Insights:", result.personal_growth_insights)
print("💡 Recommendations:", result.recommendations)
```

### Demo and Testing
- Run `python demo.py` for a complete demonstration
- Run `python test_swarms.py` to verify everything is working
- No API key? The demo will show basic insights without AI analysis

---

## Insights Feature

The Insights feature provides analytics on your journal entries to help you track patterns, moods, and productivity over time. **Enhanced with Swarms AI for deeper analysis!**

### What Insights Show You
- **Streaks:** See how many consecutive days you’ve written entries.
- **Daily Counts:** Track your journaling frequency over the last 30 days (customizable).
- **Mood & Category Breakdown:** Visualize the distribution of your moods and categories.
- **Top Tags:** Discover which tags you use most (set your own limit for top results).
- **Totals & Metrics:** Total entries, unique tags/categories, and average writing frequency.

### How It Works
- Data is analyzed in real-time from your journal entries.
- All times are stored and calculated in UTC (Coordinated Universal Time) for consistency across time zones.
- CSV export is available for deeper analysis or backup.

### Example Usage
```python
from datetime import datetime, UTC
from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper

# Sample entries
entries = [
    JournalEntry(1, "Great day!", "happy", "personal", ["motivation"], datetime.now(UTC)),
    JournalEntry(2, "Productive work", "focused", "work", ["productivity"], datetime.now(UTC))
]

helper = InsightsHelper(InsightData(entries))
print(f"Current streak: {helper.calculate_streak()} days")
print(f"Mood breakdown: {helper.get_mood_breakdown()}")
print(f"Top tags: {helper.get_top_tags(5)}")
```

### 🆕 Enhanced with Swarms AI
The insights are now enhanced with AI-powered analysis using our Swarms integration:

```python
# Advanced AI analysis
from baddie_journal import JournalAnalysisSwarm

swarm = JournalAnalysisSwarm()  # Requires OPENAI_API_KEY
result = swarm.perform_comprehensive_analysis(insight_data)

print("🧠 AI Mood Analysis:", result.mood_analysis)
print("🔍 Pattern Recognition:", result.pattern_insights)  
print("🌱 Growth Coaching:", result.personal_growth_insights)
print("💡 AI Recommendations:", result.recommendations)
```

### Interpreting Your Insights
- **Streaks:** Longer streaks mean more consistent journaling.
- **Mood breakdown:** Shows your emotional trends—use to spot highs/lows or triggers.
- **Top tags:** Reveals what topics or feelings dominate your journaling.

### Export & Privacy
- You can export your insights as a CSV.
- Analytics are private and visible only to you.

---

## 🐳 Docker Deployment

You can containerize the application using Docker for consistent deployment across environments.

### Building the Docker Image

```bash
# Build the Docker image
docker build -t baddie-journal .

# Run the container locally
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_DEBUG=false \
  -e SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host:port/db \
  baddie-journal
```

### Environment Variables for Docker

Set these environment variables when running the container:

- `SECRET_KEY`: A secure random string for session security
- `FLASK_DEBUG`: Set to `false` for production
- `SQLALCHEMY_DATABASE_URI`: Database connection string (PostgreSQL for production)
- `PORT`: Port to bind (default: 8000)

### Docker Compose Example

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secure-secret-key
      - FLASK_DEBUG=false
      - SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host:port/db
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=journal
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

The application will be available at `http://localhost:8000`.

---

## Deploy to Railway (Postgres)

This section provides step-by-step instructions for deploying the Baddie AI Journal to Railway with a PostgreSQL database.

### Prerequisites
- A Railway account (sign up at [railway.app](https://railway.app))
- Your application code in a Git repository
- Basic understanding of environment variables

### Step 1: Add PostgreSQL Driver and Confirm Requirements

1. **Verify the PostgreSQL driver is included** in your `requirements.txt`:
   ```
   psycopg2-binary>=2.9.0
   ```

2. **Confirm your requirements.txt** includes all necessary dependencies for your application.

### Step 2: Set Up Railway Project and PostgreSQL Plugin

1. **Create a new Railway project:**
   - Visit [railway.app](https://railway.app) and sign in
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Add PostgreSQL plugin:**
   - In your Railway project dashboard, click "New Service"
   - Select "Database" → "Add PostgreSQL"
   - Railway will automatically provision a PostgreSQL database

### Step 3: Configure Environment Variables

Set the following environment variables in your Railway project settings:

1. **SECRET_KEY**: A secure random string for your application
   ```
   SECRET_KEY=your-very-secure-random-key-here
   ```

2. **ADMIN_PASSWORD**: Password for admin access
   ```
   ADMIN_PASSWORD=your-secure-admin-password
   ```

3. **SQLALCHEMY_DATABASE_URI**: PostgreSQL connection string
   ```
   SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database
   ```
   
   **Important**: Use the `postgresql://` prefix (not `postgres://`) for proper SQLAlchemy compatibility.
   
   Railway will provide the database connection details in the PostgreSQL service variables. You can copy the connection string from the "Connect" tab of your PostgreSQL service.

### Step 4: Confirm Procfile

Ensure you have a `Procfile` in your project root:
```
web: python app.py
```

Or for Gunicorn (recommended for production):
```
web: gunicorn app:app
```

### Step 5: Deploy

1. **Connect your repository** to Railway (if not done in Step 2)
2. **Configure build settings** if needed (Railway usually auto-detects Python apps)
3. **Deploy** by pushing to your main branch or clicking "Deploy" in Railway
4. **Monitor the build logs** in Railway's dashboard

### Step 6: Verification Checklist

After deployment, verify your application is working:

- [ ] Application builds successfully (check Railway build logs)
- [ ] Database connection is established (no connection errors in logs)
- [ ] Application starts without errors
- [ ] Environment variables are properly set
- [ ] PostgreSQL service is running and accessible
- [ ] Application can create/read journal entries
- [ ] Admin functionality works with your set password

### Troubleshooting

**Common issues and solutions:**

1. **Database connection errors:**
   - Verify the `SQLALCHEMY_DATABASE_URI` uses `postgresql://` prefix (not `postgres://`)
   - Check that the database credentials are correct
   - Ensure the PostgreSQL service is running in Railway

2. **Build failures:**
   - Verify `psycopg2-binary` is spelled correctly in requirements.txt
   - Check that all dependencies are listed in requirements.txt
   - Review build logs for specific error messages

3. **Admin access issues:**
   - Confirm `ADMIN_PASSWORD` environment variable is set
   - Verify the password meets any complexity requirements
   - Check application logs for authentication errors

4. **Application won't start:**
   - Verify your `Procfile` command is correct
   - Check that your main application file exists
   - Review application logs for startup errors

### Migrate data from SQLite to PostgreSQL

If you're migrating from a local SQLite database to your Railway PostgreSQL instance, use the provided migration script to safely transfer your journal entries.

#### Prerequisites

The migration script requires `psycopg2-binary`, which is already listed in `requirements.txt`.

#### Step 1: Backup Your Local SQLite Database

Before starting migration, create a backup of your local SQLite database:

```bash
# Create a backup copy of your SQLite database
cp journal.db journal.db.backup

# Optional: Create a SQL dump as additional backup
sqlite3 journal.db .dump > journal_backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Step 2: Set Environment Variables

Set the required environment variables for source and destination databases:

```bash
# Source: Your local SQLite database
export SQLALCHEMY_DATABASE_URI_SRC="sqlite:///journal.db"

# Destination: Your Railway PostgreSQL database
# Replace with your actual Railway PostgreSQL connection string
export SQLALCHEMY_DATABASE_URI_DST="postgresql://username:password@host:port/database"
```

**Important:** Use the `postgresql://` prefix (not `postgres://`) for proper SQLAlchemy compatibility. You can find your Railway PostgreSQL connection string in the "Connect" tab of your PostgreSQL service.

#### Step 3: Perform a Dry Run

Before migrating actual data, perform a dry run to verify the migration will work correctly:

```bash
# Run the migration script in dry-run mode
python migrate_sqlite_to_postgres.py --dry-run
```

This will:
- Validate your database connections
- Show you exactly what data would be migrated
- Identify any potential issues without making changes

#### Step 4: Perform the Actual Migration

If the dry run completes successfully, perform the actual migration:

```bash
# Run the actual migration
python migrate_sqlite_to_postgres.py
```

The script will:
- Connect to both databases
- Migrate all tables and data from SQLite to PostgreSQL
- Provide a detailed summary of the migration results
- Handle any data type conversions automatically

#### Step 5: Verify Migration in Railway App

After migration completes successfully:

1. **Check the migration logs** for any warnings or errors
2. **Deploy your application** to Railway (if not already deployed)
3. **Test key functionality:**
   ```bash
   # If you have a command-line interface, test basic operations
   # Or access your deployed Railway app URL
   ```
4. **Verify your data:**
   - Check that all journal entries are present
   - Verify entry counts match between source and destination
   - Test creating new entries to ensure the database is working correctly
   - Confirm that insights and analytics reflect your migrated data

#### Example Migration Workflow

Here's a complete example workflow:

```bash
# 1. Backup your data
cp journal.db journal.db.backup

# 2. Set environment variables (replace with your actual values)
export SQLALCHEMY_DATABASE_URI_SRC="sqlite:///journal.db"
export SQLALCHEMY_DATABASE_URI_DST="postgresql://postgres:password@containers-us-west-123.railway.app:6543/railway"

# 3. Test with dry run
python migrate_sqlite_to_postgres.py --dry-run

# 4. Perform actual migration
python migrate_sqlite_to_postgres.py

# 5. Verify in your Railway app
# Visit your deployed app URL and test functionality
```

#### Troubleshooting Migration

**Common issues and solutions:**

1. **Environment variable errors:**
   - Ensure both `SQLALCHEMY_DATABASE_URI_SRC` and `SQLALCHEMY_DATABASE_URI_DST` are set
   - Verify the PostgreSQL URI uses `postgresql://` prefix (not `postgres://`)
   - Check that your Railway PostgreSQL credentials are correct

2. **Connection errors:**
   - Verify your local SQLite database file exists
   - Ensure your Railway PostgreSQL service is running
   - Test connectivity to Railway from your local machine

3. **Migration failures:**
   - Review the detailed error messages in the script output
   - Ensure your local SQLite database isn't corrupted
   - Try the dry run first to identify issues before actual migration

4. **Data verification issues:**
   - Compare row counts between source and destination
   - Check for any data type conversion issues
   - Verify that primary keys and relationships are preserved

---

## 🚀 Creating New Projects

Want to create a new repository for a related project or use this as a template?

See our comprehensive guide: **[CREATE_NEW_REPOSITORY_GUIDE.md](CREATE_NEW_REPOSITORY_GUIDE.md)**

This guide covers:
- Step-by-step repository creation on GitHub
- Using this repository as a template
- Best practices for naming and structuring projects
- How to fork or clone for new projects

---

For questions, feedback, or to suggest new insights, open an issue or contact support.
