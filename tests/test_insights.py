from datetime import datetime, timedelta
import pytest

from app import app, db, Entry
from app import (
    compute_streak,
    daily_counts_last_n,
    mood_breakdown_last_30,
    category_breakdown_last_30,
    top_tags_last_60,
    totals,
)

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def _add_entry(days_ago=0, mood="neutral", tags="", category="Personal", text="test"):
    created = datetime.utcnow() - timedelta(days=days_ago)
    e = Entry(text=text, mood=mood, tags=tags, category=category, created_at=created)
    db.session.add(e)
    db.session.commit()
    return e

def test_streak_simple(client):
    # entries for today and yesterday -> streak 2
    _add_entry(days_ago=0)
    _add_entry(days_ago=1)
    assert compute_streak() == 2

def test_streak_missing_today(client):
    # entries for yesterday and day-before -> streak 2 (no today)
    _add_entry(days_ago=1)
    _add_entry(days_ago=2)
    assert compute_streak() == 2

def test_daily_counts(client):
    # day 0: 2 entries, day 1: 1 entry
    _add_entry(days_ago=0)
    _add_entry(days_ago=0)
    _add_entry(days_ago=1)
    counts = daily_counts_last_n(3)
    assert isinstance(counts, list) and len(counts) == 3
    total = sum(c for d, c in counts)
    assert total == 3

def test_mood_and_category_breakdowns(client):
    _add_entry(days_ago=0, mood="happy", category="Work")
    _add_entry(days_ago=0, mood="happy", category="Personal")
    _add_entry(days_ago=2, mood="stressed", category="Work")
    moods = dict(mood_breakdown_last_30())
    cats = dict(category_breakdown_last_30())
    assert moods.get("happy", 0) == 2
    assert cats.get("Work", 0) == 2

def test_top_tags(client):
    _add_entry(days_ago=0, tags="a,b")
    _add_entry(days_ago=10, tags="b,c")
    top = top_tags_last_60(limit=5)
    top_dict = dict(top)
    assert top_dict.get("b", 0) == 2
    assert top_dict.get("a", 0) == 1

def test_totals(client):
    _add_entry(days_ago=0)
    _add_entry(days_ago=8)  # outside 7-day window but inside 30-day
    last7, last30 = totals()
    assert last30 >= 2
    assert last7 >= 1

def test_flask_routes(client):
    """Test basic Flask routes work"""
    # Test home page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Baddie AI Journal Hustle' in response.data
    
    # Test insights page
    response = client.get('/insights')
    assert response.status_code == 200
    assert b'Journal Insights' in response.data
    
    # Test API endpoint
    response = client.get('/api/insights')
    assert response.status_code == 200
    assert response.is_json
    
    # Test adding entry
    response = client.post('/add_entry', data={
        'text': 'Test entry',
        'mood': 'happy',
        'category': 'Test',
        'tags': 'test,validation'
    })
    assert response.status_code == 200