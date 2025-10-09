from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class HealthStatus:
    """Health status domain entity"""

    status: str
    message: str
    timestamp: datetime

    def __post_init__(self):
        if not hasattr(self, "timestamp") or self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class Blacklist:
    """Blacklist domain entity"""

    email: str
    app_uuid: str
    blocked_reason: str
    ip: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if not hasattr(self, "created_at") or self.created_at is None:
            self.created_at = datetime.utcnow()
