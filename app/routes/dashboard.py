# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista del dashboard.

from flask import Blueprint, jsonify, render_template, request, session, abort
from flask_login import login_required
from sqlalchemy import select, func, asc, desc
from markupsafe import escape
from app.utils import permiso_requerido
from app.models import Peticion, Hito, Estado, Tramite, Empleado
from app import db


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/peticiones")
@login_required
@permiso_requerido("ver_peticiones")
def peticiones():

    estados_posibles = db.session.scalars(select(Estado)).all()
    tramites_posibles = db.session.scalars(select(Tramite).where(Tramite.activo==True)).all()

    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')

    peticiones = db.session.scalars(select(Peticion).limit(10))
    
    return render_template("peticiones.html", filtro_estados = estados_posibles, filtro_tramites = tramites_posibles, orden_actual=escape(orden), direccion_actual=escape(direccion), peticiones=peticiones)

@dashboard_bp.route("/api/peticiones")
@login_required
def api_peticiones():
    id = request.args.get('id', type=int)
    telefono = request.args.get('telefono', type=int)
    idEstado = request.args.get('estado', type=int)
    idTramite = request.args.get('tramite', type=int)
    empleado = request.args.get('empleado', '')

    orden = request.args.get('orden')
    direccion = request.args.get('direccion')

    stmt = select(Peticion)
    if id:
        stmt = stmt.where(Peticion.id.like(f"%{id}%"))
    if telefono:
        stmt = stmt.where(Peticion.telefono.like(f"%{telefono}%"))
    if idEstado:
        stmt = stmt.where(Peticion.idEstadoActual==idEstado)
    if idTramite:
        stmt = stmt.where(Peticion.idTramite==idTramite)
    if empleado:
        #TODO consulta para obtener peticiones dependiendo de si el valor de empleado coincide con el user, nombre o apellido de un empleado
        stmt = stmt
    
    if direccion == "ascendente":
        stmt = stmt.order_by(asc(getattr(Peticion, orden)))
    else:
        stmt = stmt.order_by(desc(getattr(Peticion, orden)))

    peticiones = db.session.scalars(stmt.limit(10))

    data = [{
        "id": p.id,
        "telefono": p.telefono,
        "estado": p.estadoActual.valor,
        "tramite": p.tramite.valor,
        "creacion": p.get_fechaCreacion(),
        "asignacion": f"{p.empleadoAsignado.nombre} {p.empleadoAsignado.apellido1}" if p.empleadoAsignado else '-'
    } for p in peticiones]
    print(data)
    return jsonify(data)


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

