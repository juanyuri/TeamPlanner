import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from model.userdto import UserDTO
from model.teamdto import TeamDTO


#Blueprint for application
views = Blueprint('views', __name__)
srp = sirope.Sirope()

@views.route("/dashboard")
@login_required
def dashboard():
    usr = UserDTO.current_user()
    teams = TeamDTO.findall(srp)
    
    data = {
        "usr": usr,
        "teams": teams
    }
    return flask.render_template("main/dashboard.html", **data)


@views.route("/teams", methods = ['GET','POST'])
@login_required
def teams():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        codigo_renta = request.form.get("edCodigo")
        descripcion = request.form.get("edDescripcion")
        fecha = request.form.get("edFecha")
        rating = request.form.get("edRating")
        autor = usr.nombre
        
        team = TeamDTO(nombre, descripcion, codigo_renta, fecha, autor, rating)
        print("[Equipo]: ")
        srp.save(team)
        
        flash("Equipo creado correctamente", category="success")
        return redirect( url_for("views.dashboard") )
        
    data = {
        "usr": usr
    }
    return flask.render_template("main/pkmn-form-add.html", **data)