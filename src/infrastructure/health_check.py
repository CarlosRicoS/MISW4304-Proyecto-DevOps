from src.domain.ports import HealthCheckPort
from .models import db


class SQLAlchemyHealthCheck(HealthCheckPort):
    """SQLAlchemy implementation of HealthCheckPort"""

    def check_database_health(self) -> bool:
        """Check if database connection is healthy"""
        try:
            # Simple database connectivity check
            db.session.execute("SELECT 1")
            return True
        except Exception:
            return False

    def check_external_services_health(self) -> bool:
        """Check if external services are healthy"""
        # For now, just return True as we don't have external services
        # In a real application, this would check external APIs, message queues, etc.
        return True
