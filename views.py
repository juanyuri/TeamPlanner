import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from model.userdto import UserDTO


#Blueprint for application
views = Blueprint('views', __name__)

@views.route("/dashboard")
@login_required
def home():
    usr = UserDTO.current_user()
    data = {
        "usr": usr
    }
    return flask.render_template("main/dashboard.html", **data)

