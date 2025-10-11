from datetime import datetime
from src.domain.entities import HealthStatus
from src.domain.ports import HealthCheckPort


class HealthService:
    """Application service for health check operations"""

    def __init__(self, health_check_port: HealthCheckPort):
        self._health_check_port = health_check_port

    def get_health_status(self) -> HealthStatus:
        """Get overall health status of the application"""
        try:
            db_healthy = self._health_check_port.check_database_health()
            services_healthy = self._health_check_port.check_external_services_health()

            if db_healthy and services_healthy:
                return HealthStatus(
                    status="healthy", message="All systems operational", timestamp=datetime.utcnow()
                )
            else:
                return HealthStatus(
                    status="unhealthy", message="Some systems are down", timestamp=datetime.utcnow()
                )
        except Exception as e:
            return HealthStatus(
                status="error",
                message=f"Health check failed: {str(e)}",
                timestamp=datetime.utcnow(),
            )

    def ping(self) -> dict:
        """Simple ping endpoint for basic connectivity check"""
        return {"status": "ok", "message": "pong", "timestamp": datetime.utcnow().isoformat()}
