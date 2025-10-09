from marshmallow import Schema, fields


class UserSchema(Schema):
    """User schema for serialization/deserialization using Marshmallow"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password_hash = fields.Str(load_only=True)
    created_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
