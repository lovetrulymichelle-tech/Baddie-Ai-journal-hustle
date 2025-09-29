# Vercel Deployment Guide

## Overview

This document provides instructions for deploying Baddie AI Journal Hustle to Vercel as a serverless application.

## Configuration Files

### vercel.json
The `vercel.json` file is configured for Vercel v2 with the following features:
- Uses `@vercel/python` builder
- Routes all requests to the serverless handler
- Sets appropriate environment variables
- Configures 30-second timeout for functions

### Serverless Handler
The `api/index.py` file serves as the entry point for Vercel:
- Imports the main Flask application
- Sets up proper Python path handling
- Configures serverless environment detection
- Exports the application for Vercel runtime

## Environment Variables

Set these in your Vercel dashboard:

### Required
- `SECRET_KEY` - Flask secret key for sessions
- `SQLALCHEMY_DATABASE_URI` - Database connection string (use Vercel Postgres or external)

### Optional
- `FLASK_DEBUG` - Set to "false" for production (default)
- `OPENAI_API_KEY` - For AI analysis features
- `STRIPE_SECRET_KEY` - For subscription payments
- `STRIPE_WEBHOOK_SECRET` - For webhook verification

## Deployment Steps

1. **Connect Repository**
   - Import your GitHub repository to Vercel
   - Vercel will automatically detect the `vercel.json` configuration

2. **Configure Environment Variables**
   - Go to Project Settings > Environment Variables
   - Add the required environment variables listed above

3. **Deploy**
   - Push to your main branch or manually trigger deployment
   - Vercel will build and deploy automatically

## Database Considerations

### For Production
- Use Vercel Postgres addon or external PostgreSQL database
- Set `SQLALCHEMY_DATABASE_URI` to your database connection string
- Example: `postgresql://user:password@host:port/database`

### For Development/Testing
- The app will fall back to SQLite if no database URI is provided
- This works for testing but is not recommended for production

## Health Check

After deployment, visit `/health` endpoint to verify:
- Application status
- Database connectivity
- Serverless environment detection
- Platform information

Example response:
```json
{
  "status": "healthy",
  "app": "Baddie AI Journal Hustle",
  "version": "0.1.0",
  "serverless": true,
  "platform": "preview",
  "database": "connected",
  "entries_count": 0
}
```

## Troubleshooting

### Common Issues

1. **500 INTERNAL_SERVER_ERROR**
   - Check environment variables are set correctly
   - Verify database connection string
   - Check Vercel function logs for detailed errors

2. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check that the Python path is set correctly in `api/index.py`

3. **Database Connection Issues**
   - Verify `SQLALCHEMY_DATABASE_URI` format
   - Ensure database server is accessible from Vercel
   - Check database credentials and permissions

### Debugging

1. **Check Function Logs**
   - Go to Vercel dashboard > Functions tab
   - View real-time logs during requests

2. **Test Locally**
   - Run `python api/index.py` to test the serverless handler
   - Use `python app.py` to test the main application

3. **Health Endpoint**
   - Visit `/health` to get diagnostic information
   - Check for any error messages or missing components

## Performance Optimization

- Vercel functions have a 30-second timeout limit
- Database connections are managed per request
- Consider implementing connection pooling for high traffic
- Static files are served directly by Vercel CDN

## Security Notes

- Never commit sensitive environment variables to the repository
- Use Vercel's environment variable management
- Set `FLASK_DEBUG=false` in production
- Ensure `SECRET_KEY` is cryptographically secure