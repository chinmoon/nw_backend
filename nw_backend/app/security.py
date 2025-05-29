from flask_appbuilder.security.manager import SecurityManager
from flask_appbuilder.security.views import UserDBModelView
from .models import GQAUser

class GQAUserModelView(UserDBModelView):
    show_columns = ['username', 'first_name', 'last_name', 'email', 
                    'is_active', 'role', 'last_login', 'phone']
    edit_columns = ['first_name', 'last_name', 'email', 'phone']
    add_columns = ['first_name', 'last_name', 'username', 
                   'email', 'phone', 'role', 'password', 'conf_password']

CUSTOM_SECURITY_MANAGER = {
    "ROLES": {
        "Admin": [
            ["can_list", "User"],
            ["can_edit", "User"],
            ["can_add", "User"],
            ["can_delete", "User"],
        ],
        "User": [
            ["can_list", "MyView"],
            ["can_edit", "MyView"],
        ]
    }
}

class GQASecurityManager(SecurityManager):
    user_model = GQAUser
    userdbmodelview = GQAUserModelView

    def __init__(self, appbuilder):
        super(GQASecurityManager, self).__init__(appbuilder)
        self.init_custom_roles()
    
    def init_custom_roles(self):
        for role_name, permissions in CUSTOM_SECURITY_MANAGER["ROLES"].items():
            role = self.find_role(role_name)
            if not role:
                role = self.add_role(role_name)
            for permission in permissions:
                pvm = self.find_permission_view_menu(permission[0], permission[1])
                if pvm:
                    self.add_permission_role(role, pvm)