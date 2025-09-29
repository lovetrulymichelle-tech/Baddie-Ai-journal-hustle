#!/usr/bin/env python3
"""
Vercel serverless WSGI handler for Baddie AI Journal Hustle.

This file is the entry point for Vercel's Python runtime.
It imports the Flask app and exposes it for serverless execution.
"""

import os
import sys

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app - this will initialize everything
from app import app

# Vercel expects a variable named 'app' or a handler function
# The Flask app instance is already named 'app', so we can use it directly
handler = app

# For Vercel's WSGI runtime
application = app
