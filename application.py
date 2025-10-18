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

if __name__ == '__main__':
    app = create_app('development')
    
    # Create database tables on startup
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, host='0.0.0.0', port=5000)
