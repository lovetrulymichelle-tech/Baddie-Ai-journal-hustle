# Deployment Guide - Baddie AI Journal 🚀

This guide covers all deployment scenarios for the Baddie AI Journal application, from local development to production scaling for viral traffic.

## 🏃‍♀️ Quick Start

### Local Development
```bash
# Clone and setup
git clone https://github.com/lovetrulymichelle-tech/Baddie-Ai-journal-hustle.git
cd Baddie-Ai-journal-hustle

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Visit `http://localhost:5000` to access the dashboard.

### Testing the Application
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=baddie_journal --cov-report=html

# Run the insights preview
python preview_insights.py
```

## 🐳 Docker Deployment

### Build and Run with Docker
```bash
# Build the image
docker build -t baddie-ai-journal .

# Run the container
docker run -p 5000:5000 -e DATABASE_URL="sqlite:///journal.db" baddie-ai-journal

# Or with PostgreSQL
docker run -p 5000:5000 -e DATABASE_URL="postgresql://user:pass@host/db" baddie-ai-journal
```

### Docker Compose for Full Stack
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/baddie_journal
      - SECRET_KEY=your-production-secret-key
    depends_on:
      - db
      
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=baddie_journal
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## ☁️ Cloud Deployment

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create baddie-ai-journal-prod

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=postgres://...

# Deploy
git push heroku main

# Run database migrations
heroku run python -c "from baddie_journal.models import create_database_engine, create_tables; engine = create_database_engine(); create_tables(engine)"
```

### AWS Deployment (ECS/Fargate)
```yaml
# taskdefinition.json
{
  "family": "baddie-ai-journal",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "baddie-journal",
      "image": "your-registry/baddie-ai-journal:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ]
    }
  ]
}
```

### Google Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/baddie-ai-journal

# Deploy to Cloud Run
gcloud run deploy baddie-ai-journal \
  --image gcr.io/your-project/baddie-ai-journal \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://...
```

## 🗄️ Database Setup

### PostgreSQL (Recommended for Production)
```bash
# Create database
createdb baddie_journal

# Set environment variable
export DATABASE_URL="postgresql://user:password@localhost/baddie_journal"

# Create tables
python -c "from baddie_journal.models import create_database_engine, create_tables; engine = create_database_engine(); create_tables(engine)"
```

### Database Migrations
```python
# For schema changes, create migration scripts
from baddie_journal.models import create_database_engine, Base
from sqlalchemy import text

engine = create_database_engine()

# Example migration
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE journal_entries ADD COLUMN new_field VARCHAR(100)"))
    conn.commit()
```

## 🚀 Production Configuration

### Environment Variables
```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/database
SECRET_KEY=your-super-secret-key-min-32-chars

# Optional
FLASK_ENV=production
FLASK_DEBUG=false
REDIS_URL=redis://localhost:6379/0
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Security Hardening
```python
# Additional security headers
from flask_talisman import Talisman

app = create_app()
Talisman(app, force_https=True)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### Performance Optimization
```python
# Enable caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

# Database connection pooling
engine = create_engine(
    database_url,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300
)
```

## 📊 Monitoring & Logging

### Application Monitoring
```python
# Add Sentry for error tracking
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Health Checks
```bash
# Application health check
curl http://localhost:5000/api/health

# Database health check
python -c "from baddie_journal.models import create_database_engine; engine = create_database_engine(); print('Database OK' if engine.connect() else 'Database Error')"
```

### Log Management
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/baddie_journal.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

## 🌊 Scaling for Viral Traffic

### Load Balancing
```nginx
# nginx.conf
upstream baddie_journal {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name baddiejournal.ai;
    
    location / {
        proxy_pass http://baddie_journal;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Auto-Scaling with Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: baddie-journal
spec:
  replicas: 3
  selector:
    matchLabels:
      app: baddie-journal
  template:
    metadata:
      labels:
        app: baddie-journal
    spec:
      containers:
      - name: baddie-journal
        image: baddie-ai-journal:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url

---
apiVersion: v1
kind: Service
metadata:
  name: baddie-journal-service
spec:
  selector:
    app: baddie-journal
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### CDN Integration
```python
# Configure CDN for static assets
STATIC_URL_PATH = 'https://cdn.baddiejournal.ai/static'

# Set cache headers
@app.after_request
def after_request(response):
    if request.endpoint == 'static':
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response
```

## 🔒 Security Checklist

- [ ] HTTPS enabled with valid SSL certificate
- [ ] Environment variables for all secrets
- [ ] Database connection encrypted
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (using SQLAlchemy ORM)
- [ ] XSS protection headers
- [ ] CSRF protection enabled
- [ ] Regular security audits scheduled
- [ ] Backup and disaster recovery plan

## 📈 Performance Benchmarks

### Target Metrics
- **Response Time:** <200ms for API endpoints
- **Throughput:** 1000+ requests/second
- **Availability:** 99.9% uptime
- **Database:** <50ms query response time
- **Memory Usage:** <512MB per container

### Load Testing
```bash
# Install artillery
npm install -g artillery

# Create load test
cat > loadtest.yml << EOF
config:
  target: 'http://localhost:5000'
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: "Test insights API"
    requests:
      - get:
          url: "/api/insights"
EOF

# Run load test
artillery run loadtest.yml
```

## 🆘 Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check database connection
python -c "from baddie_journal.models import create_database_engine; create_database_engine().connect()"
```

#### High Memory Usage
```bash
# Monitor memory
ps aux | grep python

# Profile memory usage
pip install memory-profiler
python -m memory_profiler run.py
```

#### Database Connection Issues
```python
# Add connection retry logic
import time
from sqlalchemy.exc import OperationalError

def create_database_engine_with_retry(database_url, max_retries=5):
    for attempt in range(max_retries):
        try:
            engine = create_database_engine(database_url)
            engine.connect()
            return engine
        except OperationalError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

## 🎯 Go Live Checklist

- [ ] Production environment configured
- [ ] Database setup and migrated
- [ ] SSL certificate installed
- [ ] Environment variables set
- [ ] Monitoring and logging enabled
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated
- [ ] Team trained on deployment process

---

**Ready to launch? Let's change lives through AI-powered journaling! 🚀💪**

For deployment support, join our [Discord community](https://discord.gg/baddiejournal) or contact our DevOps team.