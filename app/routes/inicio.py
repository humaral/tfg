# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista de inicio.

from flask import Blueprint, redirect, url_for

inicio_bp = Blueprint('inicio', __name__)
@inicio_bp.route("/")
def start():
    return redirect(url_for("auth.login"))