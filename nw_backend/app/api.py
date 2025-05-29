from flask_appbuilder import ModelRestApi
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_

from . import appbuilder, db
from .models import Contact, ContactGroup, ModelOMParent

    #raise RuntimeError("不兼容的marshmallow版本>4.0，会出现KeyError: permission_id，请安装3.26.1"pip install marshmallow==3.26.1)
from marshmallow import fields, Schema


from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta




from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.security.manager import AUTH_DB
from werkzeug.security import check_password_hash


db.create_all()


class GreetingsResponseSchema(Schema):
    message = fields.String()


class GreetingApi(BaseApi):
    resource_name = "greeting"
    openapi_spec_component_schemas = (GreetingsResponseSchema,)

    openapi_spec_methods = {
        "greeting": {"get": {"description": "Override description"}}
    }

    @expose("/")
    def greeting(self):
        """Send a greeting
        ---
        get:
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    $ref: '#/components/schemas/GreetingsResponseSchema'
        """
        return self.response(200, message="Hello")


appbuilder.add_api(GreetingApi)


class CustomFilter(BaseFilter):
    name = "Custom Filter"
    arg_name = "opr"

    def apply(self, query, value):
        return query.filter(
            or_(Contact.name.like(value + "%"), Contact.address.like(value + "%"))
        )


class ContactModelApi(ModelRestApi):
    resource_name = "contact"
    datamodel = SQLAInterface(Contact)
    allow_browser_login = True

    search_filters = {"name": [CustomFilter]}
    openapi_spec_methods = {
        "get_list": {"get": {"description": "Get all contacts, filter and pagination"}}
    }


appbuilder.add_api(ContactModelApi)


class GroupModelApi(ModelRestApi):
    resource_name = "group"
    datamodel = SQLAInterface(ContactGroup)
    allow_browser_login = True


appbuilder.add_api(GroupModelApi)


class ModelOMParentApi(ModelRestApi):
    allow_browser_login = True
    datamodel = SQLAInterface(ModelOMParent)


appbuilder.add_api(ModelOMParentApi)



# 先定义所有的 Schema 类
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

class AuthApi(BaseApi):
    resource_name = 'auth'
    openapi_spec_component_schemas = (LoginRequestSchema, LoginResponseSchema)

    @expose('/login', methods=['POST'])
    def login(self):
        """
        User Login
        ---
        post:
            description: Authenticate user and return token
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/LoginRequestSchema'
            responses:
                200:
                    description: Successfully authenticated
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/LoginResponseSchema'
                400:
                    description: Bad request
                401:
                    description: Authentication failed
        """
        if not request.is_json:
            return jsonify({
                "code": 0,
                "message": "Missing JSON in request",
                "data": None
            }), 400
            
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        
        if not username or not password:
            return jsonify({
                "code": 0,
                "message": "Missing username or password",
                "data": None
            }), 400
        
        user = self.appbuilder.sm.find_user(username=username)
        if not user:
            return jsonify({
                "code": 0,
                "message": "Invalid username",
                "data": None
            }), 401
            
        if check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=username,
                expires_delta=timedelta(hours=24)
            )
            
            return jsonify({
                "code": 1,
                "message": "Login successful",
                "data": {
                    "token": access_token,
                    "username": user.username,
                    "nickname": getattr(user, 'nickname', user.username),
                    "real_name": getattr(user, 'first_name', '') + ' ' + getattr(user, 'last_name', ''),
                    "avatar": getattr(user, 'avatar', ''),
                    "email": user.email,
                    "roles": [role.name for role in user.roles]
                }
            }), 200
        
        return jsonify({
            "code": 0,
            "message": "Login failed",
            "data": None
        }), 401

# 注册API
appbuilder.add_api(AuthApi)