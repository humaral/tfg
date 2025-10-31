# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista del dashboard.

from flask import Blueprint, render_template, request, session, abort
from flask_login import login_required
from sqlalchemy import select
from markupsafe import escape
from datetime import datetime
from app.utils import permiso_requerido
from app.models import Peticion, Hito
from app import db


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/peticiones")
@login_required
@permiso_requerido("ver_peticiones")
def peticiones():
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("peticiones.html", orden_actual=escape(orden), direccion_actual=escape(direccion))

@dashboard_bp.route("/peticiones/<int:idPeticion>")
@login_required
@permiso_requerido("ver_peticiones")
def sumary_peticion(idPeticion):

    stmt = select(Peticion).where(Peticion.id==idPeticion)
    peticion = db.session.scalars(stmt).first()

    stmt = select(Hito).where(Hito.idPeticion==idPeticion)
    historial = db.session.scalars(stmt).all()

    return render_template("sumaryPeticion.html", peticion=peticion, historial=historial)

@dashboard_bp.route("/empleados")
@login_required
@permiso_requerido("ver_empleados")
def empleados():
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("empleados.html", orden_actual=escape(orden), direccion_actual=escape(direccion))

@dashboard_bp.route("/empleados/new")
@login_required
@permiso_requerido("crear_empleado")
def new_empleado():
    return render_template("registroEmpleados.html")

@dashboard_bp.route("/estadisticas")
@login_required
@permiso_requerido("ver_estadisticas")
def estadisticas():
    if "ver_estadisticas_generales" in session["permisos"]:
        return render_template("estadisticas.html")
    elif "ver_estadisticas_secretario" in session["permisos"]:
        return render_template("estadisticas.html")
    else:
        abort(404)

