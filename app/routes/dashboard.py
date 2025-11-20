# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista del dashboard.

from flask import Blueprint, jsonify, render_template, request, session, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import select, func, asc, desc, or_
from app.utils import permiso_requerido, temporal_password, verificar_permiso, rpa_certificado_empadronamiento, crear_peticion
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
            subq = select(Empleado).where(or_(
                Empleado.username.ilike(f"%{empleado}%"),
                Empleado.nombre.ilike(f"%{empleado}%"),
                Empleado.apellido1.ilike(f"%{empleado}%"),
                Empleado.apellido2.ilike(f"%{empleado}%")
                )).subquery()
            stmt = stmt.join(subq, Peticion.idEmpleadoAsignado == subq.c.id)
    
    direc = asc if direccion == "ascendente" else desc
    
    if orden in ("id", "telefono"):
        stmt = stmt.order_by(direc(getattr(Peticion, orden)))
    elif orden == "estado":
        stmt = stmt.join(Estado, Peticion.idEstadoActual==Estado.id).order_by(direc(func.lower(Estado.valor)))
    elif orden == "tramite":
        stmt = stmt.join(Tramite, Peticion.idTramite==Tramite.id).order_by(direc(func.lower(Tramite.valor)))
    elif orden == "creacion":
        #TEST comprobar que funcion ya que el insert pone todas las peticiones con la misma fechas
        stmt = stmt.join(Hito, (Peticion.id==Hito.idPeticion) & (Peticion.idEstadoActual == Hito.idEstado)).order_by(direc(Hito.updated_at))
    elif orden == "asignacion":
        stmt = stmt.outerjoin(Empleado, Peticion.idEmpleadoAsignado==Empleado.id).order_by(direc(func.lower(Empleado.username)).nulls_last(), direc(Peticion.id))
    
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

@dashboard_bp.route("/peticiones/<int:idPeticion>", methods=["GET", "POST"])
@login_required
@permiso_requerido("ver_peticiones")
def sumary_peticion(idPeticion):

    stmt = select(Peticion).where(Peticion.id==idPeticion)
    peticion = db.session.scalar(stmt)

    if(peticion == None):
        abort(404)

    if request.method =="POST":
        
        if 'completar' in request.form:
            rpa_certificado_empadronamiento(peticion.informacion)
            peticion.idEstadoActual = 5
            db.session.flush()
            newHito = Hito(idPeticion = peticion.id, idEstado = peticion.idEstadoActual, updated_by = peticion.idEmpleadoAsignado)
            db.session.add(newHito)
            peticion.idEmpleadoAsignado = None
            db.session.commit()

        elif 'asignar' in request.form:
            peticion.idEstadoActual = 4
            peticion.idEmpleadoAsignado = current_user.id
            db.session.flush()
            newHito = Hito(idPeticion = peticion.id, idEstado = peticion.idEstadoActual, updated_by = peticion.idEmpleadoAsignado)
            db.session.add(newHito)
            db.session.commit()

        elif 'actualizar' in request.form:
            informacion = {k:v for k, v in request.form.items() if k !="actualizar"}
            peticion.informacion = informacion
            db.session.commit()

        elif 'cancelar' in request.form:
            peticion.idEstadoActual = 6
            db.session.flush()
            newHito = Hito(idPeticion = peticion.id, idEstado = peticion.idEstadoActual, updated_by = peticion.idEmpleadoAsignado)
            db.session.add(newHito)
            peticion.idEmpleadoAsignado = None
            db.session.commit()

    historial = db.session.scalars(select(Hito).where(Hito.idPeticion==idPeticion))

    return render_template("sumaryPeticion.html", peticion=peticion, historial=historial)

@dashboard_bp.route("/new/peticion", methods=["GET", "POST"])
@login_required
@permiso_requerido("crear_peticion")
def new_peticion():
    
    tramites = db.session.scalars(select(Tramite).where(Tramite.activo==True))
    
    if request.method == "POST":

        telefonoLlamada = request.form["telefonoLlamada"]
        tramite = request.form["tramite"]
        idTramite = db.session.scalar(select(Tramite.id).where(Tramite.valor==tramite))

        informacion = {k:v for k, v in request.form.items() if k not in ["telefonoLlamada", "tramite"]}

        idPeticion = crear_peticion(telefonoLlamada, idTramite, informacion)

        return redirect(url_for("dashboard.sumary_peticion", idPeticion=idPeticion))

    return render_template("crearPeticion.html", tramites=tramites)


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
    activo = request.args.get('activo', '') in ['true', 'on', '1']

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
   
    stmt = stmt.where(Empleado.activo==activo)

    direc = asc if direccion == "ascendente" else desc
    
    if orden in ("username", "email"):
        stmt = stmt.order_by(direc(func.lower(getattr(Empleado, orden))))
    elif orden == "nombre":
        stmt = stmt.order_by(direc(func.lower(Empleado.nombre)), direc(func.lower(Empleado.apellido1)), direc(func.lower(Empleado.apellido2)))
    elif orden == "rol":
        stmt = stmt.join(Rol, Empleado.idRol==Rol.id).order_by(direc(func.lower(Rol.valor)))
    
    empleados = db.session.scalars(stmt.offset((page-1)*per_page).limit(per_page))

    data = [{
        "id": e.id,
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

@dashboard_bp.route("/empleado", methods=["GET", "POST"])
@login_required
def edit_empleado():

    idEmpleadoEditar = request.args.get('id', type=int)
    empleadoEditar = db.session.scalar(select(Empleado).where(Empleado.id == idEmpleadoEditar))

    if empleadoEditar:
        verificar_permiso("editar_empleado")
    else:
        verificar_permiso("crear_empleado")

    if request.method == "POST":
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        email = request.form['email']
        rol = int(request.form['rol'])
        activo = 'activo' in request.form
        
        if empleadoEditar:
            empleadoEditar.nombre = nombre
            empleadoEditar.apellido1 = apellido1
            empleadoEditar.apellido2 = apellido2
            empleadoEditar.email = email
            empleadoEditar.idRol = rol
            empleadoEditar.activo = activo
            db.session.commit()
            return redirect(url_for("dashboard.empleados"))
        else:

            stmt = select(Empleado).where(Empleado.email==email)
            empleado = db.session.scalar(stmt)
            if empleado:
                flash("Ya existe un empleado con ese email.", "error")
            else:
                newEmpleado = Empleado(nombre=nombre, apellido1=apellido1, apellido2=apellido2, email=email, idRol=rol, activo=activo)

                newEmpleado.username = newEmpleado.generar_username()
                tempPass = temporal_password()
                newEmpleado.set_password(tempPass)
                db.session.add(newEmpleado)
                db.session.commit()
                return redirect(url_for("dashboard.empleados"))
    
    return render_template("editarEmpleado.html", empleado=empleadoEditar)


@dashboard_bp.route("/tramites")
@login_required
@permiso_requerido("ver_tramites")
def tramites():

    return render_template("tramites.html")

@dashboard_bp.route("/api/tramites")
@login_required
@permiso_requerido("ver_tramites")
def api_tramites():
    id = request.args.get('username', '')
    valor = request.args.get('valor', '')
    activo = request.args.get('activo', '') in ['true', 'on', '1']

    orden = request.args.get('orden')
    direccion = request.args.get('direccion')

    per_page = request.args.get('per_page', type=int)
    page = request.args.get('page', type=int)
    paginas_totales = ceil((db.session.scalar(select(func.count()).select_from(Tramite)))/per_page)

    stmt = select(Tramite)
    if id:
        stmt = stmt.where(Tramite.id.like(f"%{id}%"))
    if valor:
        stmt = stmt.where(Tramite.valor.like(f"%{valor}%"))
   
    stmt = stmt.where(Tramite.activo==activo)

    direc = asc if direccion == "ascendente" else desc

    if orden == "id":
        stmt = stmt.order_by(direc(Tramite.id))
    elif orden == "valor":
        stmt = stmt.order_by(direc(func.lower(Tramite.valor)))
    
    tramites = db.session.scalars(stmt.offset((page-1)*per_page).limit(per_page))

    data = [{
        "id": t.id,
        "nombre": t.valor,
        "activo": t.activo,
    } for t in tramites]
    
    return jsonify({
        'tramites': data,
        'ordenActual': orden,
        'direccionActual': direccion,
        'pageActual': page,
        'totalPages': paginas_totales
    })

@dashboard_bp.route("/edit/tramite", methods=["GET", "POST"])
@login_required
def edit_tramite():

    idTramiteEditar = request.args.get("id", type=int)
    tramiteEditar = db.session.scalar(select(Tramite).where(Tramite.id==idTramiteEditar))

    if tramiteEditar:
        verificar_permiso("editar_tramite")
    else:
        verificar_permiso("crear_tramite")

    if request.method == "POST":
        nombre = request.form['nombre']
        activo = 'activo' in request.form

        if tramiteEditar:
            tramiteEditar.valor = nombre
            tramiteEditar.activo = activo
            db.session.commit()
            return redirect(url_for("dashboard.tramites"))
        else:
            stmt = select(Tramite).where(Tramite.valor==nombre)
            tramite = db.session.scalar(stmt)
            if tramite:
                flash("Ya existe un trámite con ese nombre.", "error")
            else:
                newTramite = Tramite(valor=nombre, activo=activo)
                db.session.add(newTramite)
                db.session.commit()
                return redirect(url_for("dashboard.tramites"))
    
    return render_template("editarTramite.html", tramite=tramiteEditar)


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


@dashboard_bp.route("/perfil/<username>", methods=["GET", "POST"])
@login_required
def perfil(username):
    ocultar_pass_menu = True
    

    if request.method == "POST":
        currentPassword = request.form['currentPass']
        newPassword = request.form['newPass']
        confirmPassword = request.form['confirmPass']

        if not(current_user.check_password(currentPassword)):
            flash("La contraseña actual es incorrecta", "error")
            ocultar_pass_menu = False
        elif newPassword != confirmPassword:
            flash("Las contraseñas no coinciden", "error")
            ocultar_pass_menu = False
        elif currentPassword == newPassword:
            flash("La nueva contraseña no puede ser igual a la antigua", "error")
            ocultar_pass_menu = False  
        else:
            current_user.set_password(newPassword)
            db.session.commit()
            flash("Contraseña actualizada con éxito", "success")
            return redirect(url_for("dashboard.perfil", username=username))

    return render_template("perfil.html", ocultar_pass_menu=ocultar_pass_menu)