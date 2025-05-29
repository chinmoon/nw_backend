from flask_appbuilder.api import BaseApi, expose
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import check_password_hash

from ..schemas.auth import LoginRequestSchema, LoginResponseSchema
from ..utils.response import APIResponse

class AuthApi(BaseApi):
    resource_name = 'auth1'
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
            return APIResponse.error("Missing JSON in request")
            
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not username or not password:
            return APIResponse.error("Missing username or password")
        
        user = self.appbuilder.sm.find_user(username=username)
        if not user:
            return APIResponse.error("Invalid username", 401)
            
        if check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=username,
                expires_delta=timedelta(hours=24)
            )
            
            return APIResponse.success({
                "token": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "nickname": getattr(user, 'nickname', user.username),
                    "real_name": f"{user.first_name} {user.last_name}".strip(),
                    "avatar": getattr(user, 'avatar', ''),
                    "email": user.email,
                    "roles": [role.name for role in user.roles]
                }
            })
        
        return APIResponse.error("Login failed", 401)