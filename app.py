#!/usr/bin/env python3
"""
Minimal Flask web application for Baddie AI Journal Hustle.

This creates a deployable web interface around the existing journaling functionality.
"""

import os
import sys
from datetime import datetime, UTC

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

    FLASK_AVAILABLE = True
except ImportError:
    print("Flask is required for web deployment. Install with: pip install flask")
    sys.exit(1)

from baddie_journal.models import JournalEntry, InsightData
from baddie_journal.insights import InsightsHelper
from database import DatabaseManager

# Initialize database manager
try:
    db_manager = DatabaseManager()
    print("✅ Database manager initialized successfully")
except Exception:
    print("⚠️ Database initialization error - using fallback storage")
    # Fallback to in-memory storage
    from database import DatabaseManager

    db_manager = DatabaseManager()


# Sample data for demonstration - only add if no entries exist
def create_sample_entries():
    """Create some sample entries if none exist."""
    if db_manager.get_entry_count() == 0:
        sample_data = [
            {
                "content": "Started my morning with meditation and journaling. Feeling grateful for this new day!",
                "mood": "grateful",
                "category": "personal",
                "tags": ["meditation", "gratitude", "morning"],
            },
            {
                "content": "Had a productive work session today. Completed three major tasks and felt really focused.",
                "mood": "productive",
                "category": "work",
                "tags": ["productivity", "focus", "achievement"],
            },
            {
                "content": "Feeling a bit overwhelmed with all the upcoming deadlines. Need to prioritize better.",
                "mood": "stressed",
                "category": "work",
                "tags": ["stress", "deadlines", "planning"],
            },
        ]

        for data in sample_data:
            db_manager.add_entry(
                content=data["content"],
                mood=data["mood"],
                category=data["category"],
                tags=data["tags"],
            )
        print(f"✅ Created {len(sample_data)} sample entries")


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "baddie-journal-demo-key-change-in-production")


@app.route("/")
def home():
    """Home page with journal entry form and recent entries."""
    create_sample_entries()  # Ensure we have some demo data
    all_entries = db_manager.get_all_entries()
    recent_entries = all_entries[:5]  # Show last 5 entries
    return render_template("index.html", entries=recent_entries)


@app.route("/add_entry", methods=["POST"])
def add_entry():
    """Add a new journal entry."""

    content = request.form.get("content", "").strip()
    mood = request.form.get("mood", "").strip()
    category = request.form.get("category", "personal").strip()
    tags_input = request.form.get("tags", "").strip()

    if not content:
        flash("Content is required!", "error")
        return redirect(url_for("home"))

    if not mood:
        flash("Mood is required!", "error")
        return redirect(url_for("home"))

    # Parse tags (comma-separated)
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    # Create new entry using database manager
    try:
        entry = db_manager.add_entry(
            content=content, mood=mood, category=category, tags=tags
        )
        flash("Journal entry added successfully!", "success")
    except Exception:
        # Don't expose internal errors to users
        flash("Error adding entry. Please try again.", "error")

    return redirect(url_for("home"))


@app.route("/entries")
def entries():
    """List all journal entries."""
    all_entries = db_manager.get_all_entries()
    return render_template("entries.html", entries=all_entries)


@app.route("/insights")
def insights():
    """Show analytics and insights."""
    all_entries = db_manager.get_all_entries()

    if not all_entries:
        create_sample_entries()
        all_entries = db_manager.get_all_entries()

    insight_data = InsightData(all_entries)
    helper = InsightsHelper(insight_data)

    # Calculate insights
    streak = helper.calculate_streak()
    total_entries = insight_data.total_entries()
    frequency = helper.get_writing_frequency(30)
    mood_breakdown = helper.get_mood_breakdown()
    top_tags = helper.get_top_tags(10)
    metrics = helper.get_total_metrics()

    return render_template(
        "insights.html",
        streak=streak,
        total_entries=total_entries,
        frequency=frequency,
        mood_breakdown=mood_breakdown,
        top_tags=top_tags,
        metrics=metrics,
    )


@app.route("/api/entries", methods=["GET"])
def api_entries():
    """API endpoint to get entries as JSON."""
    all_entries = db_manager.get_all_entries()
    entries_data = []
    for entry in all_entries:
        entries_data.append(
            {
                "id": entry.id,
                "content": entry.content,
                "mood": entry.mood,
                "category": entry.category,
                "tags": entry.tags,
                "timestamp": entry.timestamp.isoformat(),
            }
        )
    return jsonify(entries_data)


@app.route("/health")
def health():
    """Health check endpoint for deployment platforms."""
    try:
        entry_count = db_manager.get_entry_count()
        
        # Detect if running in serverless environment
        is_serverless = (
            os.getenv('VERCEL') == '1' or 
            os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None or
            app.config.get('SERVERLESS', False)
        )
        
        return jsonify(
            {
                "status": "healthy",
                "app": "Baddie AI Journal Hustle",
                "version": "0.1.0",
                "entries_count": entry_count,
                "database": "connected",
                "python_version": sys.version,
                "flask_available": True,
                "serverless": is_serverless,
                "platform": os.getenv('VERCEL_ENV', 'unknown'),
                "sqlalchemy_available": (
                    True if hasattr(db_manager, "engine") else False
                ),
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )
    except Exception as e:
        # Don't expose stack trace details in production, but provide debug info
        error_info = (
            str(e)
            if os.getenv("FLASK_DEBUG") == "true"
            else "Database connection error"
        )
        
        is_serverless = (
            os.getenv('VERCEL') == '1' or 
            os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None or
            app.config.get('SERVERLESS', False)
        )
        
        return (
            jsonify(
                {
                    "status": "error",
                    "app": "Baddie AI Journal Hustle",
                    "version": "0.1.0",
                    "error": error_info,
                    "python_version": sys.version,
                    "flask_available": True,
                    "serverless": is_serverless,
                    "platform": os.getenv('VERCEL_ENV', 'unknown'),
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            ),
            500,
        )


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return (
        render_template("error.html", error_code=404, error_message="Page not found"),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "error.html", error_code=500, error_message="Internal server error"
        ),
        500,
    )


@app.teardown_appcontext
def close_db(error):
    """Clean up database connections on app teardown."""
    try:
        db_manager.close()
    except Exception:
        pass


if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    print(f"🚀 Starting Baddie AI Journal Hustle on {host}:{port}")
    print(f"📖 Visit http://{host}:{port} to start journaling!")
    print(f"🔧 Debug mode: {debug}")
    print(
        f"💾 Database: {os.getenv('SQLALCHEMY_DATABASE_URI', 'SQLite (default)')[:50]}..."
    )

    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    finally:
        # Clean up database connection
        try:
            db_manager.close()
        except Exception:
            pass
