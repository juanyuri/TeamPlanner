import flask
import flask_login
import sirope
import werkzeug.security as safe

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from teamplanner.auth.model.userdto import UserDTO
import re

#Blueprint for application
auth = Blueprint('auth', __name__, template_folder="templates")
srp = sirope.Sirope()


def check_name(nombre):
    """ Funcion que devuelve un string si existe un error, si no lo hay devuelve cadena vacia """
    
    if len(nombre) <=0 or len(nombre)> 20: return "El nombre debe tener una longitud entre 1 y 20"
    elif not nombre.isalpha():  return "El nombre debe contener solamente letras"
    
    return ""

def check_email(email):
    PATRON_EMAIL ="^[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z]{2,6}$"
    if not(re.fullmatch(PATRON_EMAIL, email)) or len(email)>30:
       	return "Ingrese un correo electronico valido de hasta máximo de 30 caracteres"
    
    return ""
    


@auth.route("/", methods = ['GET','POST'])
@auth.route("/login", methods = ['GET','POST'])
def login():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        password = request.form.get("edPassword")
        
        msg_error = check_name(nombre)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".login") )
        
        
        usr = UserDTO.find(srp, nombre)
        if not usr:
            flash("Usuario no existente", category="error")
            return redirect("/login")
        
        if not usr.chk_password(password):
            flash("Contraseña incorrecta", category="error")
            return redirect("/login")
        
        login_user(usr)
        flash("Usuario logueado correctamente", category="success")
        return redirect( url_for("teams_blueprint.teams") )
            
            
        
    data = {
        "usr": usr
    }
    
    return flask.render_template("auth/login.html", **data)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada!", category="success")
    return flask.redirect(url_for("auth.login"))



@auth.route("/register", methods = ['GET','POST'])
def register():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        email = request.form.get("edEmail")
        password = request.form.get("edPassword")
        password_salt = safe.generate_password_hash(password)
        
        msg_error = check_name(nombre)
        msg_error_email = check_email(email)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".register") )
        
        if msg_error_email != '':
            flash(msg_error_email, category="error")
            return redirect( url_for(".register") )
        
        usr = UserDTO(nombre, email, password_salt)
        srp.save(usr)
        flash("Usuario registrado correctamente", category="success")
        return redirect( url_for(".login") )
            
            
            
        
    data = {
        "usr": usr
    }
    return flask.render_template("auth/registro.html", **data)