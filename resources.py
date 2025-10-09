from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from models import db, User
from schemas import user_schema, users_schema


class UserResource(Resource):
    """Single user resource"""
    
    @jwt_required()
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)
    
    @jwt_required()
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200


class UserListResource(Resource):
    """User list resource"""
    
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)
    
    def post(self):
        data = request.get_json()
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data.get('password_hash', '')
        )
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class LoginResource(Resource):
    """Login resource for JWT authentication"""
    
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return {'message': 'Username is required'}, 400
        
        # In a real application, verify password here
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200


class HealthCheckResource(Resource):
    """Health check resource"""
    
    def get(self):
        return {'status': 'healthy', 'message': 'API is running'}, 200
