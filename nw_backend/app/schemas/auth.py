from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    nickname = fields.String()
    real_name = fields.String()
    email = fields.String()
    avatar = fields.String()
    roles = fields.List(fields.String())

class LoginRequestSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class LoginResponseSchema(Schema):
    code = fields.Integer()
    message = fields.String()
    data = fields.Dict()