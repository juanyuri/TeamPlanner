import flask
import flask_login
import sirope
import uuid

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from teamplanner.auth.model.userdto import UserDTO
from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO
from teamplanner.movimientos.model.movedto import MovimientoDTO
from teamplanner.pokemon.model.pokemondto import PokemonDTO
from teamplanner.teams.model.teamdto import TeamDTO


#Blueprint for application
views = Blueprint('views', __name__)
srp = sirope.Sirope()

@views.route("/dashboard")
@login_required
def dashboard():
    usr = UserDTO.current_user()
    tipos = TipoDTO.findall(srp)
    moves = MovimientoDTO.findall(srp)
    
    data = {
        "usr": usr,
        "types" : tipos,
        "moves" : moves
    }
    return flask.render_template("dashboard.html", **data)