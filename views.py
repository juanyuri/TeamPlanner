import flask
import flask_login
import sirope
import uuid

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user

from teamplanner.auth.model.userdto import UserDTO
""" from model.teamdto import TeamDTO
from model.tipodto import TipoDTO
from model.movedto import MovimientoDTO
from model.pokemondto import PokemonDTO """


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