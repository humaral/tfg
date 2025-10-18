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

@app.route("/empleados")
def empleados(name=None):
    orden = request.args.get('orden', 'id')
    direccion = request.args.get('direccion', 'ascendente')
    return render_template("empleados.html", orden_actual=orden, direccion_actual=direccion)

@app.route("/estadisticas")
def estadisticas(name=None):
    return render_template("estadisticas.html")

if __name__ == "__main__":
    app.run(debug=True)