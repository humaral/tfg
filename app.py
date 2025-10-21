# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: programa de inicialización de la aplicación.

from flask import Flask, render_template, request, url_for, redirect
import os
from datetime import datetime

APP_VERSION = "0.1"

app = Flask(__name__)

@app.context_processor
def inject_globals():
    return {
        "current_date": datetime.now().strftime('%d/%m/%Y'),
        "current_year": datetime.now().year,
        "version": APP_VERSION
    }

@app.route("/")
def inicio(name=None):
    #DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    return redirect(url_for("login"))

@app.route("/login")
def login(name=None):

    return render_template("login.html", person=name)

@app.route("/peticiones")
def peticiones(name=None):
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("peticiones.html", orden_actual=orden, direccion_actual=direccion)

@app.route("/peticiones/<int:peticion_id>")
def sumary_peticion(peticion_id):
    peticion = {
        'id': peticion_id,
        'telefono': 983983983,
        'tramite': 'Cita AEAT',
        'estado': 'Revisable',
        'fecha': '2025-05-03T15:41:00',
        'informacion': {
            "dni": "69834521J",
            "nombre": "Fran García",
            "modalidad": "Presencial",
            "oficina": "Administración de la Aeat en el Ejido",
            "direccion": "Av Bulevar de El Ejido, 168...",
            "servicio": "IVA",
            "fecha": "2026-01-11T13:30:00"
        }
    }

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

@app.route("/empleados")
def empleados(name=None):
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("empleados.html", orden_actual=orden, direccion_actual=direccion)

@app.route("/empleados/new")
def new_empleado(name=None):
    return render_template("registroEmpleados.html")

@app.route("/estadisticas")
def estadisticas(name=None):
    return render_template("estadisticas.html")

if __name__ == "__main__":
    app.run(debug=True)