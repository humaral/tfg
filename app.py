# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: programa de inicialización de la aplicación.

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.context_processor
def inject_globals():
    return {
        "current_date": datetime.now().strftime('%d/%m/%Y'),
        "current_year": datetime.now().year
    }

@app.route("/")
def inicio():
    #DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')

    #TODO: Comprobar si el usuario está autenticado, si lo esta redirigir a peticiones
    return redirect(url_for("login"))

@app.route("/login")
def login():
    if request.method == "POST":
        # Aquí iría la lógica para autenticar al usuario
        pass
    else:
        return render_template("login.html")

@app.route("/peticiones")
def peticiones():
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("peticiones.html", orden_actual=escape(orden), direccion_actual=escape(direccion))

@app.route("/peticiones/<int:peticion_id>")
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

@app.route("/empleados")
def empleados():
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("empleados.html", orden_actual=escape(orden), direccion_actual=escape(direccion))

@app.route("/empleados/new")
def new_empleado():
    return render_template("registroEmpleados.html")

@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])