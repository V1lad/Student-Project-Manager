from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import login_required, current_user
from datetime import datetime
from models import Project

testing = Blueprint('projects', __name__)

@testing.route('/projects', methods=["GET"])
@login_required
def projects():
    projects = Project.query.first()
    project = Project(ownerId=current_user.id, firstName=firstName, password=password1, status="inactive")
    return render_template("projects.html", user=current_user, available_projects = projects)

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