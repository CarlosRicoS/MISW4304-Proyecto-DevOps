"""
Database migration script to create blacklist table
"""
from flask import current_app
from src.infrastructure.models import db, BlacklistModel


def create_blacklist_table():
    """Create blacklist table"""
    with current_app.app_context():
        # Create the blacklist table
        db.create_all()
        print("Blacklist table created successfully")


def drop_blacklist_table():
    """Drop blacklist table"""
    with current_app.app_context():
        BlacklistModel.__table__.drop(db.engine)
        print("Blacklist table dropped successfully")


if __name__ == "__main__":
    # This script can be run directly for manual migrations
    from src.app import create_app
    
    app = create_app()
    with app.app_context():
        create_blacklist_table()