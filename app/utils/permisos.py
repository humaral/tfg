# Autor: Hugo Martín Alonso
# Fecha: 30/10/2025
# Descripción: Craga la información de los permisos por roles.

import os, json
from flask import session, abort
from functools import wraps
from flask_login import current_user

#Devuelve la lista de permisos del usuario. Rol = current_user.rol.valor
def cargar_permisos(rol):
    ruta = os.path.join(os.path.dirname(__file__), "permisos.json")
    with open(ruta, "r", encoding="utf-8") as f:
        session["permisos"] = json.load(f)[rol]


#Comprueba si un usuario tiene el permisos necesario con un decorador
def permiso_requerido(permiso):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            else:
                if permiso not in session.get("permisos", []):
                    abort(403)
                return f(*args, **kwargs)
        return decorated_function
    return decorator

#Comprueba si un usuario tiene el permisos necesario
def verificar_permiso(permiso):
    if not current_user.is_authenticated:
        abort(401)
    else:
        if permiso not in session.get("permisos", []):
            abort(403)
    return