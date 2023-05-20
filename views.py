import flask
import flask_login
import sirope
import uuid

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from model.userdto import UserDTO
from model.teamdto import TeamDTO
from model.tipodto import TipoDTO
from model.movedto import MovimientoDTO
from model.pokemondto import PokemonDTO


#Blueprint for application
views = Blueprint('views', __name__)
srp = sirope.Sirope()

@views.route("/dashboard")
@login_required
def dashboard():
    usr = UserDTO.current_user()
    teams = TeamDTO.findall(srp)
    tipos = TipoDTO.findall(srp)
    moves = MovimientoDTO.findall(srp)
    
    data = {
        "usr": usr,
        "teams": teams,
        "types" : tipos,
        "moves" : moves
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
        srp.save(team)
        
        flash("Equipo creado correctamente", category="success")
        return redirect( url_for("views.dashboard") )
        
    data = {
        "usr": usr
    }
    return flask.render_template("main/team-form-add.html", **data)



@views.route("/types", methods = ['GET','POST'])
@login_required
def types():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        
        tipo = TipoDTO(nombre)
        srp.save(tipo)
        
        flash("Tipo creado correctamente", category="success")
        return redirect( url_for("views.dashboard") )
        
    data = {
        "usr": usr
    }
    return flask.render_template("main/type-form-add.html", **data)





@views.route("/moves", methods = ['GET','POST'])
@login_required
def moves():
    usr = UserDTO.current_user()
    types = TipoDTO.findall(srp)
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        descripcion = request.form.get("edDescripcion")
        categoria = request.form.get("edCategoria")
        potencia = request.form.get("edPotencia")
        tipo = request.form.get("edTipo")    
         
        move = MovimientoDTO(nombre, descripcion, categoria, potencia, tipo)
        srp.save(move)
        
        flash("Movimiento creado correctamente", category="success")
        return redirect( url_for("views.dashboard") )
        
    data = {
        "types": types,
        "usr": usr
    }
    return flask.render_template("main/move-form-add.html", **data)




@views.route("/pokemon", methods = ['GET','POST'])
@login_required
def pokemon():
    usr = UserDTO.current_user()
    types = TipoDTO.findall(srp)
    moves = MovimientoDTO.findall(srp)
    
    if flask.request.method == "POST":
        especie = request.form.get("edEspecie")
        pokedex = request.form.get("edPokedex")
        nivel = request.form.get("edNivel")
        move1 = request.form.get("edMove1")
        move2 = request.form.get("edMove2")
        tipo = request.form.get("edTipo")
        
        id = 1
        pkmn = PokemonDTO(id, especie, pokedex, nivel, move1, move2, tipo)

        print(pkmn)
        srp.save(pkmn)
        
        flash("Pokémon creado correctamente", category="success")
        return redirect( url_for("views.dashboard") )
        
    data = {
        "types": types,
        "moves": moves,
        "usr": usr
    }
    return flask.render_template("main/pkmn-form-add.html", **data)