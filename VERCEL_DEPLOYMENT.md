# Vercel Serverless Deployment Guide

## Overview

This Flask application has been configured to work with Vercel's serverless Python runtime. However, there are important considerations and requirements for successful deployment.

## ⚠️ Important Serverless Considerations

### Database Requirements

**Vercel serverless functions have ephemeral filesystems** - any files written during function execution are lost when the function terminates. This means:

- ❌ **SQLite will NOT work reliably** in serverless mode (data will be lost between requests)
- ✅ **PostgreSQL or other network databases are REQUIRED** for persistent storage

### Required Environment Variables

You **MUST** set the following environment variable in your Vercel project:

```
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/database
```

**Where to get a PostgreSQL database:**
- [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres) (easiest, integrated with Vercel)
- [Neon](https://neon.tech/) (free tier available, serverless PostgreSQL)
- [Supabase](https://supabase.com/) (free tier available)
- [Railway](https://railway.app/) (free tier available)
- [ElephantSQL](https://www.elephantsql.com/) (free tier available)

### Recommended Environment Variables

```bash
SECRET_KEY=your-very-secure-random-key-here
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/database
FLASK_DEBUG=false
```

## Deployment Steps

### 1. Prerequisites

- Vercel account ([signup at vercel.com](https://vercel.com))
- PostgreSQL database (see options above)
- Git repository connected to Vercel

### 2. Configure Your PostgreSQL Database

Choose one of the database providers and get your connection string. Example with Vercel Postgres:

1. Go to your Vercel project dashboard
2. Navigate to "Storage" tab
3. Click "Create Database" → "Postgres"
4. Copy the connection string (starts with `postgresql://`)

### 3. Set Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to "Settings" → "Environment Variables"
3. Add the following variables:

   ```
   SQLALCHEMY_DATABASE_URI = postgresql://...
   SECRET_KEY = <generate-a-random-string>
   ```

4. Save the changes

### 4. Deploy

Push your code to GitHub/GitLab/Bitbucket, and Vercel will automatically deploy:

```bash
git add .
git commit -m "Configure for Vercel serverless deployment"
git push origin main
```

Or deploy using Vercel CLI:

```bash
vercel --prod
```

## Verifying Deployment

After deployment, test these endpoints:

1. **Health Check**: `https://your-app.vercel.app/health`
   - Should return `{"status": "healthy", ...}`

2. **Home Page**: `https://your-app.vercel.app/`
   - Should load the journal interface

3. **API Endpoint**: `https://your-app.vercel.app/api/entries`
   - Should return JSON array of entries

## Architecture

The application uses the following structure for Vercel:

```
.
├── api/
│   └── index.py          # Vercel serverless handler (WSGI entry point)
├── app.py                # Flask application (can still run locally)
├── database.py           # Database layer with PostgreSQL support
├── vercel.json           # Vercel configuration
└── requirements.txt      # Python dependencies
```

### How It Works

1. **Vercel routes all requests** to `api/index.py`
2. **`api/index.py` imports** the Flask app from `app.py`
3. **Vercel's Python runtime** executes the Flask app as a serverless function
4. **Database connections** are made on-demand (lazy initialization)
5. **PostgreSQL stores** all persistent data

## Troubleshooting

### Error: "500 INTERNAL_SERVER_ERROR"

**Cause**: Missing or invalid database configuration

**Solution**: 
1. Verify `SQLALCHEMY_DATABASE_URI` is set in Vercel environment variables
2. Ensure the database URL is valid and accessible from Vercel's infrastructure
3. Check Vercel function logs for detailed error messages

### Error: "Data disappears between requests"

**Cause**: Using SQLite in serverless mode

**Solution**: Switch to PostgreSQL by setting `SQLALCHEMY_DATABASE_URI`

### Error: "Module not found"

**Cause**: Missing dependencies in `requirements.txt`

**Solution**: Ensure all dependencies are listed in `requirements.txt`

### Viewing Logs

1. Go to your Vercel project dashboard
2. Click on a deployment
3. Navigate to the "Functions" tab
4. Click on a function to see its logs

## Performance Considerations

### Cold Starts

Serverless functions experience "cold starts" - the first request after inactivity takes longer. To minimize this:

- Keep the application lightweight
- Use connection pooling for database connections
- Consider using Vercel's edge network features

### Database Connections

- The app uses lazy initialization to create database connections only when needed
- Connections are properly closed after each request
- Consider using PgBouncer or similar connection pooler for high traffic

## Local Development

You can still run the app locally using the traditional method:

```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SQLALCHEMY_DATABASE_URI="postgresql://..."
export SECRET_KEY="your-secret-key"

# Run locally
python app.py
```

## Migration from SQLite to PostgreSQL

If you have existing SQLite data, use the migration script:

```bash
# Set source (SQLite) and destination (PostgreSQL) URLs
export SQLALCHEMY_DATABASE_URI_SRC="sqlite:///journal.db"
export SQLALCHEMY_DATABASE_URI_DST="postgresql://..."

# Run migration
python migrate_sqlite_to_postgres.py
```

## Alternative: Traditional Server Deployment

If you prefer traditional server-based deployment instead of serverless, consider:

- **Railway**: Uses `Procfile` with Gunicorn (already configured)
- **Heroku**: Uses `Procfile` with Gunicorn (already configured)
- **DigitalOcean App Platform**: Compatible with current setup
- **AWS Elastic Beanstalk**: Compatible with current setup

These platforms don't have the SQLite limitation and can use the filesystem.

## Support

For issues related to:
- **Vercel deployment**: Check [Vercel Documentation](https://vercel.com/docs)
- **PostgreSQL setup**: Check your database provider's documentation
- **Application bugs**: Open an issue on the GitHub repository

## Summary

✅ **Vercel deployment requires:**
1. PostgreSQL database (not SQLite)
2. `SQLALCHEMY_DATABASE_URI` environment variable set
3. Code pushed to Git repository connected to Vercel

❌ **What won't work:**
1. SQLite database in serverless mode
2. File-based sessions or storage
3. Long-running background tasks (use external services)
