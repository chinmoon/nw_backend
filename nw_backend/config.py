import os
from flask_appbuilder.security.manager import AUTH_DB
basedir = os.path.abspath(os.path.dirname(__file__))

FAB_ADD_SECURITY_API = True
CSRF_ENABLED = True
SECRET_KEY = os.urandom(32)


OPENID_PROVIDERS = [
    {"name": "Google", "url": "https://www.google.com/accounts/o8/id"},
    {"name": "Yahoo", "url": "https://me.yahoo.com"},
    {"name": "AOL", "url": "http://openid.aol.com/<username>"},
    {"name": "Flickr", "url": "http://www.flickr.com/<username>"},
    {"name": "MyOpenID", "url": "https://www.myopenid.com"},
]

#SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/myapp1'

# SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost:5432/myapp'
# SQLALCHEMY_ECHO = True
SQLALCHEMY_POOL_RECYCLE = 3

BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_FOLDER = "translations"
LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
    "zh": {"flag": "cn", "name": "Chinese"},
    
}


# ------------------------------
# GLOBALS FOR GENERAL APP's
# ------------------------------
FAB_API_SWAGGER_UI = True

UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
# FAB配置
AUTH_TYPE = AUTH_DB
# AUTH_LDAP_SERVER = "ldap://dc.domain.net"
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "F.A.B. Example"
APP_THEME = ""  # default
# APP_THEME = "cerulean.css"      # COOL
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"       # COOL
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"          # COOL
# APP_THEME = "spacelab.css"      # NICE
# APP_THEME = "united.css"
# APP_THEME = "darkly.css"
# APP_THEME = "lumen.css"
# APP_THEME = "paper.css"
# APP_THEME = "sandstone.css"
# APP_THEME = "solar.css"
# APP_THEME = "superhero.css"

# FAB_ROLES = {
#    "ReadOnly": [
#        [".*", "can_list"],
#        [".*", "can_show"],
#        [".*", "menu_access"]
#    ]
# }
