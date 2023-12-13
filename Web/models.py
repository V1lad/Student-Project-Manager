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
    addedProjects = db.Column(db.JSON, default='[]')


class Project(db.Model, UserMixin):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    name = db.Column(db.String(150), default='')
    shortDescription = db.Column(db.String(255), default='')
    fullDescription = db.Column(db.String(255), default='')
    goal = db.Column(db.String(255), default='')
    
    allowedUsers = db.Column(db.JSON, default='[]')
    subprojects = db.relationship('SubProject')
    
class SubProject(db.Model, UserMixin):
    __tablename__ = 'subprojects'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    
    name = db.Column(db.String(150), default='')
    shortDescription = db.Column(db.String(255), default='')
    content = db.Column(db.JSON, default='[]')
    
    notes = db.relationship('Note')

class Note(db.Model, UserMixin):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('subprojects.id'))
    
    content = db.Column(db.String, default='')
    type = db.Column(db.String, default='')
    done = db.Column(db.String, default='')
    