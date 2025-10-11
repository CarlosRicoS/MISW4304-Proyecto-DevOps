from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from .config import config
from .infrastructure.models import db
from .container import DIContainer


def create_app(config_name="default"):
    """Application factory pattern with hexagonal architecture"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)

    # Initialize dependency injection container
    container = DIContainer()

    # Initialize Flask-RESTful API
    api = Api(app)

    # Add API resources with dependency injection
    api.add_resource(container.get_ping_controller(), "/ping")
    api.add_resource(container.get_health_controller(), "/health")
    
    # Add blacklist endpoints
    api.add_resource(container.get_blacklist_controller(), "/blacklists")
    api.add_resource(container.get_blacklist_check_controller(), "/blacklists/<string:email>")

    # Store container in app context for access in controllers
    app.container = container

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app("development")
    app.run(debug=True, host="0.0.0.0", port=5000)
