# Deployment Policy - Baddie AI Journal Hustle

## ⚠️ IMPORTANT: Single Instance Policy

**This application should ONLY be deployed to ONE platform at a time.**

## Why This Matters

Having multiple deployments of the same journal application can cause:
- Data synchronization issues
- User confusion about which URL to use
- Unnecessary resource usage and costs
- Security concerns with multiple access points

## Supported Deployment Method

**✅ Railway Deployment (Recommended)**
- Configuration: `Procfile`
- Database: PostgreSQL (provided by Railway) or SQLite fallback
- Process: Automatic deployment via Railway's GitHub integration

## Previously Removed Configurations

The following deployment methods were removed to prevent dual deployments:
- ❌ Docker (`Dockerfile`) - Removed to prevent container deployment conflicts
- ❌ Vercel (`vercel.json`) - Removed to prevent serverless deployment conflicts  
- ❌ Domain setup for multiple platforms - Removed confusing documentation

## How to Deploy

1. **Choose Railway as your single deployment platform**
2. Connect your GitHub repository to Railway
3. Set required environment variables (`SECRET_KEY`)
4. Deploy using the existing `Procfile` configuration
5. **Do NOT deploy to additional platforms**

## If You Need to Change Deployment Platforms

1. **Fully shut down** the current deployment
2. Export any important data
3. Deploy to the new platform
4. Update DNS/domain settings to point to the new deployment
5. Verify the old deployment is completely offline

## Monitoring

- Use the `/health` endpoint to monitor your single deployment
- Set up monitoring alerts for your chosen platform only
- Regularly verify only one instance is running

## Verification Script

To verify your repository has a single deployment configuration:

```bash
python verify_single_deployment.py
```

This script will check for:
- ✅ Required Railway deployment files (Procfile, app.py, requirements.txt)
- ❌ Conflicting deployment files (Dockerfile, vercel.json, etc.)
- ✅ Deployment policy documentation

---

**Remember: One application, one deployment, one platform.**