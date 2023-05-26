import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO
from teamplanner.movimientos.model.movedto import MovimientoDTO
from teamplanner.pokemon.model.pokemondto import PokemonDTO
from teamplanner.teams.model.teamdto import TeamDTO

teams_blueprint = Blueprint('teams_blueprint', __name__, template_folder="templates")
srp = sirope.Sirope()



@teams_blueprint.route("/teams", methods = ['GET','POST'])
@login_required
def teams():
    usr = UserDTO.current_user()
    teams = TeamDTO.findall(srp)
        
    data = {
        "usr": usr,
        "teams": teams
    }
    return flask.render_template("teams/team-list.html", **data)



# ADD TEAM
@teams_blueprint.route("/teams/add", methods = ['GET','POST'])
@login_required
def add_team():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        codigo_renta = request.form.get("edCodigo")
        descripcion = request.form.get("edDescripcion")
        fecha = request.form.get("edFecha")
        rating = request.form.get("edRating")
        autor = usr.nombre
        
        team = TeamDTO(nombre, descripcion, codigo_renta, fecha, autor, rating)
        srp.save(team)
        
        flash("Equipo creado correctamente", category="success")
        return redirect( url_for("teams_blueprint.teams") )
        
    data = {
        "usr": usr
    }
    return flask.render_template("teams/team-form-add.html", **data)



# EDIT TEAM
@teams_blueprint.route("/teams/edit/<team_code>", methods = ['GET','POST'])
@login_required
def edit_team(team_code):
    usr = UserDTO.current_user()
    equipo = TeamDTO.find(srp, team_code)
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        codigo_renta = request.form.get("edCodigo")
        descripcion = request.form.get("edDescripcion")
        fecha = request.form.get("edFecha")
        rating = request.form.get("edRating")
        autor = usr.nombre
        
        equipo.nombre = nombre
        equipo.descripcion = descripcion
        equipo.fecha = fecha
        equipo.rating = rating
        
        srp.save(equipo)
        
        flash("Equipo editado correctamente", category="success")
        return redirect( url_for("teams_blueprint.teams") )
    
    
    data = {
        "usr": usr,
        "team": equipo
    }
    return flask.render_template("teams/team-form-edit.html", **data)



# VIEW TEAM
@teams_blueprint.route("/teams/view/<team_code>", methods = ['GET','POST'])
@login_required
def view_team(team_code):
    usr = UserDTO.current_user()
    equipo = TeamDTO.find(srp, team_code)
    
    
    data = {
        "usr": usr,
        "team": equipo
    }
    return flask.render_template("teams/team-form-view.html", **data)




# DELETE TEAM
@teams_blueprint.route("/teams/delete/<team_code>", methods = ['GET','POST'])
@login_required
def delete_team(team_code):
    usr = UserDTO.current_user()
    equipo = TeamDTO.find(srp, team_code)
    
    if flask.request.method == "POST":
        srp.delete(equipo.__oid__)
        flash("Equipo eliminado correctamente", category="success")
        return redirect( url_for("teams_blueprint.teams") )
    
    data = {
        "usr": usr,
        "team": equipo
    }
    return flask.render_template("teams/team-form-delete.html", **data)