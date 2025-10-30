# Autor: Hugo Martín Alonso
# Fecha: 27-10-2025
# Descripción: Controlador de las rutas en la vista del dashboard.

from flask import Blueprint, render_template, request, session, abort
from flask_login import login_required
from markupsafe import escape
from datetime import datetime
from app.utils import permiso_requerido


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/peticiones")
@login_required
@permiso_requerido("ver_peticiones")
def peticiones():
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("peticiones.html", orden_actual=escape(orden), direccion_actual=escape(direccion))

@dashboard_bp.route("/peticiones/<int:peticion_id>")
@login_required
@permiso_requerido("ver_peticiones")
def sumary_peticion(peticion_id):
    #TODO: Obtener los datos de la petición desde la base de datos, utilizar escape si es necesario
    peticion = {
        'id': peticion_id,
        'telefono': 983983983,
        'tramite': 'Cita AEAT',
        'informacion': {
            "dni": "69834521J",
            "nombre": "Fran García",
            "modalidad": "Presencial",
            "oficina": "Administración de la Aeat en el Ejido",
            "direccion": "Av Bulevar de El Ejido, 168...",
            "servicio": "IVA",
            "fecha": datetime(2026,1,11,13,30),
        }
    }
    #TODO: Obtener el historial de la petición desde la base de datos
    historial = [
        {
            'fecha': datetime(2025,5,3,15,41),
            'estado': 'Creada',
            'icono': 'mdi:plus-box',
            'empleado': None
        },
        {
            'fecha': datetime(2025,5,5,9,30),
            'estado': 'Revisable',
            'icono': 'mdi:eye-check',
            'empleado': None
        },
        {
            'fecha': datetime(2025,5,6,16,15),
            'estado': 'Asignada',
            'icono': 'mdi:check-circle-outline',
            'empleado': {
                'nombre': 'Laura',
                'apellido1': 'Martínez',
                'apellido2': 'López',
                'rol': 'Secretario',
                'fotoPerfil': '/static/img/perfil/default.jpg'

            }
        },
        {
            'fecha': datetime(2025,5,6,16,22),
            'estado': 'Cancelada',
            'icono': 'mdi:cross-circle-outline',
            'empleado': {
                'nombre': 'Laura',
                'apellido1': 'Martínez',
                'apellido2': 'López',
                'rol': 'Secretario',
                'fotoPerfil': '/static/img/perfil/default.jpg'

            }
        }
    ]
    
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

