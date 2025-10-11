from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from functools import wraps
from ..application.blacklist_service import BlacklistService
from .schemas import (
    blacklist_request_schema,
    blacklist_response_schema,
    blacklist_check_response_schema
)


def require_auth_token(f):
    """Decorator to require Bearer token authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return {'error': 'Missing Authorization header'}, 401
        
        if not auth_header.startswith('Bearer '):
            return {'error': 'Invalid Authorization header format'}, 401
        
        token = auth_header[7:]  # Remove "Bearer " prefix
        
        if not token:
            return {'error': 'Missing token'}, 401
        
        # For now, we'll accept any Bearer token
        # In a real application, you would validate the token
        return f(*args, **kwargs)
    
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