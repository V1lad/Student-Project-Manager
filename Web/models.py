from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    status = db.Column(db.String(16))
    ownedProjects = db.relationship('Project')


class Project(db.Model, UserMixin):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    name = db.Column(db.String(150), default='')
    shortDescription = db.Column(db.String(255), default='')
    fullDescription = db.Column(db.String(255), default='')
    goal = db.Column(db.String(255), default='')
    
    allowedUsers = db.Column(db.JSON, default='[]')
    
    
    