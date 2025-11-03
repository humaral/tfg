# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista del dashboard.

from flask import Blueprint, jsonify, render_template, request, session, abort
from flask_login import login_required
from sqlalchemy import select, func, asc, desc, or_, case
from markupsafe import escape
from app.utils import permiso_requerido
from app.models import Peticion, Hito, Estado, Tramite, Empleado
from app import db


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/peticiones")
@login_required
@permiso_requerido("ver_peticiones")
def peticiones():

    estados_posibles = db.session.scalars(select(Estado))
    tramites_posibles = db.session.scalars(select(Tramite).where(Tramite.activo==True))

    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    stmt = select(Peticion).limit(10)
    if direccion == "ascendente":
        stmt = stmt.order_by(asc(getattr(Peticion, orden)))
    else:
        stmt = stmt.order_by(desc(getattr(Peticion, orden)))

    paginas_totales = db.session.scalar(select(func.count()).select_from(Peticion))

    peticiones = db.session.scalars(stmt.offset((page-1)*per_page).limit(per_page))


    return render_template("peticiones.html", filtro_estados = estados_posibles, filtro_tramites = tramites_posibles, orden_actual=escape(orden), direccion_actual=escape(direccion), peticiones=peticiones, page_actual=escape(page), per_page=escape(per_page))

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

    per_page = request.args.get('per_page', type=int)


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
        if empleado=='-':
            stmt = stmt.where(Peticion.idEmpleadoAsignado.is_(None))
        else:
            subq = select(Empleado).where(or_(Empleado.username.like(f"%{empleado}%"),Empleado.nombre.like(f"%{empleado}%"),Empleado.apellido1.like(f"%{empleado}%"))).subquery()
            stmt = stmt.join(subq, Peticion.idEmpleadoAsignado == subq.c.id)
    
    direc = asc if direccion == "ascendente" else desc
    
    if orden in ("id", "telefono"):
        stmt = stmt.order_by(direc(getattr(Peticion, orden)))
    elif orden == "estado":
        stmt = stmt.join(Estado, Peticion.idEstadoActual==Estado.id).order_by(direc(Estado.valor))
    elif orden == "tramite":
        stmt = stmt.join(Tramite, Peticion.idTramite==Tramite.id).order_by(direc(Tramite.valor))
    elif orden == "creacion":
        #TEST comprobar que funcion ya que el insert pone todas las peticiones con la misma fechas
        stmt = stmt.join(Hito, (Peticion.id==Hito.idPeticion) & (Peticion.idEstadoActual == Hito.idEstado)).order_by(direc(Hito.updated_at))
    elif orden == "asignacion":
        stmt = stmt.outerjoin(Empleado, Peticion.idEmpleadoAsignado==Empleado.id).order_by(direc(Empleado.username).nulls_last(), direc(Peticion.id))
    
    peticiones = db.session.scalars(stmt.limit(per_page))


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
    peticion = db.session.scalar(stmt)
    stmt = select(Hito).where(Hito.idPeticion==idPeticion)
    historial = db.session.scalars(stmt)

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

