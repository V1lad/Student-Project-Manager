from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

# This is main page of an application.
@views.route('/')
def main_():
    return render_template("main.html", user=current_user)

# This is user's personal page.
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user, db=db)