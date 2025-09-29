# Quick Fix: Vercel 500 INTERNAL_SERVER_ERROR

## Problem
You're seeing this error on Vercel:
```
500: INTERNAL_SERVER_ERROR
Code: FUNCTION_INVOCATION_FAILED
```

## Root Cause
The application was not properly configured for Vercel's serverless architecture. The main issues were:

1. **Missing serverless handler** - Vercel needs a specific entry point (`api/index.py`)
2. **SQLite database incompatibility** - Serverless functions have ephemeral filesystems
3. **Database initialization timing** - Module-level initialization causes cold start problems

## ✅ Solution Applied

This repository now has **full Vercel serverless support** with the following changes:

### 1. Serverless Handler Created
- **File**: `api/index.py` 
- **Purpose**: WSGI entry point for Vercel's Python runtime
- **Action**: Imports and exposes the Flask application

### 2. Vercel Configuration Updated
- **File**: `vercel.json`
- **Changes**: 
  - Points to `api/index.py` as the entry point
  - Specifies Python 3.12
  - Configures proper routing

### 3. Lazy Database Initialization
- **File**: `app.py`
- **Changes**:
  - Database manager is now initialized on-demand via `get_db_manager()`
  - Prevents cold start issues in serverless environment
  - Still backward compatible with traditional deployments

### 4. Environment Warnings
- **File**: `database.py`
- **Changes**:
  - Detects when SQLite is used in Vercel environment
  - Warns users to switch to PostgreSQL
  - Prevents silent data loss

## 🚀 What You Need To Do

### Required: Set Up PostgreSQL Database

**Vercel REQUIRES a network database (PostgreSQL) for persistent storage.** Choose one of these free options:

1. **Vercel Postgres** (Recommended - easiest integration)
   - Go to your Vercel project → Storage → Create Database → Postgres
   - Copy the connection string

2. **Neon** (Free tier, serverless PostgreSQL)
   - Sign up at [neon.tech](https://neon.tech)
   - Create a database and copy the connection string

3. **Supabase** (Free tier)
   - Sign up at [supabase.com](https://supabase.com)
   - Create a project and get the connection string

4. **Railway** (Free tier)
   - Sign up at [railway.app](https://railway.app)
   - Add PostgreSQL plugin and get connection string

### Required: Set Environment Variable in Vercel

1. Go to your Vercel project dashboard
2. Settings → Environment Variables
3. Add this variable:
   ```
   SQLALCHEMY_DATABASE_URI = postgresql://user:password@host:port/database
   ```
   (Use the connection string from your chosen PostgreSQL provider)

4. Add a secret key (recommended):
   ```
   SECRET_KEY = your-random-secret-key-here
   ```

5. **Redeploy** your application after setting environment variables

### Verify It Works

After redeploying with the PostgreSQL connection string:

1. Visit: `https://your-app.vercel.app/health`
   - Should return: `{"status": "healthy", ...}`

2. Visit: `https://your-app.vercel.app/`
   - Should load the journal interface

3. Try adding a journal entry
   - Should persist across requests

## 📖 Full Documentation

For complete deployment instructions, see:
- **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)** - Comprehensive Vercel guide
- **[README.md](README.md)** - General deployment options

## ⚙️ Technical Details

### What Changed (For Developers)

1. **Module Structure**:
   ```
   api/
     └── index.py      # New: Vercel serverless entry point
   app.py              # Modified: Lazy database initialization
   database.py         # Modified: Vercel environment detection
   vercel.json         # Modified: Proper serverless configuration
   ```

2. **Database Pattern**:
   ```python
   # Before (causes issues in serverless)
   db_manager = DatabaseManager()
   
   # After (lazy initialization)
   db_manager = None
   def get_db_manager():
       global db_manager
       if db_manager is None:
           db_manager = DatabaseManager()
       return db_manager
   ```

3. **Backward Compatibility**:
   - ✅ Railway deployment still works (uses Procfile)
   - ✅ Heroku deployment still works (uses Procfile)
   - ✅ Local development still works (`python app.py`)
   - ✅ Docker deployment still works (uses Dockerfile)

## 🆘 Still Having Issues?

### Check Vercel Function Logs

1. Go to your Vercel project dashboard
2. Click on your latest deployment
3. Navigate to the "Functions" tab
4. Look for error messages

### Common Issues

**"Module not found" errors**:
- Ensure `requirements.txt` is present and complete
- Check that all files are committed to your repository

**"Database connection error"**:
- Verify `SQLALCHEMY_DATABASE_URI` is set in Vercel
- Test your PostgreSQL connection string locally first
- Ensure the database is accessible from the internet

**"Cold start timeout"**:
- This is normal for the first request after inactivity
- Subsequent requests will be faster
- Consider upgrading to Vercel Pro for better cold start performance

### Test Locally with PostgreSQL

```bash
# Set environment variable
export SQLALCHEMY_DATABASE_URI="postgresql://user:password@host:port/database"

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## Summary

✅ **What was fixed**:
- Added Vercel serverless support via `api/index.py`
- Implemented lazy database initialization
- Added environment detection and warnings
- Created comprehensive documentation

⚠️ **What you must do**:
- Set up PostgreSQL database (SQLite won't work)
- Add `SQLALCHEMY_DATABASE_URI` environment variable in Vercel
- Redeploy after adding environment variables

🎉 **Result**:
- Application will work properly on Vercel
- Data will persist across requests
- No more 500 errors
