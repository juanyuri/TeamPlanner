import flask
import flask_login
import sirope

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from teamplanner.auth.model.userdto import UserDTO
from teamplanner.tipos.model.tipodto import TipoDTO


types_blueprint = Blueprint('types_blueprint', __name__, template_folder="templates")
srp = sirope.Sirope()


def check_attrs(nombre):
    """ Funcion que devuelve un string si existe un error, si no lo hay devuelve cadena vacia """
    
    if len(nombre) <=0 or len(nombre)> 20: return "El nombre debe tener una longitud entre 0 y 20"
    elif not nombre.isalpha():  return "El nombre debe contener solamente letras"
    return ""




# LIST TYPES
@types_blueprint.route("/types", methods = ['GET','POST'])
@login_required
def types():
    usr = UserDTO.current_user()
    types = TipoDTO.findall(srp)
        
    data = {
        "usr": usr,
        "tipos": types
    }
    return flask.render_template("tipos/type-list.html", **data)



# ADD TYPE
@types_blueprint.route("/types/add", methods = ['GET','POST'])
@login_required
def add_type():
    usr = UserDTO.current_user()
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        
        msg_error = check_attrs(nombre)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".add_type") )
        
        
        tipo = TipoDTO(nombre)
        srp.save(tipo)
        
        flash("Tipo creado correctamente", category="success")
        return redirect( url_for(".types") )
        
    data = {
        "usr": usr
    }
    return flask.render_template("tipos/type-form-add.html", **data)




# EDIT TYPE
@types_blueprint.route("/types/edit/<type_name>", methods = ['GET','POST'])
@login_required
def edit_type(type_name):
    usr = UserDTO.current_user()
    tipo = TipoDTO.find(srp, type_name)
    
    if flask.request.method == "POST":
        nombre = request.form.get("edNombre")
        
        msg_error = check_attrs(nombre)
        if msg_error != '':
            flash(msg_error, category="error")
            return redirect( url_for(".edit_type", type_name = type_name) )
        
        tipo.nombre = nombre
        srp.save(tipo)
        
        flash("Tipo editado correctamente", category="success")
        return redirect( url_for(".types") )
    
    
    data = {
        "usr": usr,
        "tipo": tipo
    }
    return flask.render_template("tipos/type-form-edit.html", **data)



# VIEW TEAM
@types_blueprint.route("/types/view/<type_name>", methods = ['GET','POST'])
@login_required
def view_type(type_name):
    usr = UserDTO.current_user()
    tipo = TipoDTO.find(srp, type_name)
    
    data = {
        "usr": usr,
        "tipo": tipo
    }
    return flask.render_template("tipos/type-form-view.html", **data)




# DELETE TEAM
@types_blueprint.route("/types/delete/<type_name>", methods = ['GET','POST'])
@login_required
def delete_type(type_name):
    usr = UserDTO.current_user()
    tipo = TipoDTO.find(srp, type_name)
    
    if flask.request.method == "POST":
        srp.delete(tipo.__oid__)
        flash("Tipo eliminado correctamente", category="success")
        return redirect( url_for(".types") )
    
    data = {
        "usr": usr,
        "tipo": tipo
    }
    return flask.render_template("tipos/type-form-delete.html", **data)