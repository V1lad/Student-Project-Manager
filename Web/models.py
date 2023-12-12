from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    status = db.Column(db.String(16))
    ownedProjects = db.Column(db.String(16))
    sharedProjects = db.Column(db.String(16))

class Project(db.Model, UserMixin):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    ownerId = db.Column(db.Integer)
    name = db.Column(db.String(150))
    shortDescription = db.Column(db.String(255))
    fullDescription = db.Column(db.String(255))
    
    allowedUsers = db.Column(db.JSON)
    
    isArchived = db.Column(db.Boolean)
    isPublic = db.Column(db.Boolean)
    
    