import flask
import json

import sirope
import flask_login
from teamplanner.auth.model.userdto import UserDTO

from teamplanner.auth.auth import auth
from teamplanner.tipos.tipos import types_blueprint
from teamplanner.movimientos.movimientos import moves_blueprint
from teamplanner.pokemon.pokemon import pokemon_blueprint
from teamplanner.teams.teams import teams_blueprint


def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    app = flask.Flask(__name__)
    app.config.from_file("config.json", load=json.load)
    srp = sirope.Sirope()
    lmanager.init_app(app)
    
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(types_blueprint, url_prefix="/")
    app.register_blueprint(moves_blueprint, url_prefix="/")
    app.register_blueprint(pokemon_blueprint, url_prefix="/")
    app.register_blueprint(teams_blueprint, url_prefix="/")
    
    return lmanager, srp, app

lmanager, srp, app = create_app()



@lmanager.user_loader
def user_loader(nombre):
    return  UserDTO.find(srp, nombre)


@lmanager.unauthorized_handler
def unauthorized_handler():
    flask.flash("No autorizado")
    return flask.redirect("/")
