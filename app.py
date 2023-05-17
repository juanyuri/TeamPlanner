import flask
import json

import sirope
import flask_login
from model.userdto import UserDTO

from auth import auth
from views import views


def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    app = flask.Flask(__name__)
    app.config.from_file("config.json", load=json.load)
    srp = sirope.Sirope()
    lmanager.init_app(app)
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return lmanager, srp, app

lmanager, srp, app = create_app()



#TODO: Refactorizar y poner en auth.py
@lmanager.user_loader
def user_loader(email):
    return UserDTO.find(srp, email)



@lmanager.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")
