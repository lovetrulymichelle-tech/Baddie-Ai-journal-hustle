## Insights Feature

The Insights feature provides analytics on your journal entries to help you track patterns, moods, and productivity over time.

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

### Interpreting Your Insights
- **Streaks:** Longer streaks mean more consistent journaling.
- **Mood breakdown:** Shows your emotional trends—use to spot highs/lows or triggers.
- **Top tags:** Reveals what topics or feelings dominate your journaling.

### Export & Privacy
- You can export your insights as a CSV.
- Analytics are private and visible only to you.

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

### Optional: Export/Import SQLite Data

If you're migrating from a local SQLite database:

1. **Export existing data:**
   ```bash
   # Create a backup of your SQLite data
   sqlite3 your_database.db .dump > backup.sql
   ```

2. **Prepare for PostgreSQL:**
   - Review the SQL dump file
   - Modify any SQLite-specific syntax for PostgreSQL compatibility
   - Consider using tools like `pgloader` for automated migration

3. **Import to PostgreSQL:**
   ```bash
   # Connect to your Railway PostgreSQL instance
   psql $DATABASE_URL < modified_backup.sql
   ```

4. **Verify data integrity:**
   - Check that all tables and data were imported correctly
   - Test application functionality with the migrated data

---

For questions, feedback, or to suggest new insights, open an issue or contact support.
