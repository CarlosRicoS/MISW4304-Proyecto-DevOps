from src.application.health_service import HealthService
from src.application.blacklist_service import BlacklistService
from src.infrastructure.health_check import SQLAlchemyHealthCheck
from src.infrastructure.repositories import BlacklistRepository
from src.adapters.health_controller import HealthController, PingController
from src.adapters.blacklist_controller import BlacklistController, BlacklistCheckController, TokenController


class DIContainer:
    """Dependency Injection Container"""

    def __init__(self):
        self._services = {}
        self._setup_services()

    def _setup_services(self):
        """Setup all service dependencies"""
        # Infrastructure layer
        health_check = SQLAlchemyHealthCheck()
        blacklist_repository = BlacklistRepository()

        # Application layer
        health_service = HealthService(health_check)
        blacklist_service = BlacklistService(blacklist_repository)

        # Store services for injection into controllers
        self._services = {
            "health_check": health_check,
            "health_service": health_service,
            "blacklist_repository": blacklist_repository,
            "blacklist_service": blacklist_service,
        }

    def get_service(self, name: str):
        """Get service by name"""
        return self._services.get(name)

    def create_controller_class(self, controller_class):
        """Create a controller class with dependency injection"""
        container = self

        class InjectedController(controller_class):
            def __init__(self):
                super().__init__()
                # Inject dependencies based on controller type
                if hasattr(self, "set_health_service"):
                    self.set_health_service(container.get_service("health_service"))

        # Preserve the original class name for Flask-RESTful
        InjectedController.__name__ = controller_class.__name__
        return InjectedController

    def create_blacklist_controller_class(self, controller_class):
        """Create a blacklist controller class with dependency injection"""
        container = self

        class InjectedController(controller_class):
            def __init__(self):
                blacklist_service = container.get_service("blacklist_service")
                super().__init__(blacklist_service)

        # Preserve the original class name for Flask-RESTful
        InjectedController.__name__ = controller_class.__name__
        return InjectedController

    def get_health_controller(self):
        return self.create_controller_class(HealthController)

    def get_ping_controller(self):
        return self.create_controller_class(PingController)

    def get_blacklist_controller(self):
        return self.create_blacklist_controller_class(BlacklistController)

    def get_blacklist_check_controller(self):
        return self.create_blacklist_controller_class(BlacklistCheckController)

    def get_blacklist_token_controller(self):
        return self.create_blacklist_controller_class(TokenController)