import flask
from flask import Blueprint, render_template, request, url_for, flash, redirect
import sirope
from model.userdto import UserDTO

import flask_login
from flask_login import login_required, current_user, logout_user

#Blueprint for application
auth = Blueprint('auth', __name__)


@auth.route("/login" , methods = ['GET','POST'])
def login():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        email = request.form.get("edEmail")
        password = request.form.get("edPassword")
        remember = True if request.form.get('edRemember') else False
        
        if len(nombre) < 4:
            flash("El nombre debe tener una longitud superior a 4", category="error")
        else:
            usr = UserDTO(nombre, email, password)
            flask_login.login_user(usr)
            flash("Usuario registrado correctamente", category="success")
            redirect("main/dashboard")
        #return flask.redirect("main/dashboard")
        
    data = {
        "usr": usr
    }
    
    return flask.render_template("auth/login.html", **data)


@auth.route("/logout")
def logout():
    print("Logged-out user")
    logout_user()
    return flask.redirect(url_for("auth.login"))


@auth.route("/sign-up")
def sign_up():
    return "<h1>Register</h1>"