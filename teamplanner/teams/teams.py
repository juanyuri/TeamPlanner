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

from datetime import datetime

teams_blueprint = Blueprint('teams_blueprint', __name__, template_folder="templates")
srp = sirope.Sirope()


def check_attrs(nombre, descripcion, codigo, fecha, autor, rating):
    """ Funcion que devuelve un string si existe un error, si no lo hay devuelve cadena vacia """
    
    if len(nombre) <=0 or len(nombre)> 20: return "El nombre debe tener una longitud entre 1 y 20"
    elif not nombre.isalpha():  return "El nombre debe contener solamente letras"
    
    #Validar la descripción
    elif len(descripcion) <= 0 or len(descripcion) > 150: return "La descripción debe tener una longitud entre 1 y 150"
    elif not descripcion.isalnum(): return "La descripción debe contener solamente letras y números"
    
    #Validar codigo
    if len(codigo) != 6 or not codigo.isalnum(): 
        return "El código debe tener exactamente 6 caracteres"
    
    #Validar la fecha
    try:
        fecha_form = datetime.strptime(fecha, "%Y.%m.%d")
        actual = datetime.now()
        
        if fecha_form > actual:
            return "La fecha no puede ser mayor que la actual"
    
    except ValueError:
        return f"La fecha '{fecha}' no tiene el formato correcto (YYYY.MM.DD)"
    
    #Validar el autor
    if not autor.isalpha(): return "El autor debería tener solamente letras. Contacta con admin..."
    
    #Validar el rating
    if not isinstance(rating, int) or rating < 0 or rating > 5:
          return "El rating debe ser un número entero en el rango de 0 y 5"
    
    #Si todos son correctos
    return ""



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
        
        msg_error = check_attrs(nombre, descripcion, codigo_renta, fecha, autor, rating)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".add_team") )
        
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
        
        msg_error = check_attrs(nombre, descripcion, codigo_renta, fecha, autor, rating)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".edit_team", team_code = team_code) )
        
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