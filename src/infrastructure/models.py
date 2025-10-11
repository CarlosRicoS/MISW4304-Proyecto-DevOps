from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class BlacklistModel(db.Model):
    """SQLAlchemy model for blacklist entries"""
    
    __tablename__ = 'blacklist'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.Text, nullable=False)
    ip = db.Column(db.String(45), nullable=True)  # Supports both IPv4 and IPv6
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlacklistModel {self.email}>'
