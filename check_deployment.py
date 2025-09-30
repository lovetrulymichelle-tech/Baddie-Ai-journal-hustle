#!/usr/bin/env python3
"""
Deployment verification script for Baddie AI Journal Hustle.

This script checks if all dependencies and configurations are ready for deployment.
"""

import sys
import os
from datetime import datetime, timezone


def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Python Version Check:")
    version = sys.version_info
    print(f"   Current: Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Compatible")
        return True
    else:
        print("   ❌ Requires Python 3.8+")
        return False


def check_dependencies():
    """Check if required dependencies are available."""
    print("\n📦 Dependencies Check:")
    dependencies = [
        ("flask", "Flask"),
        ("sqlalchemy", "SQLAlchemy"),
        ("psycopg2", "PostgreSQL driver"),
        ("dateutil", "Python-dateutil"),
        ("gunicorn", "Gunicorn WSGI server"),
    ]

    all_deps_ok = True
    for dep_name, display_name in dependencies:
        try:
            __import__(dep_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} - Missing")
            all_deps_ok = False

    return all_deps_ok


def check_environment_variables():
    """Check deployment environment variables."""
    print("\n🔧 Environment Variables Check:")

    # Essential variables
    essential_vars = ["PORT"]
    recommended_vars = ["SECRET_KEY", "SQLALCHEMY_DATABASE_URI", "FLASK_DEBUG"]

    all_essential = True
    for var in essential_vars:
        if os.getenv(var):
            print(f"   ✅ {var} = {os.getenv(var)}")
        else:
            print(f"   ❌ {var} - Missing (will use default)")
            # PORT is actually optional as we have defaults

    for var in recommended_vars:
        if os.getenv(var):
            # Don't print full secret key value
            value = os.getenv(var)
            if "SECRET" in var.upper() or "PASSWORD" in var.upper():
                value = f"***{value[-4:]}" if len(value) > 4 else "***"
            elif "DATABASE" in var.upper() and len(value) > 20:
                value = value[:20] + "..."
            print(f"   ℹ️  {var} = {value}")
        else:
            print(f"   ⚠️  {var} - Not set (will use default)")

    return all_essential


def check_app_structure():
    """Check if app files are in place."""
    print("\n📁 Application Structure Check:")
    required_files = [
        "app.py",
        "Procfile",
        "requirements.txt",
        "database.py",
        "baddie_journal/__init__.py",
        "baddie_journal/models/__init__.py",
        "baddie_journal/insights.py",
    ]

    all_files_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            all_files_ok = False

    return all_files_ok


def check_imports():
    """Test critical imports."""
    print("\n🔄 Import Test:")

    try:
        # Test Flask app imports
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        from baddie_journal.models import JournalEntry, InsightData  # noqa: F401

        print("   ✅ Core models")

        from baddie_journal.insights import InsightsHelper  # noqa: F401

        print("   ✅ Insights helper")

        from database import DatabaseManager  # noqa: F401

        print("   ✅ Database manager")

        # Test Flask imports
        from flask import Flask  # noqa: F401

        print("   ✅ Flask framework")

        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False


def check_database_connection():
    """Test database connectivity."""
    print("\n💾 Database Connection Test:")

    try:
        from database import DatabaseManager

        db = DatabaseManager()

        # Test basic operations
        count = db.get_entry_count()
        print(f"   ✅ Database connected - {count} entries")

        db.close()
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False


def main():
    """Run all deployment checks."""
    print("🚀 Baddie AI Journal Hustle - Deployment Verification")
    print(f"   Running at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)

    checks = [
        check_python_version(),
        check_dependencies(),
        check_environment_variables(),
        check_app_structure(),
        check_imports(),
        check_database_connection(),
    ]

    print("\n" + "=" * 60)

    success_count = sum(checks)
    total_checks = len(checks)

    if success_count == total_checks:
        print("🎉 ALL CHECKS PASSED - Ready for deployment!")
        print("\n🚀 Deployment Commands:")
        print("   Local test: python app.py")
        print("   Production: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1")
        return 0
    else:
        print(
            f"⚠️  {total_checks - success_count} CHECKS FAILED - Fix issues before deploying"
        )
        print("\n🔧 Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Set SECRET_KEY environment variable")
        print("   - Configure database connection string")
        return 1


if __name__ == "__main__":
    sys.exit(main())
