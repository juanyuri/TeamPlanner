import flask
# from Flask import Flask, renderTemplate
import sirope
import flask_login
import json
from model.userdto import UserDTO

def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    app = flask.Flask(__name__)
    app.config.from_file("config.json", load=json.load)
    
    srp = sirope.Sirope()
    lmanager.init_app(app)

    return lmanager, srp, app

lmanager, srp, app = create_app()

@lmanager.user_loader
def user_loader(email):
    return UserDto.find(srp, email)

@lmanager.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route("/login" , methods = ['GET','POST'])
def get_login():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = flask.request.form["edNombre"]
        password = flask.request.form["edPassword"]
        usr = UserDTO(nombre, password)
    
    data = {
        "usr": usr
    }
    
    return flask.render_template("auth/login.html", **data)




@app.route("/register" , methods = ['GET','POST'])
def get_register():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = flask.request.form["edNombre"]
        email = flask.request.form["edEmail"]
        password = flask.request.form["edPassword"]
        usr = UserDTO(nombre, email, password)
    
    data = {
        "usr": usr
    }
    
    return flask.render_template("auth/register.html", **data)