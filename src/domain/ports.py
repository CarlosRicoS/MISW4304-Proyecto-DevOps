from abc import ABC, abstractmethod
from typing import Optional
from .entities import Blacklist


class HealthCheckPort(ABC):
    """Port for health check operations"""

    @abstractmethod
    def check_database_health(self) -> bool:
        """Check if database connection is healthy"""
        pass

    @abstractmethod
    def check_external_services_health(self) -> bool:
        """Check if external services are healthy"""
        pass


class BlacklistRepositoryPort(ABC):
    """Port for blacklist repository operations"""

    @abstractmethod
    def add_email_to_blacklist(self, blacklist: Blacklist) -> bool:
        """Add an email to the blacklist"""
        pass

    @abstractmethod
    def is_email_blacklisted(self, email: str) -> Optional[Blacklist]:
        """Check if an email is in the blacklist and return the blacklist entry"""
        pass
