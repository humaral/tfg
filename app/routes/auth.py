# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Controlador de las rutas relacionadas con la autentificación.

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select, or_
from app.models import Empleado
from app.utils import cargar_permisos
from app import db

auth_bp = Blueprint('auth', __name__)

#Funcionalidad para mostrar el login, iniciar sesión y redirigir a peticiones
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.peticiones"))
    else:
        if request.method == "POST":
            
            username = request.form['username']
            password = request.form['password']

            stmt = select(Empleado).where(or_(Empleado.username==username, Empleado.email==username))
            empleado = db.session.scalar(stmt)

            if not(empleado and empleado.check_password(password)):
                flash("Usuario y/o contraseña incorrectos", "error")
            elif not(empleado.activo):
                flash("Cuenta desactivada, póngase en contacto con un Administrador", "error")
            else:
                login_user(empleado)
                cargar_permisos(empleado.rol.valor)
                return redirect(url_for("dashboard.peticiones"))

        return render_template("login.jinja")

#Funcionalidad para cerrar sesión
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))

