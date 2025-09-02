"""Tests for the Flask application."""

import pytest
import json
from baddie_journal.app import create_app


@pytest.fixture
def app():
    """Create test Flask app."""
    app = create_app({
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///:memory:'
    })
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestFlaskApp:
    """Test cases for Flask application."""
    
    def test_dashboard_route(self, client):
        """Test dashboard route returns HTML."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Baddie AI Journal' in response.data
        assert b'Insights Dashboard' in response.data
    
    def test_api_insights_route(self, client):
        """Test insights API endpoint."""
        response = client.get('/api/insights')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Check required keys are present
        required_keys = ['streak', 'daily_counts', 'mood_breakdown', 
                        'category_breakdown', 'top_tags', 'metrics', 'mood_trends']
        for key in required_keys:
            assert key in data
        
        # Check data types
        assert isinstance(data['streak'], int)
        assert isinstance(data['daily_counts'], dict)
        assert isinstance(data['mood_breakdown'], dict)
        assert isinstance(data['category_breakdown'], dict)
        assert isinstance(data['top_tags'], list)
        assert isinstance(data['metrics'], dict)
        assert isinstance(data['mood_trends'], dict)
    
    def test_export_csv_entries(self, client):
        """Test CSV export for entries."""
        response = client.get('/api/export/csv?type=entries')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert 'attachment' in response.headers['Content-Disposition']
        
        # Check CSV content
        csv_content = response.data.decode('utf-8')
        assert 'Entry ID' in csv_content
        assert 'Content' in csv_content
        assert 'Mood' in csv_content
    
    def test_export_csv_summary(self, client):
        """Test CSV export for insights summary."""
        response = client.get('/api/export/csv?type=summary')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert 'attachment' in response.headers['Content-Disposition']
        
        # Check CSV content
        csv_content = response.data.decode('utf-8')
        assert 'Current Streak' in csv_content
        assert 'Total Entries' in csv_content
        assert 'Mood Breakdown' in csv_content
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['version'] == '0.1.0'