#!/usr/bin/env python3
"""
Minimal Flask web application for Baddie AI Journal Hustle.

This creates a deployable web interface around the existing journaling functionality.
"""

import os
import sys
from datetime import datetime, timezone

try:
    from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

    FLASK_AVAILABLE = True
except ImportError:
    print("Flask is required for web deployment. Install with: pip install flask")
    sys.exit(1)

# Add the current directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from baddie_journal.models import InsightData  # noqa: E402
from baddie_journal.insights import InsightsHelper  # noqa: E402
from database import DatabaseManager  # noqa: E402

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
        db_manager.add_entry(content=content, mood=mood, category=category, tags=tags)
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
        return jsonify(
            {
                "status": "healthy",
                "app": "Baddie AI Journal Hustle",
                "version": "0.1.0",
                "entries_count": entry_count,
                "database": "connected",
                "python_version": sys.version,
                "flask_available": True,
                "sqlalchemy_available": (
                    True if hasattr(db_manager, "engine") else False
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    except Exception as e:
        # Don't expose stack trace details in production, but provide debug info
        error_info = (
            str(e)
            if os.getenv("FLASK_DEBUG") == "true"
            else "Database connection error"
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
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            500,
        )


# Thrift E-commerce Content Generator Routes
@app.route("/thrift")
def thrift_home():
    """Thrift product management home page."""
    return render_template("thrift_index.html")


@app.route("/thrift/analyze", methods=["POST"])
def thrift_analyze():
    """Analyze a thrift product and generate content."""
    try:
        from baddie_journal.models import ProductItem, ProductListing  # noqa: E402
        from baddie_journal.thrift_swarms import ThriftContentSwarm  # noqa: E402

        # Get form data
        item_type = request.form.get("item_type", "").strip()
        brand = request.form.get("brand", "").strip() or None
        model = request.form.get("model", "").strip() or None
        condition = request.form.get("condition", "Used").strip()
        key_features = [
            f.strip()
            for f in request.form.get("key_features", "").split(",")
            if f.strip()
        ]
        known_flaws = [
            f.strip() for f in request.form.get("known_flaws", "").split(",") if f.strip()
        ]
        target_audience = request.form.get("target_audience", "").strip() or None
        original_price = request.form.get("original_retail_price", "").strip()
        acquisition_cost = request.form.get("acquisition_cost", "").strip()
        user_description = request.form.get("user_description", "").strip() or None

        if not item_type:
            flash("Item type is required!", "error")
            return redirect(url_for("thrift_home"))

        # Create product item
        product = ProductItem(
            id=1,  # In production, use database ID
            item_type=item_type,
            brand=brand,
            model=model,
            condition=condition,
            key_features=key_features,
            known_flaws=known_flaws,
            target_audience=target_audience,
            original_retail_price=float(original_price) if original_price else None,
            acquisition_cost=float(acquisition_cost) if acquisition_cost else None,
            user_description=user_description,
        )

        # Check if AI analysis is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            flash("OpenAI API key not configured. Using basic template.", "warning")
            # Return basic template without AI analysis
            return render_template(
                "thrift_result.html",
                product=product,
                analysis=None,
                pricing=None,
                ai_available=False,
            )

        # Perform AI analysis
        try:
            swarm = ThriftContentSwarm(api_key=api_key)
            result = swarm.perform_comprehensive_analysis(product)

            # Create product listing
            listing = ProductListing(
                product=product,
                analysis=result.product_analysis,
                pricing=result.pricing_guidance,
            )

            return render_template(
                "thrift_result.html",
                product=product,
                analysis=result.product_analysis,
                pricing=result.pricing_guidance,
                image_suggestions=result.image_suggestions,
                listing=listing,
                ai_available=True,
            )
        except Exception as e:
            flash(f"AI analysis failed: {str(e)}", "error")
            return render_template(
                "thrift_result.html",
                product=product,
                analysis=None,
                pricing=None,
                ai_available=False,
            )

    except ImportError:
        flash(
            "Thrift functionality requires additional packages. "
            "Install with: pip install swarms openai",
            "error",
        )
        return redirect(url_for("thrift_home"))
    except Exception as e:
        flash(f"Error analyzing product: {str(e)}", "error")
        return redirect(url_for("thrift_home"))


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
