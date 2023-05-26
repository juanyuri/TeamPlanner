import flask
import flask_login
import sirope
import werkzeug.security as safe

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from teamplanner.auth.model.userdto import UserDTO


#Blueprint for application
auth = Blueprint('auth', __name__, template_folder="templates")
srp = sirope.Sirope()




@auth.route("/login", methods = ['GET','POST'])
def login():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        password = request.form.get("edPassword")
        
        #TODO: Refactorizar a una función if-elses con returns
        if len(nombre) < 2:
            flash("El nombre debe tener una longitud superior a 2", category="error")
        elif len(password) < 4:
            flash("La contraseña debe tener una longitud superior a 4", category="error")
        else:
            usr = UserDTO.find(srp, nombre)
            if not usr:
                flash("Usuario no existente", category="error")
                return redirect("/login")
            
            if not usr.chk_password(password):
                flash("Contraseña incorrecta", category="error")
                return redirect("/login")
            
            login_user(usr)
            flash("Usuario logueado correctamente", category="success")
            return redirect( url_for("views.dashboard") )
            
            
        
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
        
        #TODO: Refactorizar a una función if-elses con returns
        if len(nombre) < 2:
            flash("El nombre debe tener una longitud superior a 2", category="error")
        elif len(email) < 4:
            flash("El email debe tener una longitud superior a 4", category="error")
        elif len(password) < 4:
            flash("La contraseña debe tener una longitud superior a 4", category="error")
        else:
            usr = UserDTO(nombre, email, password_salt)
            srp.save(usr)
            flash("Usuario registrado correctamente", category="success")
            return redirect( url_for(".login") )
            
            
            
        
    data = {
        "usr": usr
    }
    return flask.render_template("auth/registro.html", **data)