from flask_restful import Resource
from src.application.health_service import HealthService
from .schemas import health_status_schema


class HealthController(Resource):
    """Controller for health check operations"""

    def __init__(self):
        self.health_service: HealthService = None  # Will be injected by dependency container

    def set_health_service(self, health_service: HealthService):
        """Set health service (dependency injection)"""
        self.health_service = health_service

    def get(self):
        """Get detailed health status"""
        health_status = self.health_service.get_health_status()
        return health_status_schema.dump(health_status)


class PingController(Resource):
    """Controller for simple ping health check"""

    def __init__(self):
        self.health_service: HealthService = None  # Will be injected by dependency container

    def set_health_service(self, health_service: HealthService):
        """Set health service (dependency injection)"""
        self.health_service = health_service

    def get(self):
        """Simple ping endpoint"""
        return self.health_service.ping()

    def head(self):
        """HEAD request for ping - useful for load balancers"""
        return "", 200
