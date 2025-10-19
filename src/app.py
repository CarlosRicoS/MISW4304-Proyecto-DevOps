from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    InvalidHeaderError,
    JWTDecodeError,
    CSRFError,
    WrongTokenError,
)
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError,
    InvalidTokenError,
)
from .config import config
from .infrastructure.models import db
from .container import DIContainer


def create_app(config_name="default"):
    """Application factory pattern with hexagonal architecture"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # JWT Error Handlers - These handle flask-jwt-extended managed errors
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        """Handle invalid token errors"""
        return jsonify({
            'error': 'Invalid identity',
            'message': error_string
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        """Handle missing token errors"""
        return jsonify({
            'error': 'Invalid identity',
            'message': 'Authorization token is missing'
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired token errors"""
        return jsonify({
            'error': 'Invalid identity',
            'message': 'Token has expired'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handle revoked token errors"""
        return jsonify({
            'error': 'Invalid identity',
            'message': 'Token has been revoked'
        }), 401

    # Initialize dependency injection container
    container = DIContainer()

    # Initialize Flask-RESTful API with custom error handler
    api = Api(app, catch_all_404s=True)

    # Override Flask-RESTful's error handler to catch JWT exceptions
    def custom_error_handler(error):
        """Custom error handler for Flask-RESTful that catches JWT exceptions"""
        # Handle PyJWT exceptions (signature verification, etc.)
        if isinstance(error, (InvalidSignatureError, DecodeError, InvalidTokenError)):
            return jsonify({
                'error': 'Invalid identity',
                'message': 'Token signature verification failed'
            }), 401
        
        # Handle expired tokens
        if isinstance(error, ExpiredSignatureError):
            return jsonify({
                'error': 'Invalid identity',
                'message': 'Token has expired'
            }), 401
        
        # Handle flask-jwt-extended exceptions
        if isinstance(error, (NoAuthorizationError, InvalidHeaderError, JWTDecodeError)):
            return jsonify({
                'error': 'Invalid identity',
                'message': str(error)
            }), 401
        
        if isinstance(error, (CSRFError, WrongTokenError)):
            return jsonify({
                'error': 'Invalid identity',
                'message': 'Token validation failed'
            }), 401
        
        # Log other exceptions
        app.logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        
        # Return generic error for other exceptions
        if app.debug:
            return jsonify({
                'error': 'Internal server error',
                'message': str(error)
            }), 500
        else:
            return jsonify({
                'error': 'Internal server error',
                'message': 'An error occurred'
            }), 500

    # Register the custom error handler with Flask-RESTful
    api.handle_error = custom_error_handler

    # Also register Flask error handlers as backup
    @app.errorhandler(InvalidSignatureError)
    def handle_invalid_signature(e):
        return jsonify({
            'error': 'Invalid identity',
            'message': 'Token signature verification failed'
        }), 401

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Catch-all error handler"""
        return custom_error_handler(e)

    # Add API resources with dependency injection
    api.add_resource(container.get_ping_controller(), "/ping")
    api.add_resource(container.get_health_controller(), "/health")
    
    # Add blacklist endpoints
    api.add_resource(container.get_blacklist_controller(), "/blacklists")
    api.add_resource(container.get_blacklist_check_controller(), "/blacklists/<string:email>")

    # Add token endpoint
    api.add_resource(container.get_blacklist_token_controller(), "/token")

    # Store container in app context for access in controllers
    app.container = container

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app("development")
    app.run(debug=True, host="0.0.0.0", port=5000)
