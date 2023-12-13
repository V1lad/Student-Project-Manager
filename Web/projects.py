from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .models import Project, User, SubProject, Note
import json

projects = Blueprint('projects', __name__)

@projects.route('/projects', methods=["GET"])
@login_required
def allProjects():
    
    projects = Project.query.all()
    
    return render_template("projects.html", user=current_user, available_projects = projects)

@projects.route('/projects/<int:index>/redact', methods=["POST"])
@login_required
def redactProject(index):
    # Везде добавить проверку на то, что заходит владелец или человек с доступом! Функция HasAccess?
    name = request.form.get('name')
    shortDescription = request.form.get('shortDescription')
    fullDescription = request.form.get('fullDescription')
    goal = request.form.get('goal')
    delete_word = request.form.get('delete')
    user_id = request.form.get('user_id')
    to_delete_user_id = request.form.get('to_delete_user_id')
    
    
    project = Project.query.filter_by(id=index).first()
    
    allowed_users_list = json.loads(project.allowedUsers)
    allowed_users = [User.query.filter_by(id=int(i)).first() for i in allowed_users_list]
    
    if not project:
        return redirect(url_for('allProjects'))


    if delete_word == "УДАЛИТЬ":
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('projects.allProjects'))
    
    if name:
        project.name = name
    elif fullDescription:
        project.fullDescription = fullDescription
    elif shortDescription:
        project.shortDescription = shortDescription
    elif goal:
        project.goal = goal
    elif to_delete_user_id:
        print(allowed_users_list, to_delete_user_id)
        allowed_users_list.remove(to_delete_user_id)
        project.allowedUsers = json.dumps(allowed_users_list)
        allowed_users.remove(User.query.filter_by(id=to_delete_user_id).first())
        
    elif user_id:
        # Надо сделать проверку на повторение и на существование пользователя
        user_to_add = User.query.filter_by(id=user_id).first()
        if not user_to_add:
            flash("Пользователь с таким ID не найден", category="error")
            return render_template("redact_project.html", project=project, user=current_user, allowed_users=allowed_users)
        
        elif project.owner_id == user_to_add.id:
            flash("Вы не можете добавить владельца", category="error")
            return render_template("redact_project.html", project=project, user=current_user, allowed_users=allowed_users)

        else:
            # Проверяем, если ли уже у запрашиваемого пользователя доступ к проекту
            if user_id not in allowed_users_list:
                allowed_users_list.append(user_id)
                added_user = User.query.filter_by(id=user_id).first()
                allowed_users.append(added_user)
                project.allowedUsers = json.dumps(allowed_users_list)
            else:
                flash("Пользователю с таким ID уже предоставлен доступ", category="error")
                
    db.session.commit()
    
    return render_template("redact_project.html", project=project, user=current_user, allowed_users=allowed_users)

@projects.route('/new_project', methods=["GET", "POST"])
@login_required
def newProject():
    if request.method == "GET":
        return render_template("new_project.html", user=current_user)
    
    elif request.method == "POST":
        name = request.form.get('name')
        shortDescription = request.form.get('shortDescription')

        # Надо добавить OwnerID
        new_project = Project(name=name, shortDescription=shortDescription, owner_id=current_user.id)
        
        db.session.add(new_project)
        db.session.commit()
        
        return redirect(url_for('projects.allProjects'))

@projects.route('/projects/<int:index>', methods=["POST"])
@login_required
def showProject(index):
    # Надо сделать проверку на доступ к проекту.
    if request.method == "POST":
        to_create_subproject_name = request.form.get('to_create_subproject_name')
        
        
        print(to_create_subproject_name, "aaaaaaaaaaaaaa")
        project = Project.query.filter_by(id=index).first()
        subprojects = project.subprojects
        
        # Предотвращаем повторное создание ПОКА НЕТ
        
        if to_create_subproject_name:
            subproject = SubProject(name = to_create_subproject_name, parent_id = project.id)
            db.session.add(subproject)
            subprojects.append(subproject)

        
        db.session.commit()
        return render_template("show_project.html", project=project, user=current_user, subprojects=subprojects)

@projects.route('/projects/<int:index>/<int:subproject>/redact', methods=["POST"])
@login_required
def redactSubProject(index, subproject):
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        delete_word = request.form.get('delete')
        
        project = Project.query.filter_by(id=index).first()
    
        
        subproject = SubProject.query.filter_by(id=subproject).first()
        
        if delete_word == "УДАЛИТЬ":
            db.session.delete(subproject)
            db.session.commit()
            return redirect(url_for('projects.allProjects'))
        
        if name:
            subproject.name = name
        elif description:
            subproject.shortDescription = description

        db.session.commit()    
        return render_template("redact_subproject.html", project=project, user=current_user, subproject=subproject)
    
@projects.route('/projects/<int:index>/<int:subproject>', methods=["POST"])
@login_required
def showSubProject(index, subproject):
    if request.method == "POST":
        create_note = request.form.get('create_note')
        content = request.form.get('content')
        content_id = request.form.get('content_id')
        delete = request.form.get('delete')
        complete = request.form.get('complete')
        
        project = Project.query.filter_by(id=index).first()
        subproject = SubProject.query.filter_by(id=subproject).first()
        
        if create_note:
            note = Note(parent_id=subproject.id, content=create_note, done="False")
            db.session.add(note)
            
        elif delete:
            note = Note.query.filter_by(id=int(delete)).first()
            db.session.delete(note)

        elif complete:   
            note = Note.query.filter_by(id=int(complete)).first()

            if note.done == "True":
                note.done = "False"
            else:
                note.done = "True"

            
        elif content_id:
            note = Note.query.filter_by(id=int(content_id)).first()
            note.content = content
            
        db.session.commit()
        return render_template("show_subproject.html", project=project, user=current_user, subproject=subproject)