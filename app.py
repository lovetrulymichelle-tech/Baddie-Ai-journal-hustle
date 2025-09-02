"""
Baddie AI Journal Hustle - Flask Application
Journal entries tracking with insights and analytics
"""
from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy import func
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Entry Model
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50), nullable=False, default='neutral')
    tags = db.Column(db.Text, default='')  # comma-separated tags
    category = db.Column(db.String(100), default='Personal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'mood': self.mood,
            'tags': self.tags.split(',') if self.tags else [],
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }

# Insights Functions
def compute_streak():
    """Calculate current journaling streak"""
    today = datetime.utcnow().date()
    current_date = today
    streak = 0
    
    while True:
        entries = Entry.query.filter(
            func.date(Entry.created_at) == current_date
        ).count()
        
        if entries > 0:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

def daily_counts_last_n(days=30):
    """Get daily entry counts for last N days"""
    results = []
    today = datetime.utcnow().date()
    
    for i in range(days):
        date = today - timedelta(days=i)
        count = Entry.query.filter(
            func.date(Entry.created_at) == date
        ).count()
        results.append((date.isoformat(), count))
    
    return results

def mood_breakdown_last_30():
    """Get mood breakdown for last 30 days"""
    cutoff = datetime.utcnow() - timedelta(days=30)
    entries = Entry.query.filter(Entry.created_at >= cutoff).all()
    moods = [entry.mood for entry in entries]
    return Counter(moods).most_common()

def category_breakdown_last_30():
    """Get category breakdown for last 30 days"""
    cutoff = datetime.utcnow() - timedelta(days=30)
    entries = Entry.query.filter(Entry.created_at >= cutoff).all()
    categories = [entry.category for entry in entries]
    return Counter(categories).most_common()

def top_tags_last_60(limit=10):
    """Get top tags for last 60 days"""
    cutoff = datetime.utcnow() - timedelta(days=60)
    entries = Entry.query.filter(Entry.created_at >= cutoff).all()
    all_tags = []
    for entry in entries:
        if entry.tags:
            all_tags.extend([tag.strip() for tag in entry.tags.split(',') if tag.strip()])
    return Counter(all_tags).most_common(limit)

def totals():
    """Get total counts for last 7 and 30 days"""
    cutoff_7 = datetime.utcnow() - timedelta(days=7)
    cutoff_30 = datetime.utcnow() - timedelta(days=30)
    
    last7 = Entry.query.filter(Entry.created_at >= cutoff_7).count()
    last30 = Entry.query.filter(Entry.created_at >= cutoff_30).count()
    
    return last7, last30

# Routes
@app.route('/')
def index():
    """Simple home page with basic functionality"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Baddie AI Journal Hustle</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; }
            input, textarea, select { width: 300px; padding: 8px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .insights { margin-top: 30px; }
            .stat { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
        </style>
    </head>
    <body>
        <h1>Baddie AI Journal Hustle</h1>
        
        <h2>Add New Entry</h2>
        <form action="/add_entry" method="post">
            <div class="form-group">
                <label>Entry Text:</label>
                <textarea name="text" rows="4" placeholder="Write your journal entry..."></textarea>
            </div>
            <div class="form-group">
                <label>Mood:</label>
                <select name="mood">
                    <option value="happy">Happy</option>
                    <option value="neutral" selected>Neutral</option>
                    <option value="sad">Sad</option>
                    <option value="excited">Excited</option>
                    <option value="stressed">Stressed</option>
                    <option value="focused">Focused</option>
                </select>
            </div>
            <div class="form-group">
                <label>Category:</label>
                <input type="text" name="category" value="Personal" />
            </div>
            <div class="form-group">
                <label>Tags (comma-separated):</label>
                <input type="text" name="tags" placeholder="motivation, work, health" />
            </div>
            <button type="submit">Add Entry</button>
        </form>
        
        <div class="insights">
            <h2>Quick Insights</h2>
            <div class="stat">Current Streak: {{ streak }} days</div>
            <div class="stat">Entries (Last 7 days): {{ last7 }}</div>
            <div class="stat">Entries (Last 30 days): {{ last30 }}</div>
        </div>
        
        <p><a href="/insights">View Full Insights →</a></p>
    </body>
    </html>
    """
    streak = compute_streak()
    last7, last30 = totals()
    return render_template_string(template, streak=streak, last7=last7, last30=last30)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    """Add a new journal entry"""
    entry = Entry(
        text=request.form.get('text', ''),
        mood=request.form.get('mood', 'neutral'),
        category=request.form.get('category', 'Personal'),
        tags=request.form.get('tags', '')
    )
    db.session.add(entry)
    db.session.commit()
    return f'<h2>Entry added successfully!</h2><p><a href="/">← Back to Home</a></p>'

@app.route('/insights')
def insights():
    """Display comprehensive insights"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Insights - Baddie AI Journal Hustle</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .stat { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
            .breakdown { display: flex; flex-wrap: wrap; gap: 15px; }
            .card { background: white; border: 1px solid #dee2e6; padding: 15px; border-radius: 5px; min-width: 200px; }
        </style>
    </head>
    <body>
        <h1>Journal Insights</h1>
        
        <div class="stat">Current Streak: {{ streak }} days</div>
        <div class="stat">Total Entries (Last 7 days): {{ last7 }}</div>
        <div class="stat">Total Entries (Last 30 days): {{ last30 }}</div>
        
        <div class="breakdown">
            <div class="card">
                <h3>Top Moods (Last 30 days)</h3>
                {% for mood, count in moods %}
                <p>{{ mood }}: {{ count }}</p>
                {% endfor %}
            </div>
            
            <div class="card">
                <h3>Top Categories (Last 30 days)</h3>
                {% for category, count in categories %}
                <p>{{ category }}: {{ count }}</p>
                {% endfor %}
            </div>
            
            <div class="card">
                <h3>Top Tags (Last 60 days)</h3>
                {% for tag, count in tags %}
                <p>{{ tag }}: {{ count }}</p>
                {% endfor %}
            </div>
        </div>
        
        <p><a href="/">← Back to Home</a></p>
    </body>
    </html>
    """
    streak = compute_streak()
    last7, last30 = totals()
    moods = mood_breakdown_last_30()
    categories = category_breakdown_last_30()
    tags = top_tags_last_60(5)
    
    return render_template_string(template, 
                                streak=streak, last7=last7, last30=last30,
                                moods=moods, categories=categories, tags=tags)

@app.route('/api/insights')
def api_insights():
    """API endpoint for insights data"""
    return jsonify({
        'streak': compute_streak(),
        'totals': totals(),
        'daily_counts': daily_counts_last_n(30),
        'mood_breakdown': mood_breakdown_last_30(),
        'category_breakdown': category_breakdown_last_30(),
        'top_tags': top_tags_last_60(10)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)