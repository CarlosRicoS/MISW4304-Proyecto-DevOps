from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError
from functools import wraps
from ..application.blacklist_service import BlacklistService
from .schemas import (
    blacklist_request_schema,
    blacklist_response_schema,
    blacklist_check_response_schema
)
from ..utils.jwt_utils import get_singleton_token

def require_auth_token(f):
    @jwt_required()
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get user identity from JWT token
        user_identity = get_jwt_identity()

        # Optional: Add additional validation
        if not user_identity:
            return {'error': 'Invalid token identity'}, 401

        # Add user info to request context for potential use
        request.user_info = {
            'identity': user_identity,
            'jwt_data': get_jwt_identity()
        }

        return f(*args, **kwargs)
    """Decorator to require Bearer token authentication"""

    return decorated_function


class BlacklistController(Resource):
    """Controller for blacklist operations"""

    def __init__(self, blacklist_service: BlacklistService):
        self.blacklist_service = blacklist_service

    @require_auth_token
    def post(self):
        """Add an email to the blacklist"""
        try:
            # Validate request data
            json_data = request.get_json()
            if not json_data:
                return {'error': 'No JSON data provided'}, 400
            
            # Validate using schema
            validated_data = blacklist_request_schema.load(json_data)
            
            # Call service
            result = self.blacklist_service.add_email_to_blacklist(
                email=validated_data['email'],
                app_uuid=validated_data['app_uuid'],
                blocked_reason=validated_data['blocked_reason']
            )
            
            # Check if there was an error
            if 'error' in result:
                return result, 409  # Conflict - email already exists
            
            # Return success response
            return blacklist_response_schema.dump(result), 201
            
        except ValidationError as err:
            return {'error': 'Validation error', 'details': err.messages}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500


class BlacklistCheckController(Resource):
    """Controller for checking blacklist status"""

    def __init__(self, blacklist_service: BlacklistService):
        self.blacklist_service = blacklist_service

    @require_auth_token
    def get(self, email):
        """Check if an email is in the blacklist"""
        try:
            # Validate email format
            if not email or '@' not in email:
                return {'error': 'Invalid email format'}, 400
            
            # Call service
            result = self.blacklist_service.check_email_blacklist_status(email)
            
            # Return response
            return blacklist_check_response_schema.dump(result), 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500


class TokenController(Resource):
    """Controller for token generation (for testing purposes)"""

    def __init__(self, blacklist_service: BlacklistService):
        self.blacklist_service = blacklist_service

    def post(self):
        """Return the same static JWT token each call"""
        try:
            token = get_singleton_token()
            return {
                'token': token,
                'message': 'Token generated successfully',
                'usage': 'Use this token in Authorization header: Bearer <token>'
            }, 200
        except Exception as e:
            return {'error': 'Failed to generate token'}, 500