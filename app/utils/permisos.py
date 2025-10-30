# Autor: Hugo Martín Alonso
# Fecha: 30/10/2025
# Descripción: Craga la información de los permisos por roles.

import os, json
from flask import session

#Devuelve la lista de permisos del usuario. Rol = current_user.rol.valor
def cargar_permisos(rol):
    ruta = os.path.join(os.path.dirname(__file__), "permisos.json")
    with open(ruta, "r", encoding="utf-8") as f:
        session["permisos"] = json.load(f)[rol]