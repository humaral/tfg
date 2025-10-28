# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas de los errores.

from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)


@error_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404