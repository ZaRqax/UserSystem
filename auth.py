from models import User
from app import db
import flask as fl
import hashing


def is_authenticate(user):
    if user.id == fl.session['user']:
        return True
    return False


def get_user():
    user_id = fl.session.get('user', False)
    if user_id:
        return User.query.get(user_id)


def authenticate(username, password):
    user = db.session.query(User).filter(User.username == username).first()
    if user is not None:
        h = hashing.hash(password)
        if user.password == h:
            return user


def login(user):
    fl.session['user'] = user.id
