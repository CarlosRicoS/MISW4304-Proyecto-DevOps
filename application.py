#!/usr/bin/env python3
"""
Main entry point for the Flask application
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_app
from src.infrastructure.models import db

# Create the application instance for gunicorn/WSGI servers
application = create_app('production')

# Create database tables on startup
with application.app_context():
    db.create_all()

if __name__ == '__main__':
    # When running directly (not via gunicorn), use development config
    app = create_app('development')
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, host='0.0.0.0', port=5000)
