from . import db
from flask_login import UserMixin
from flask_authorize import AllowancesMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    status = db.Column(db.String(16))

