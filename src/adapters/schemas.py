from marshmallow import Schema, fields, validate


class HealthStatusSchema(Schema):
    """Health status schema for serialization"""

    status = fields.Str()
    message = fields.Str()
    timestamp = fields.DateTime()


class BlacklistRequestSchema(Schema):
    """Schema for blacklist creation request"""
    
    email = fields.Email(required=True, validate=validate.Length(min=1, max=255))
    app_uuid = fields.Str(required=True, validate=validate.Length(min=1, max=36))
    blocked_reason = fields.Str(required=True, validate=validate.Length(min=1, max=1000))


class BlacklistResponseSchema(Schema):
    """Schema for blacklist response"""
    
    mensaje = fields.Str()
    email = fields.Email()
    app_uuid = fields.Str()
    blocked_reason = fields.Str()
    fecha_creacion = fields.Str()
    error = fields.Str()


class BlacklistCheckResponseSchema(Schema):
    """Schema for blacklist check response"""
    
    blacklisted = fields.Bool(required=True)
    email = fields.Email(required=True)
    blocked_reason = fields.Str()
    app_uuid = fields.Str()
    fecha_creacion = fields.Str()


# Schema instances
health_status_schema = HealthStatusSchema()
blacklist_request_schema = BlacklistRequestSchema()
blacklist_response_schema = BlacklistResponseSchema()
blacklist_check_response_schema = BlacklistCheckResponseSchema()
