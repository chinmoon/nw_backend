import datetime
import enum

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from flask_appbuilder.security.sqla.models import User

mindate = datetime.date(datetime.MINYEAR, 1, 1)

class GQAUser(User):
    """
    扩展 FAB 用户模型
    """
    __tablename__ = 'ab_user'  # 使用与基类相同的表名
    __table_args__ = {'extend_existing': True}  # 允许表已存在
    
    # 添加新字段
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return self.username
class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(enum.Enum):
    Female = 1
    Male = 2


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"), nullable=False)
    contact_group = relationship("ContactGroup")
    gender = Column(Enum(Gender), info={"marshmallow_by_value": False})

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)


class ModelOMParent(Model):
    __tablename__ = "model_om_parent"
    id = Column(Integer, primary_key=True)
    field_string = Column(String(50), unique=True, nullable=False)


class ModelOMChild(Model):
    id = Column(Integer, primary_key=True)
    field_string = Column(String(50), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("model_om_parent.id"))
    parent = relationship(
        "ModelOMParent",
        backref=backref("children", cascade="all, delete-orphan"),
        foreign_keys=[parent_id],
    )
