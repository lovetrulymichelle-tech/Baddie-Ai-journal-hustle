# Quick Debugging Guide for 500 Errors

## ⚡ Quick Start

If you're seeing 500 errors in production, follow these steps:

### 1. Check Your Logs Immediately

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Docker:**
```bash
docker logs <container-name>
```

### 2. Look for ERROR Messages

Search for lines containing:
- `ERROR` - Critical errors with stack traces
- `500 Internal Server Error` - Specific 500 errors
- `Exception` - Python exceptions

Example:
```
2025-09-30 03:25:15,123 - app - ERROR - 500 Internal Server Error: Database connection failed
```

### 3. Common Issues & Quick Fixes

#### Database Connection Errors
**Log:**
```
ERROR - Database initialization error: could not connect to server
```
**Fix:**
- Check `SQLALCHEMY_DATABASE_URI` environment variable
- Verify PostgreSQL service is running
- Check database credentials

#### Missing Environment Variables
**Log:**
```
WARNING - SECRET_KEY - Not set (will use default)
```
**Fix:**
Set in your deployment platform:
```bash
# Railway
railway variables set SECRET_KEY=your-secure-key

# Heroku
heroku config:set SECRET_KEY=your-secure-key
```

#### Template Errors
**Log:**
```
ERROR - Error template rendering failed: TemplateNotFound: error.html
```
**Fix:**
- Ensure `templates/` directory is included in deployment
- Check that all template files exist
- Verify file permissions

#### Import Errors
**Log:**
```
ERROR - ImportError: No module named 'sqlalchemy'
```
**Fix:**
- Force redeploy to reinstall dependencies
- Verify `requirements.txt` is up to date
- Check that deployment picked up latest changes

### 4. Enable Debug Mode (Temporarily)

For more detailed error messages, set:
```bash
FLASK_DEBUG=true
```

⚠️ **WARNING:** Only use in development/testing, not production!

### 5. Test Health Endpoint

Check if basic functionality works:
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "Baddie AI Journal Hustle",
  "database": "connected",
  "entries_count": 10
}
```

### 6. Check Specific Routes

Test individual routes:
```bash
# Home page
curl -I https://your-app.railway.app/

# Insights
curl -I https://your-app.railway.app/insights

# API
curl https://your-app.railway.app/api/entries
```

## 📊 Log Levels Explained

- **INFO**: Normal operations (startup, connections)
- **WARNING**: Non-critical issues (404 errors, missing optional config)
- **ERROR**: Critical errors that need attention (500 errors, database failures)

## 🔍 Advanced Debugging

### Filter Logs by Level
```bash
# Railway - show only errors
railway logs | grep ERROR

# Heroku - show only errors
heroku logs --tail | grep ERROR
```

### Check Recent Errors
```bash
# Railway - last 100 lines
railway logs --tail 100

# Heroku - last 200 lines
heroku logs -n 200
```

### Follow Logs in Real-Time
```bash
# Railway
railway logs --follow

# Heroku
heroku logs --tail

# Docker
docker logs -f <container-name>
```

## 🚨 Emergency Checklist

When production is down:

1. [ ] Check deployment logs for errors
2. [ ] Verify all environment variables are set
3. [ ] Test health endpoint
4. [ ] Check database connectivity
5. [ ] Verify recent code changes didn't break anything
6. [ ] Check if dependencies were updated correctly
7. [ ] Review deployment configuration (Procfile, etc.)
8. [ ] Test locally with production settings
9. [ ] Check for resource limits (memory, CPU)
10. [ ] Review recent deployment timeline

## 📞 Getting Help

When reporting issues, include:
- Full error message from logs
- Stack trace (if available)
- Timestamp of the error
- Which route/endpoint failed
- Recent changes made
- Environment variables (don't include secrets!)

## 🎯 Prevention

- Always test locally before deploying
- Run `python check_deployment.py` before pushing
- Monitor logs after each deployment
- Set up health check monitoring
- Keep dependencies up to date
- Use staging environment for testing

---

**Remember:** With the new logging, you'll always see exactly what's wrong! 🎉
