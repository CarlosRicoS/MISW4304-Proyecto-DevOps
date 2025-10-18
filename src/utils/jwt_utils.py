from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import datetime
from threading import Lock

_SINGLETON_TOKEN: str | None = None
_singleton_lock = Lock()

def generate_static_token() -> str:
    """Generate a static JWT token that doesn't expire"""
    additional_claims = {
        'user_id': 'blacklist_service',
        'service': 'blacklist_api',
        'created_at': datetime.utcnow().isoformat()
    }

    token = create_access_token(
        identity='blacklist_service',
        additional_claims=additional_claims,
        expires_delta=False  # This makes the token never expire
    )

    return token

def get_singleton_token() -> str:
    """Return the same token for this process lifetime"""
    global _SINGLETON_TOKEN

    if _SINGLETON_TOKEN:
        return _SINGLETON_TOKEN

    with _singleton_lock:
        if _SINGLETON_TOKEN:
            return _SINGLETON_TOKEN
        _SINGLETON_TOKEN = generate_static_token()
        return _SINGLETON_TOKEN

def get_user_info():
    """Get current user info from JWT token"""
    return get_jwt_identity()