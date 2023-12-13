from json import loads
from .models import Project, SubProject, Note

def remove_project_from_user():
    pass

def has_access_to_project(user, project):
    if project.owner_id == user.id:
        return True
    else:
        allowed_users = loads(project.allowedUsers)
        if str(user.id) in allowed_users:
            return True
        else:
            return False
        
def has_access_to_subproject(user, subproject):
    return has_access_to_subproject(user=user, subproject=Project.query.filter_by(id=subproject.parent_id).first())
        
def has_access_to_note(user, note):
    return has_access_to_subproject(user=user, subproject=SubProject.query.filter_by(id=note.parent_id).first())