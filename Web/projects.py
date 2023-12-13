from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_required, current_user
from .models import Project, User
import json

projects = Blueprint('projects', __name__)

@projects.route('/projects', methods=["GET"])
@login_required
def allProjects():
    
    #info = json.dumps({"KEY1":[1,2,3,4,5], "KEY2":3})
    #project = Project(ownerId=current_user.id, name="test", allowedUsers = info, shortDescription = "1", fullDescription = "2")
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

@projects.route('/projects/<int:index>', methods=["GET", "POST"])
@login_required
def showProject(index):
    # Надо сделать проверку на доступ к проекту.
    
    project = Project.query.filter_by(id=index).first()
    return render_template("show_project.html", project=project, user=current_user )

'''
@testing.route('/testing', methods=["POST", "GET"])
@login_required
def test():
    if current_user.roles[0].name == 'student' and current_user.status == "active":

        tasks_to_delete = check_tasks()

        if request.method == 'POST':
            if request.form.get("task"):
                task = request.form.get("task")
                task = Task.query.get(int(task))

                return render_template("active_testing.html", user=current_user, task=task)
            else:
                data = request.form
                task_id = int(request.form.get("task_id"))
                questions_ans = {}
                for question in data:
                    if question != "task_id":
                        questions_ans[Question.query.get(int(question))] = data[question]

                questions_results = {}

                correct_answers = 0
                incorrect_answers = 0

                for question in questions_ans:
                    if question.check(questions_ans[question]):
                        questions_results[question.id] = True
                        correct_answers += 1
                    else:
                        questions_results[question.id] = False
                        incorrect_answers += 1

                if incorrect_answers:
                    percentage=(correct_answers/(incorrect_answers + correct_answers)) * 100
                else:
                    percentage = 100

                if percentage > 85:
                    mark = 5
                elif 70 < percentage < 86:
                    mark = 4
                elif 50 < percentage:
                    mark = 3
                else:
                    mark = 2

                flag = True
                for res in current_user.results:
                    if res.test_id == task_id:
                        flag = False

                if flag:
                    new_result = Result(test_id=task_id, student_id=current_user.id, content=code(questions_results), percentage=percentage, mark=mark, task_name=Task.query.get(task_id).name)

                    db.session.add(new_result)
                    db.session.commit()

                return redirect(url_for("testing.results"))

        params = []
        for i in current_user.results:
            params.append(i.test_id)

        # for task in Task.query.all():
        #     if not task.questions and (task.status == "active" or task.status == "planned" or task.status == "inactive"):
        #         db.session.delete(task)
        #         db.session.commit()

        return render_template("testing.html", user=current_user, params=params)
    else:
        return "Для вашего типа аккаунта данная страница не доступна"


@testing.route('/testing_results', methods=["POST", "GET"])
@login_required
def results():
    if current_user.roles[0].name == 'student' and current_user.status == "active":
        return render_template("testing_results.html", user=current_user, Question=Question, Task=Task, decode=decode)
    else:
        return "Для вашего типа аккаунта данная страница не доступна"


def check_tasks():
    tasks_to_delete = []
    for task in Task.query.all():
        if task.status == "planned":
            if get_date(task.beginning_time) < datetime.now():
                task.status = "active"
        elif task.status == "active":
            if get_date(task.ending_time) < datetime.now():
                tasks_to_delete.append(task)
                task.status = "inactive"
                for group in task.groups:
                    for student in group.members:
                        flag = False
                        for result in student.results:
                            if result.test_id == task.id:
                                flag = True
                        if not flag:
                            contents = {}
                            for question in task.questions:
                                contents[question.id] = 0
                            new_result = Result(test_id=task.id, student_id=student.id, content=code(contents), percentage=0, mark=2, task_name=task.name)
                            db.session.add(new_result)
        db.session.commit()


    return tasks_to_delete
'''