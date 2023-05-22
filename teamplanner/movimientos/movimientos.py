import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO
from teamplanner.movimientos.model.movedto import MovimientoDTO

moves_blueprint = Blueprint('moves_blueprint', __name__, template_folder="templates")
srp = sirope.Sirope()

#LIST MOVES
@moves_blueprint.route("/moves", methods = ['GET','POST'])
@login_required
def moves():
    usr = UserDTO.current_user()
    moves = MovimientoDTO.findall(srp)

    data = {
        "usr": usr,
        "moves": moves
    }
    return flask.render_template("movimientos/move-list.html", **data)


#ADD MOVE
@moves_blueprint.route("/moves/add", methods = ['GET','POST'])
@login_required
def add_move():
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
        return redirect( url_for(".moves") )
        
    data = {
        "types": types,
        "usr": usr
    }
    return flask.render_template("movimientos/move-form-add.html", **data)



#EDIT MOVE
@moves_blueprint.route("/moves/edit/<move_name>", methods = ['GET','POST'])
@login_required
def edit_move(move_name):
    usr = UserDTO.current_user()
    move = MovimientoDTO.find(srp, move_name)
    types = TipoDTO.findall(srp)
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        descripcion = request.form.get("edDescripcion")
        categoria = request.form.get("edCategoria")
        potencia = request.form.get("edPotencia")
        tipo = request.form.get("edTipo")
        
        move.nombre = nombre
        move.descripcion = descripcion
        move.categoria = categoria
        move.potencia = potencia
        move.tipo = tipo
        
        srp.save(move)
        
        flash("Movimiento editado correctamente", category="success")
        return redirect( url_for(".moves") )
    
    
    data = {
        "usr": usr,
        "types": types,
        "move": move
    }
    return flask.render_template("movimientos/move-form-edit.html", **data)




#VIEW MOVE
@moves_blueprint.route("/moves/view/<move_name>", methods = ['GET','POST'])
@login_required
def view_move(move_name):
    usr = UserDTO.current_user()
    move = MovimientoDTO.find(srp, move_name)
    print(move)
    
    data = {
        "usr": usr,
        "move": move
    }
    return flask.render_template("movimientos/move-form-view.html", **data)




#DELETE TEAM
@moves_blueprint.route("/moves/delete/<move_name>", methods = ['GET','POST'])
@login_required
def delete_move(move_name):
    usr = UserDTO.current_user()
    move = MovimientoDTO.find(srp, move_name)
    
    if flask.request.method == "POST":
        srp.delete(move)
        flash("Movimiento eliminado correctamente", category="success")
        return redirect( url_for(".moves") )
    
    data = {
        "usr": usr,
        "move": move
    }
    return flask.render_template("movimientos/move-form-delete.html", **data)