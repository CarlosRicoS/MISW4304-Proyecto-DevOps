from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import config
from models import db
from resources import (
    UserResource,
    UserListResource,
    LoginResource,
    HealthCheckResource
)


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    
    # Initialize Flask-RESTful API
    api = Api(app)
    
    # Add API resources
    api.add_resource(HealthCheckResource, '/health')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
