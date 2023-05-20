import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO
from teamplanner.movimientos.model.movedto import MovimientoDTO

movimientos = Blueprint('movimientos', __name__, template_folder="templates")
srp = sirope.Sirope()

@movimientos.route("/moves", methods = ['GET','POST'])
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
    return flask.render_template("movimientos/move-form-add.html", **data)
