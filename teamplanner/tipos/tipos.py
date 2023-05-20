import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO

tipos = Blueprint('tipos', __name__, template_folder="templates")
srp = sirope.Sirope()

@tipos.route("/types", methods = ['GET','POST'])
@login_required
def types():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        
        tipo = TipoDTO(nombre)
        print(tipo)
        srp.save(tipo)
        
        flash("Tipo creado correctamente", category="success")
        return redirect( url_for("views.dashboard") )
        
    data = {
        "usr": usr
    }
    return flask.render_template("tipos/type-form-add.html", **data)
