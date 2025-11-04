# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista del dashboard.

from flask import Blueprint, jsonify, render_template, request, session, abort
from flask_login import login_required
from sqlalchemy import select, func, asc, desc, or_, case
from markupsafe import escape
from app.utils import permiso_requerido
from app.models import Peticion, Hito, Estado, Tramite, Empleado, Rol
from app import db
from math import ceil
from unidecode import unidecode


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/peticiones")
@login_required
@permiso_requerido("ver_peticiones")
def peticiones():

    estados_posibles = db.session.scalars(select(Estado))
    tramites_posibles = db.session.scalars(select(Tramite).where(Tramite.activo==True))

    return render_template("peticiones.html", filtro_estados = estados_posibles, filtro_tramites = tramites_posibles)

@dashboard_bp.route("/api/peticiones")
@login_required
@permiso_requerido("ver_peticiones")
def api_peticiones():
    id = request.args.get('id', type=int)
    telefono = request.args.get('telefono', type=int)
    idEstado = request.args.get('estado', type=int)
    idTramite = request.args.get('tramite', type=int)
    empleado = request.args.get('empleado', '')

    orden = request.args.get('orden')
    direccion = request.args.get('direccion')

    per_page = request.args.get('per_page', type=int)
    page = request.args.get('page', type=int)
    paginas_totales = ceil((db.session.scalar(select(func.count()).select_from(Peticion)))/per_page)

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
            #FIX ignorar tildes/mayusc
            aux = unidecode(empleado.lower())
            subq = select(Empleado).where(or_(Empleado.username.like(f"%{aux}%"),Empleado.nombre.like(f"%{aux}%"),Empleado.apellido1.like(f"%{aux}%"))).subquery()
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
    
    peticiones = db.session.scalars(stmt.offset((page-1)*per_page).limit(per_page))

    data = [{
        "id": p.id,
        "telefono": p.telefono,
        "estado": p.estadoActual.valor,
        "tramite": p.tramite.valor,
        "creacion": p.get_fechaCreacion(),
        "asignacion": f"{p.empleadoAsignado.nombre} {p.empleadoAsignado.apellido1}" if p.empleadoAsignado else '-',
    } for p in peticiones]
    
    return jsonify({
        'peticiones': data,
        'ordenActual': orden,
        'direccionActual': direccion,
        'pageActual': page,
        'totalPages': paginas_totales
    })

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
    roles_posibles = db.session.scalars(select(Rol))

    return render_template("empleados.html", filtro_roles = roles_posibles)

@dashboard_bp.route("/api/empleados")
@login_required
@permiso_requerido("ver_empleados")
def api_empleados():
    username = request.args.get('username', '')
    nombre = request.args.get('nombre', '')
    email = request.args.get('email', '')
    idRol = request.args.get('rol', type=int)
    #FIX recibe siempre True, creo que es pq se le pasa 'true' 'false'
    activo = request.args.get('activo', type=bool)
    
    orden = request.args.get('orden')
    direccion = request.args.get('direccion')

    per_page = request.args.get('per_page', type=int)
    page = request.args.get('page', type=int)
    paginas_totales = ceil((db.session.scalar(select(func.count()).select_from(Empleado)))/per_page)

    stmt = select(Empleado)
    if username:
        stmt = stmt.where(Empleado.username.like(f"%{username}%"))
    if nombre:
        stmt = stmt.where(or_(Empleado.nombre.like(f"%{nombre}%"), Empleado.apellido1.like(f"%{nombre}%") ,Empleado.apellido2.like(f"%{nombre}%")))
    if email:
        stmt = stmt.where(Empleado.email.like(f"%{email}%"))
    if idRol:
        stmt = stmt.where(Empleado.idRol==idRol)
    if activo:
        stmt = stmt.where(Empleado.activo==activo)

    direc = asc if direccion == "ascendente" else desc
    
    if orden in ("username", "email"):
        stmt = stmt.order_by(direc(getattr(Empleado, orden)))
    elif orden == "nombre":
        stmt = stmt.order_by(direc(Empleado.nombre), direc(Empleado.apellido1), direc(Empleado.apellido2))
    elif orden == "rol":
        stmt = stmt.join(Rol, Empleado.idRol==Rol.id).order_by(direc(Rol.valor))
    
    
    empleados = db.session.scalars(stmt.offset((page-1)*per_page).limit(per_page))

    data = [{
        "username": e.username,
        "nombre": f"{e.nombre} {e.apellido1}",
        "email": e.email,
        "rol": e.rol.valor,
        "activo": e.activo,
    } for e in empleados]
    
    return jsonify({
        'empleados': data,
        'ordenActual': orden,
        'direccionActual': direccion,
        'pageActual': page,
        'totalPages': paginas_totales
    })

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

