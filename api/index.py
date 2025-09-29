#!/usr/bin/env python3
"""
Vercel serverless function handler for Baddie AI Journal Hustle.

This module creates a serverless-compatible handler for the Flask application.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import the Flask app
try:
    from app import app
    
    # Set up environment for serverless
    os.environ.setdefault('FLASK_DEBUG', 'false')
    
    # Export the app for Vercel
    app.config['SERVERLESS'] = True
    
    # The app object is what Vercel will use
    application = app
    
except Exception as e:
    print(f"Error importing Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

# For direct testing
if __name__ == "__main__":
    app.run(debug=False)