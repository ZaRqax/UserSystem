from sqlalchemy.inspection import inspect
from app import db
import hashing


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(array):
        return [elem.serialize() for elem in array]


class User(db.Model, Serializer):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean())
    user_permissions = db.Column(db.ARRAY(db.String(30)))

    def __init__(self, username, password,user_permissions,is_admin=None):
        self.username = username
        self.password = hashing.hash(password)
        self.is_admin = is_admin
        self.user_permissions = user_permissions

    def serialize(self):
        s = Serializer.serialize(self)
        return s

    def __str__(self):
        return f'{self.username}'
