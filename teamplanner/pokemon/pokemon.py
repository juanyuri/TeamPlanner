import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO
from teamplanner.movimientos.model.movedto import MovimientoDTO
from teamplanner.pokemon.model.pokemondto import PokemonDTO

pokemones = Blueprint('pokemones', __name__, template_folder="templates")
srp = sirope.Sirope()


@pokemones.route("/pokemon", methods = ['GET','POST'])
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
    return flask.render_template("pokemon/pkmn-form-add.html", **data)