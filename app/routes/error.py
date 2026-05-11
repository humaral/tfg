# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas de los errores.

from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)


@error_bp.app_errorhandler(404)
def page_not_found(error): #Carga la plantilla del error 404
    return render_template("error/404.jinja"), 404

@error_bp.app_errorhandler(403)
def page_not_found(error): #Carga la plantilla del error 403
    return render_template("error/403.jinja"), 403

@error_bp.app_errorhandler(501)
def page_not_found(error): #Carga la plantilla del error 501
    return render_template("error/501.jinja"), 501