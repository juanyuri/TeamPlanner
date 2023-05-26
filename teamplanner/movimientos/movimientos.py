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


def check_attrs(nombre, descripcion, categoria, potencia, tipo):
    """ Funcion que devuelve un string si existe un error, si no lo hay devuelve cadena vacia """
    
    if len(nombre) <=0 or len(nombre)> 20: return "El nombre debe tener una longitud entre 1 y 20"
    elif not nombre.isalpha():  return "El nombre debe contener solamente letras"
    
    #Validar la descripción
    elif len(descripcion) <= 0 or len(descripcion) > 150: return "La descripción debe tener una longitud entre 1 y 150"
    elif not descripcion.replace(' ','').isalnum(): return "La descripción debe contener solamente letras y números"
    
    #Validar la categoría
    elif not categoria.isalpha(): return "La categoría debería tener solamente letras"
    
    #Validar la potencia
    elif not isinstance(potencia, int) or nivel < 0 or nivel > 150:
        return "La potencia debe ser un número entero en el rango de 0 y 150"
    
    #Validar el tipo
    elif len(tipo) <=0 or len(tipo)> 20: return "El tipo elegido debe tener una longitud entre 1 y 20"
    elif not tipo.isalpha():  return "El tipo debe contener solamente letras"
    
    #Si todos son correctos
    return ""


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
        
        msg_error = check_attrs(nombre, descripcion, categoria, potencia, tipo)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".add_move") )
        
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
        
        msg_error = check_attrs(nombre, descripcion, categoria, potencia, tipo)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".edit_move", move_name = move_name) )
        
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
        srp.delete(move.__oid__)
        flash("Movimiento eliminado correctamente", category="success")
        return redirect( url_for(".moves") )
    
    data = {
        "usr": usr,
        "move": move
    }
    return flask.render_template("movimientos/move-form-delete.html", **data)