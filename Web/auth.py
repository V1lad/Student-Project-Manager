from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Вы успешно вошли в аккаунт!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Аккаунта с такой почтой не существует', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        auth__level = request.form.get('auth__level')
        code = request.form.get('code')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Аккаунт с такой почтой уже существует', category='error')
        elif len(email) < 4:
            flash("Потчовый адрес должен быть длиннее 4 символов", category="error")
        elif len(firstName) < 2:
            flash("Имя должно состоять более чем из одного символа", category="error")
        elif password1 != password2:
            flash("Пароли не совпадают", category="error")
        elif len(password1) < 7:
            flash("Пароль должен быть длиннее 7 символов", category="error")
        elif not(auth__level != "admin" or auth__level != "teacher" or auth__level != "admin_sys" or auth__level != "admin_teach"):
            flash("Неверно указана роль аккаунта", category="error")
        elif auth__level == "admin_sys" and code != "admincodetmp":
            flash("Неверный код для админа", category="error")
        else:
            if auth__level == "admin_sys":
                new_user = User(email=email, firstName=firstName, password=password1, status="active")
            else:
                new_user = User(email=email, firstName=firstName, password=password1, status="inactive")

            if auth__level == "teacher":
                teacher = Role(name='teacher')
                curr_role = teacher

            elif auth__level == "admin_sys":
                flag = True
                for i in User.query.all():
                    if i.roles[0].name == "admin_sys":
                        flag = False
                if flag:
                    admin_sys = Role(name="admin_sys")
                    curr_role = admin_sys
                else:
                    admin_sys = Role(name="admin_sys")
                    curr_role = admin_sys
                    new_user.status = "inactive"

            elif auth__level == "admin_teach":
                admin_teach = Role(name="admin_teach")
                curr_role = admin_teach

            else:
                student = Role(name='student')
                curr_role = student

            new_user.roles = [curr_role]
            db.session.add(new_user)
            db.session.commit()

            flash("Аккаунт создан", category="success")
            return redirect(url_for('auth.login'))
    return render_template("sign_up.html", user=current_user)
