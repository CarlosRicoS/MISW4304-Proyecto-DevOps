from typing import Optional, Dict, Any
from flask import request
from ..domain.entities import Blacklist
from ..domain.ports import BlacklistRepositoryPort


class BlacklistService:
    """Application service for blacklist operations"""

    def __init__(self, blacklist_repository: BlacklistRepositoryPort):
        self.blacklist_repository = blacklist_repository

    def add_email_to_blacklist(
        self, email: str, app_uuid: str, blocked_reason: str
    ) -> Dict[str, Any]:
        """Add an email to the blacklist"""
        
        # Get client IP address
        client_ip = self._get_client_ip()
        
        # Create blacklist entity
        blacklist = Blacklist(
            email=email,
            app_uuid=app_uuid,
            blocked_reason=blocked_reason,
            ip=client_ip
        )

        # Try to add to blacklist
        success = self.blacklist_repository.add_email_to_blacklist(blacklist)
        
        if success:
            return {
                "mensaje": f"Email {email} agregado a la lista negra",
                "email": email,
                "app_uuid": app_uuid,
                "blocked_reason": blocked_reason,
                "fecha_creacion": blacklist.created_at.isoformat()
            }
        else:
            return {
                "error": f"Email {email} ya existe en la lista negra"
            }

    def check_email_blacklist_status(self, email: str) -> Dict[str, Any]:
        """Check if an email is in the blacklist"""
        
        blacklist_entry = self.blacklist_repository.is_email_blacklisted(email)
        
        if blacklist_entry:
            return {
                "blacklisted": True,
                "email": email,
                "blocked_reason": blacklist_entry.blocked_reason,
                "app_uuid": blacklist_entry.app_uuid,
                "fecha_creacion": blacklist_entry.created_at.isoformat()
            }
        else:
            return {
                "blacklisted": False,
                "email": email
            }

    def _get_client_ip(self) -> Optional[str]:
        """Get client IP address from request"""
        # Check if running behind a proxy
        if request.environ.get('HTTP_X_FORWARDED_FOR'):
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
        elif request.environ.get('HTTP_X_REAL_IP'):
            return request.environ['HTTP_X_REAL_IP']
        else:
            return request.environ.get('REMOTE_ADDR')