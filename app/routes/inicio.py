# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista de inicio.

from flask import Blueprint, redirect, url_for, abort, render_template
from flask_login import login_required
from app.utils import permiso_requerido


inicio_bp = Blueprint('inicio', __name__)

@inicio_bp.route("/")
def start():
    return redirect(url_for("auth.login"))

@inicio_bp.route("/cargar_plantilla/<string:nombre>")
@login_required
@permiso_requerido("crear_peticion")
def get_plantilla(nombre):
    #TODO comprobar si existe plantilla
    return render_template(f"components/tramites/{nombre}.jinja", peticion=None)