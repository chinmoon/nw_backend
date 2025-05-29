
from flask_appbuilder import ModelRestApi

from ..models.models import Contact, ContactGroup, ModelOMParent
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_

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


