#!/usr/bin/env python3
"""
Baddie AI Journal Hustle - Luxury Web Interface
A luxurious pink-themed journaling application with AI insights.
"""

import os
from datetime import datetime, UTC
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pathlib import Path

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'baddie-journal-secret-key-2024')

# Sample data for demonstration (will be replaced with actual database later)
sample_entries = [
    {
        'id': 1,
        'date': '2024-01-15',
        'content': 'Had an amazing day! Feeling grateful and motivated. ✨',
        'mood': 'happy',
        'category': 'personal',
        'tags': ['gratitude', 'motivation', 'success']
    },
    {
        'id': 2,
        'date': '2024-01-14',
        'content': 'Productive work session today. Accomplished all my goals! 💪',
        'mood': 'focused',
        'category': 'work',
        'tags': ['productivity', 'goals', 'achievement']
    },
    {
        'id': 3,
        'date': '2024-01-13',
        'content': 'Taking time for self-reflection and growth. Building my empire! 👑',
        'mood': 'contemplative',
        'category': 'personal',
        'tags': ['self-improvement', 'reflection', 'empire-building']
    }
]

@app.route('/')
def index():
    """Home page with journal entries."""
    return render_template('index.html', entries=sample_entries)

@app.route('/new-entry')
def new_entry():
    """Page to create a new journal entry."""
    return render_template('new_entry.html')

@app.route('/add-entry', methods=['POST'])
def add_entry():
    """Handle adding a new journal entry."""
    content = request.form.get('content')
    mood = request.form.get('mood')
    category = request.form.get('category')
    tags = request.form.get('tags', '').split(',')
    tags = [tag.strip() for tag in tags if tag.strip()]
    
    new_entry = {
        'id': len(sample_entries) + 1,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'content': content,
        'mood': mood,
        'category': category,
        'tags': tags
    }
    
    sample_entries.append(new_entry)
    flash('✨ Your journal entry has been added successfully! ✨', 'success')
    return redirect(url_for('index'))

@app.route('/insights')
def insights():
    """Insights dashboard with analytics."""
    # Calculate basic insights
    total_entries = len(sample_entries)
    mood_counts = {}
    category_counts = {}
    all_tags = []
    
    for entry in sample_entries:
        # Count moods
        mood = entry['mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        # Count categories
        category = entry['category']
        category_counts[category] = category_counts.get(category, 0) + 1
        
        # Collect all tags
        all_tags.extend(entry['tags'])
    
    # Count tag frequency
    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Get top tags
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    insights_data = {
        'total_entries': total_entries,
        'mood_breakdown': mood_counts,
        'category_breakdown': category_counts,
        'top_tags': top_tags,
        'current_streak': 3  # Mock data
    }
    
    return render_template('insights.html', insights=insights_data)

@app.route('/profile')
def profile():
    """User profile page."""
    return render_template('profile.html')

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)