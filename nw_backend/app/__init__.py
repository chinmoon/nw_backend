import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA


from flask_jwt_extended import JWTManager
from flask_cors import CORS


logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")

db = SQLA(app)
#后端接口就会自动带上 Access-Control-Allow-Origin 等 CORS 响应头，前端就不会再报 CORS 错误了
CORS(app, supports_credentials=True)
jwt = JWTManager(app)  # 实际使用JWTManager

appbuilder = AppBuilder(app, db.session)

from . import models, api  # noqa
 # 注册所有API
from .api.auth import AuthApi
appbuilder.add_api(AuthApi)
from .api.contact import ContactModelApi
appbuilder.add_api(ContactModelApi)