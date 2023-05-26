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

pokemon_blueprint = Blueprint('pokemon_blueprint', __name__, template_folder="templates")
srp = sirope.Sirope()


@pokemon_blueprint.route("/pokemon", methods = ['GET','POST'])
@login_required
def pokemon():
    usr = UserDTO.current_user()
    pokemon = PokemonDTO.findall(srp)
        
    data = {
        "usr": usr,
        "pokemon": pokemon
    }
    return flask.render_template("pokemon/pkmn-list.html", **data)


@pokemon_blueprint.route("/pokemon/add", methods = ['GET','POST'])
@login_required
def add_pokemon():
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
        
        #def __init__(self, id, especie, num_pokedex, nivel, move1, move2, tipo):
        pkmn = PokemonDTO(1, especie, pokedex, nivel, move1, move2, tipo)
        print(pkmn)

        srp.save(pkmn)
        
        flash("Pokémon creado correctamente", category="success")
        return redirect( url_for("pokemon_blueprint.pokemon") )
        
    data = {
        "types": types,
        "moves": moves,
        "usr": usr
    }
    return flask.render_template("pokemon/pkmn-form-add.html", **data)



#EDIT MOVE
@pokemon_blueprint.route("/pokemon/edit/<pkmn_sp>", methods = ['GET','POST'])
@login_required
def edit_pokemon(pkmn_sp):
    usr = UserDTO.current_user()
    pkmn = PokemonDTO.find(srp, pkmn_sp)
    print(pkmn)
    moves = MovimientoDTO.findall(srp)
    types = TipoDTO.findall(srp)
    
    if flask.request.method == "POST":
        especie = request.form.get("edEspecie")
        pokedex = request.form.get("edPokedex")
        nivel = request.form.get("edNivel")
        move1 = request.form.get("edMove1")
        move2 = request.form.get("edMove2")
        tipo = request.form.get("edTipo")
        
        pkmn.especie = especie
        pkmn.nivel = nivel
        pkmn.pokedex = pokedex
        pkmn.nivel = nivel
        pkmn.move1 = move1
        pkmn.move2 = move2
        pkmn.tipo = tipo
        
        srp.save(pkmn)
        
        flash("Pokemon editado correctamente", category="success")
        return redirect( url_for("pokemon_blueprint.pokemon") )
    
    
    data = {
        "usr": usr,
        "pkmn": pkmn,
        "types": types,
        "moves": moves
    }
    return flask.render_template("pokemon/pkmn-form-edit.html", **data)




#VIEW MOVE
@pokemon_blueprint.route("/pokemon/view/<pkmn_sp>", methods = ['GET','POST'])
@login_required
def view_pokemon(pkmn_sp):
    usr = UserDTO.current_user()
    pkmn = PokemonDTO.find(srp, pkmn_sp)
    
    data = {
        "usr": usr,
        "pkmn": pkmn
    }
    return flask.render_template("pokemon/pkmn-form-view.html", **data)




#DELETE TEAM
@pokemon_blueprint.route("/pokemon/delete/<pkmn_sp>", methods = ['GET','POST'])
@login_required
def delete_pokemon(pkmn_sp):
    usr = UserDTO.current_user()
    pkmn = PokemonDTO.find(srp, pkmn_sp)
    
    if flask.request.method == "POST":
        srp.delete(pkmn.__oid__)
        flash("Pokemon eliminado correctamente", category="success")
        return redirect( url_for("pokemon_blueprint.pokemon") )
    
    data = {
        "usr": usr,
        "pkmn": pkmn
    }
    return flask.render_template("pokemon/pkmn-form-delete.html", **data)