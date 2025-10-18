from typing import Optional
from sqlalchemy.exc import IntegrityError
from ..domain.entities import Blacklist
from ..domain.ports import BlacklistRepositoryPort
from .models import db, BlacklistModel


class BlacklistRepository(BlacklistRepositoryPort):
    """SQLAlchemy implementation of BlacklistRepositoryPort"""

    def add_email_to_blacklist(self, blacklist: Blacklist) -> bool:
        """Add an email to the blacklist"""
        try:
            blacklist_model = BlacklistModel(
                email=blacklist.email,
                app_uuid=blacklist.app_uuid,
                blocked_reason=blacklist.blocked_reason,
                ip=blacklist.ip,
                created_at=blacklist.created_at
            )
            
            db.session.add(blacklist_model)
            db.session.commit()
            return True
        except IntegrityError:
            # Email already exists in blacklist
            db.session.rollback()
            return False
        except Exception:
            db.session.rollback()
            return False

    def is_email_blacklisted(self, email: str) -> Optional[Blacklist]:
        """Check if an email is in the blacklist and return the blacklist entry"""
        try:
            blacklist_model = BlacklistModel.query.filter_by(email=email).first()
            
            if blacklist_model:
                return Blacklist(
                    email=blacklist_model.email,
                    app_uuid=blacklist_model.app_uuid,
                    blocked_reason=blacklist_model.blocked_reason,
                    ip=blacklist_model.ip,
                    created_at=blacklist_model.created_at
                )
            
            return None
        except Exception:
            return None
