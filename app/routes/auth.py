# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Controlador de las rutas relacionadas con la autentificación.

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Empleado
from app.utils import cargar_permisos

auth_bp = Blueprint('auth', __name__)

#Funcionalidad para mostrar el login, iniciar sesión y redirigir a peticiones
@auth_bp.route("/login", methods=["GET", "POST"])
def login(): #TODO Crear ficheros de logs para mantener registros
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.peticiones"))
    else:
        if request.method == "POST":
            
            username = request.form['username']
            password = request.form['password']

            empleado = Empleado.query.filter_by(username=username).first()

            if empleado and empleado.check_password(password):
                login_user(empleado)
                cargar_permisos(empleado.rol.valor)
                flash("Sesión iniciada correctamente", "success")
                return redirect(url_for("dashboard.peticiones"))
            else:
                flash("Usuario y/o contraseña incorrectos", "error")

        return render_template("login.html")

#Funcionalidad para cerrar sesión
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))

