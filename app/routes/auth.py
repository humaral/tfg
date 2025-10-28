# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Controlador de las rutas en la vista del login.

from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

#Funcionalidad para mostrar el login, iniciar sesión y redirigir a peticiones
@auth_bp.route("/login", methods=["GET", "POST"])
def login(): #TODO Crear ficheros de logs para mantener registros
    if "username" in session:
        return redirect(url_for("dashboard.peticiones"))
    else:
        if request.method == "POST":
            session["username"] = request.form["username"]
            return redirect(url_for("dashboard.peticiones"))
        else:
            return render_template("login.html")

#Funcionalidad para cerrar sesión
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))