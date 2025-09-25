#!/usr/bin/env python3
"""
Baddie AI Journal Hustle - Flask Web Application
A luxurious pink and gold themed journaling web interface
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, Response

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'baddie-ai-journal-secret-key-2024')

# Initialize SQLite database
def init_db():
    """Initialize the SQLite database with journal entries table."""
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            mood TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_entries():
    """Get all journal entries from the database."""
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM journal_entries ORDER BY timestamp DESC')
    entries = cursor.fetchall()
    conn.close()
    return entries

def add_entry(content, mood, category, tags):
    """Add a new journal entry to the database."""
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO journal_entries (content, mood, category, tags, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (content, mood, category, json.dumps(tags), datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Flask Routes
@app.route('/')
def home():
    """Home page route."""
    return render_template_string(get_home_html())

@app.route('/journal')
def journal():
    """Journal page route."""
    entries = get_all_entries()
    return render_template_string(get_journal_html(entries))

@app.route('/insights')
def insights():
    """Insights page route."""
    entries = get_all_entries()
    return render_template_string(get_insights_html(entries))

@app.route('/about')
def about():
    """About page route."""
    return render_template_string(get_about_html())

@app.route('/static/style.css')
def css():
    """Serve CSS."""
    return Response(get_css_content(), mimetype='text/css')

@app.route('/static/script.js')
def js():
    """Serve JavaScript."""
    return Response(get_js_content(), mimetype='application/javascript')

@app.route('/api/add-entry', methods=['POST'])
def add_journal_entry():
    """Handle journal entry creation."""
    content = request.form.get('content', '').strip()
    mood = request.form.get('mood', '').strip()
    category = request.form.get('category', '').strip()
    tags_str = request.form.get('tags', '').strip()
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
    
    if content and mood and category:
        add_entry(content, mood, category, tags)
        return redirect(url_for('journal'))
    else:
        return "Missing required fields", 400

def get_base_html(title, content):
    """Get base HTML template with pink luxury theme."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Baddie AI Journal Hustle</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="/static/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">
                <i class="fas fa-crown"></i>
                <span>Baddie AI Journal</span>
            </div>
            <ul class="nav-menu">
                <li><a href="/" class="nav-link"><i class="fas fa-home"></i> Home</a></li>
                <li><a href="/journal" class="nav-link"><i class="fas fa-book"></i> Journal</a></li>
                <li><a href="/insights" class="nav-link"><i class="fas fa-chart-line"></i> Insights</a></li>
                <li><a href="/about" class="nav-link"><i class="fas fa-user"></i> About</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="main-content">
        {content}
    </main>
    
    <footer class="footer">
        <p>&copy; 2024 Baddie AI Journal Hustle - Elevate Your Mind ✨</p>
    </footer>
    
    <script src="/static/script.js"></script>
</body>
</html>
"""

def get_home_html():
    """Get home page HTML."""
    content = """
    <section class="hero">
        <div class="hero-content">
            <h1 class="hero-title">Welcome to Your <span class="highlight">Baddie AI</span> Journal</h1>
            <p class="hero-subtitle">Elevate your journaling experience with luxury design and AI-powered insights</p>
            <div class="hero-buttons">
                <a href="/journal" class="btn btn-primary">
                    <i class="fas fa-pen-fancy"></i> Start Journaling
                </a>
                <a href="/insights" class="btn btn-secondary">
                    <i class="fas fa-chart-bar"></i> View Insights
                </a>
            </div>
        </div>
    </section>
    
    <section class="features">
        <div class="container">
            <h2 class="section-title">Luxurious Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3>AI-Powered Insights</h3>
                    <p>Get intelligent analysis of your mood patterns and personal growth</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-gem"></i>
                    </div>
                    <h3>Luxury Design</h3>
                    <p>Experience journaling in style with our pink and gold aesthetic</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>Progress Tracking</h3>
                    <p>Monitor your journaling streaks and emotional wellness trends</p>
                </div>
            </div>
        </div>
    </section>
    """
    return get_base_html("Home", content)

def get_journal_html(entries):
    """Get journal page HTML."""
    entries_html = ""
    if entries:
        for entry in entries:
            tags = json.loads(entry[4]) if entry[4] else []
            tags_html = " ".join([f'<span class="tag">#{tag}</span>' for tag in tags])
            entries_html += f"""
            <div class="journal-entry">
                <div class="entry-header">
                    <span class="entry-mood mood-{entry[2].lower()}">{entry[2].title()}</span>
                    <span class="entry-category">{entry[3].title()}</span>
                    <span class="entry-date">{entry[5][:10]}</span>
                </div>
                <div class="entry-content">{entry[1]}</div>
                <div class="entry-tags">{tags_html}</div>
            </div>
            """
    else:
        entries_html = '<p class="no-entries">No journal entries yet. Start writing your first entry!</p>'
    
    content = f"""
    <div class="container">
        <div class="page-header">
            <h1><i class="fas fa-book"></i> My Journal</h1>
            <button class="btn btn-primary" onclick="toggleNewEntryForm()">
                <i class="fas fa-plus"></i> New Entry
            </button>
        </div>
        
        <div id="newEntryForm" class="new-entry-form" style="display: none;">
            <form method="POST" action="/api/add-entry">
                <div class="form-group">
                    <label for="content">What's on your mind?</label>
                    <textarea id="content" name="content" placeholder="Share your thoughts..." required></textarea>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="mood">Mood</label>
                        <select id="mood" name="mood" required>
                            <option value="">Select mood</option>
                            <option value="happy">😊 Happy</option>
                            <option value="sad">😢 Sad</option>
                            <option value="excited">🤩 Excited</option>
                            <option value="stressed">😰 Stressed</option>
                            <option value="calm">😌 Calm</option>
                            <option value="grateful">🙏 Grateful</option>
                            <option value="motivated">💪 Motivated</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="category">Category</label>
                        <select id="category" name="category" required>
                            <option value="">Select category</option>
                            <option value="personal">Personal</option>
                            <option value="work">Work</option>
                            <option value="goals">Goals</option>
                            <option value="relationships">Relationships</option>
                            <option value="health">Health</option>
                            <option value="reflection">Reflection</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label for="tags">Tags (comma-separated)</label>
                    <input type="text" id="tags" name="tags" placeholder="motivation, growth, success">
                </div>
                <div class="form-buttons">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Save Entry
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="toggleNewEntryForm()">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
        
        <div class="journal-entries">
            {entries_html}
        </div>
    </div>
    """
    return get_base_html("Journal", content)

def get_insights_html(entries):
    """Get insights page HTML."""
    total_entries = len(entries)
    moods = {}
    categories = {}
    
    for entry in entries:
        mood = entry[2]
        category = entry[3]
        moods[mood] = moods.get(mood, 0) + 1
        categories[category] = categories.get(category, 0) + 1
    
    mood_stats = ""
    for mood, count in moods.items():
        percentage = (count / total_entries * 100) if total_entries > 0 else 0
        mood_stats += f'<div class="stat-item"><span class="stat-label">{mood.title()}</span><span class="stat-value">{count} ({percentage:.1f}%)</span></div>'
    
    category_stats = ""
    for category, count in categories.items():
        percentage = (count / total_entries * 100) if total_entries > 0 else 0
        category_stats += f'<div class="stat-item"><span class="stat-label">{category.title()}</span><span class="stat-value">{count} ({percentage:.1f}%)</span></div>'
    
    content = f"""
    <div class="container">
        <div class="page-header">
            <h1><i class="fas fa-chart-line"></i> Your Insights</h1>
        </div>
        
        <div class="insights-grid">
            <div class="insight-card">
                <div class="insight-header">
                    <h3><i class="fas fa-book"></i> Total Entries</h3>
                </div>
                <div class="insight-value">{total_entries}</div>
                <p class="insight-description">Journal entries written</p>
            </div>
            
            <div class="insight-card">
                <div class="insight-header">
                    <h3><i class="fas fa-heart"></i> Mood Distribution</h3>
                </div>
                <div class="insight-stats">
                    {mood_stats if mood_stats else '<p>No mood data available</p>'}
                </div>
            </div>
            
            <div class="insight-card">
                <div class="insight-header">
                    <h3><i class="fas fa-tags"></i> Categories</h3>
                </div>
                <div class="insight-stats">
                    {category_stats if category_stats else '<p>No category data available</p>'}
                </div>
            </div>
            
            <div class="insight-card">
                <div class="insight-header">
                    <h3><i class="fas fa-fire"></i> Writing Streak</h3>
                </div>
                <div class="insight-value">1</div>
                <p class="insight-description">Days in a row</p>
            </div>
        </div>
    </div>
    """
    return get_base_html("Insights", content)

def get_about_html():
    """Get about page HTML."""
    content = """
    <div class="container">
        <div class="page-header">
            <h1><i class="fas fa-user"></i> About Baddie AI Journal</h1>
        </div>
        
        <div class="about-content">
            <div class="about-section">
                <h2>Elevate Your Journaling Experience</h2>
                <p>Baddie AI Journal Hustle is more than just a journaling app – it's your personal growth companion designed with luxury and elegance in mind. Our pink and gold aesthetic creates a premium experience that makes you feel like the baddie you are.</p>
            </div>
            
            <div class="about-section">
                <h2>Features</h2>
                <ul class="feature-list">
                    <li><i class="fas fa-pen-fancy"></i> Luxurious writing experience</li>
                    <li><i class="fas fa-brain"></i> AI-powered mood analysis</li>
                    <li><i class="fas fa-chart-line"></i> Personal growth insights</li>
                    <li><i class="fas fa-gem"></i> Premium pink & gold design</li>
                    <li><i class="fas fa-mobile-alt"></i> Mobile responsive</li>
                </ul>
            </div>
            
            <div class="about-section">
                <h2>Your Privacy Matters</h2>
                <p>All your journal entries are stored securely and privately. Your thoughts and feelings are yours alone – we respect and protect your privacy.</p>
            </div>
        </div>
    </div>
    """
    return get_base_html("About", content)

def get_css_content():
    """Get CSS content for the luxury pink and gold theme."""
    return """
/* Baddie AI Journal - Luxury Pink & Gold Theme */
:root {
    --pink-primary: #FF69B4;
    --pink-secondary: #FFB6C1;
    --pink-light: #FFC0CB;
    --pink-dark: #C71585;
    --gold: #FFD700;
    --gold-dark: #B8860B;
    --white: #FFFFFF;
    --cream: #FFF8DC;
    --gray-light: #F5F5F5;
    --gray-medium: #808080;
    --gray-dark: #333333;
    --shadow-light: 0 2px 10px rgba(255, 105, 180, 0.1);
    --shadow-medium: 0 4px 20px rgba(255, 105, 180, 0.2);
    --shadow-strong: 0 8px 30px rgba(255, 105, 180, 0.3);
    --gradient-pink: linear-gradient(135deg, #FF69B4, #FFB6C1);
    --gradient-gold: linear-gradient(135deg, #FFD700, #FFA500);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: var(--gray-dark);
    background: linear-gradient(135deg, #FFF0F5, #FFE4E1);
    min-height: 100vh;
}

/* Typography */
.hero-title, h1, h2 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: var(--gradient-pink);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 1rem;
}

.highlight {
    color: var(--gold);
    text-shadow: 2px 2px 4px rgba(255, 215, 0, 0.3);
}

/* Navigation */
.navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow-light);
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.nav-brand {
    display: flex;
    align-items: center;
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--pink-primary);
}

.nav-brand i {
    color: var(--gold);
    margin-right: 0.5rem;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-link {
    text-decoration: none;
    color: var(--gray-dark);
    font-weight: 500;
    transition: all 0.3s ease;
    padding: 0.5rem 1rem;
    border-radius: 25px;
}

.nav-link:hover {
    color: var(--pink-primary);
    background: rgba(255, 105, 180, 0.1);
}

.nav-link i {
    margin-right: 0.5rem;
}

/* Main Content */
.main-content {
    min-height: calc(100vh - 120px);
    padding: 2rem 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 4rem 2rem;
    background: var(--gradient-pink);
    margin-bottom: 3rem;
    border-radius: 20px;
    box-shadow: var(--shadow-strong);
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="diamonds" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><polygon points="10,2 18,10 10,18 2,10" fill="rgba(255,215,0,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23diamonds)"/></svg>');
    opacity: 0.3;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: var(--white);
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    padding: 1rem 2rem;
    border: none;
    border-radius: 30px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-light);
}

.btn i {
    margin-right: 0.5rem;
}

.btn-primary {
    background: var(--gradient-gold);
    color: var(--gray-dark);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-medium);
}

.btn-secondary {
    background: var(--white);
    color: var(--pink-primary);
    border: 2px solid var(--pink-primary);
}

.btn-secondary:hover {
    background: var(--pink-primary);
    color: var(--white);
    transform: translateY(-2px);
}

/* Features Section */
.features {
    padding: 3rem 0;
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    color: var(--pink-primary);
    margin-bottom: 3rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.feature-card {
    background: var(--white);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: var(--shadow-light);
    text-align: center;
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-medium);
}

.feature-icon {
    width: 80px;
    height: 80px;
    background: var(--gradient-pink);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    color: var(--white);
    font-size: 2rem;
}

.feature-card h3 {
    color: var(--pink-primary);
    margin-bottom: 1rem;
}

/* Page Header */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--pink-light);
}

.page-header h1 {
    color: var(--pink-primary);
    font-size: 2.5rem;
}

/* Forms */
.new-entry-form {
    background: var(--white);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: var(--shadow-light);
    margin-bottom: 2rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--pink-primary);
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 1rem;
    border: 2px solid var(--pink-light);
    border-radius: 10px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--pink-primary);
    box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.1);
}

.form-group textarea {
    min-height: 150px;
    resize: vertical;
}

.form-buttons {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
}

/* Journal Entries */
.journal-entries {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.journal-entry {
    background: var(--white);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: var(--shadow-light);
    transition: transform 0.2s ease;
}

.journal-entry:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow-medium);
}

.entry-header {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}

.entry-mood {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
    background: var(--gradient-pink);
    color: var(--white);
}

.entry-category {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    background: var(--gradient-gold);
    color: var(--gray-dark);
    font-weight: 600;
    font-size: 0.9rem;
}

.entry-date {
    color: var(--gray-medium);
    font-size: 0.9rem;
    margin-left: auto;
}

.entry-content {
    margin-bottom: 1rem;
    line-height: 1.6;
    color: var(--gray-dark);
}

.entry-tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.tag {
    background: rgba(255, 105, 180, 0.1);
    color: var(--pink-primary);
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
}

/* Insights */
.insights-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.insight-card {
    background: var(--white);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: var(--shadow-light);
    text-align: center;
}

.insight-header {
    margin-bottom: 1rem;
}

.insight-header h3 {
    color: var(--pink-primary);
    font-size: 1.2rem;
}

.insight-value {
    font-size: 3rem;
    font-weight: 900;
    color: var(--gold);
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(255, 215, 0, 0.2);
}

.insight-description {
    color: var(--gray-medium);
    font-size: 0.9rem;
}

.insight-stats {
    text-align: left;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--gray-light);
}

.stat-label {
    font-weight: 500;
}

.stat-value {
    color: var(--pink-primary);
    font-weight: 600;
}

/* About Page */
.about-content {
    max-width: 800px;
    margin: 0 auto;
}

.about-section {
    background: var(--white);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: var(--shadow-light);
    margin-bottom: 2rem;
}

.about-section h2 {
    color: var(--pink-primary);
    margin-bottom: 1rem;
}

.feature-list {
    list-style: none;
    padding-left: 0;
}

.feature-list li {
    padding: 0.5rem 0;
    color: var(--gray-dark);
}

.feature-list li i {
    color: var(--gold);
    margin-right: 0.5rem;
}

/* Footer */
.footer {
    background: var(--gradient-pink);
    color: var(--white);
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .nav-container {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }
    
    .nav-menu {
        gap: 1rem;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .form-row {
        grid-template-columns: 1fr;
    }
    
    .page-header {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
    }
    
    .entry-header {
        justify-content: center;
        text-align: center;
    }
    
    .entry-date {
        margin-left: 0;
    }
    
    .container {
        padding: 0 1rem;
    }
}

@media (max-width: 480px) {
    .hero-title {
        font-size: 2rem;
    }
    
    .section-title {
        font-size: 2rem;
    }
    
    .page-header h1 {
        font-size: 2rem;
    }
    
    .nav-menu {
        flex-direction: column;
        text-align: center;
    }
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.feature-card,
.journal-entry,
.insight-card {
    animation: fadeInUp 0.6s ease;
}

.no-entries {
    text-align: center;
    color: var(--gray-medium);
    font-style: italic;
    padding: 3rem;
    background: var(--white);
    border-radius: 15px;
    box-shadow: var(--shadow-light);
}
"""

def get_js_content():
    """Get JavaScript content for interactivity."""
    return """
// Baddie AI Journal - JavaScript functionality

function toggleNewEntryForm() {
    const form = document.getElementById('newEntryForm');
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
        form.scrollIntoView({ behavior: 'smooth' });
    } else {
        form.style.display = 'none';
    }
}

// Add smooth scrolling to all links
document.addEventListener('DOMContentLoaded', function() {
    // Add entrance animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    // Observe all cards
    const cards = document.querySelectorAll('.feature-card, .journal-entry, .insight-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // Add floating animation to hero elements
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        setInterval(() => {
            heroTitle.style.transform = 'scale(1.02)';
            setTimeout(() => {
                heroTitle.style.transform = 'scale(1)';
            }, 1000);
        }, 3000);
    }
    
    // Add sparkle effect on button hover
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.filter = 'brightness(1.1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.filter = 'brightness(1)';
        });
    });
});

// Form validation and enhancement
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[action="/api/add-entry"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            const content = document.getElementById('content').value.trim();
            const mood = document.getElementById('mood').value;
            const category = document.getElementById('category').value;
            
            if (!content || !mood || !category) {
                e.preventDefault();
                alert('Please fill in all required fields!');
                return;
            }
            
            // Add success animation
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.innerHTML = '<i class="fas fa-check"></i> Saving...';
            submitBtn.disabled = true;
        });
    }
});

// Add typing effect to hero subtitle
document.addEventListener('DOMContentLoaded', function() {
    const subtitle = document.querySelector('.hero-subtitle');
    if (subtitle) {
        const text = subtitle.textContent;
        subtitle.textContent = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                subtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        
        setTimeout(typeWriter, 1000);
    }
});
"""

# Initialize database when the module loads
init_db()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)