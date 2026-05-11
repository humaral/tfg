# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: Script para crear la base de datos desde el .sql, borrando las tablas antiguas.

import os, random
from app import db
from app.utils import crear_peticion
from datetime import date

def reiniciar_bd(app):

    ruta_base = app.config['DB_PATH']
    ruta_sql = os.path.join(ruta_base, "data.sql")

    with app.app_context():

        with open(ruta_sql, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()

        poblar_peticiones()


def poblar_peticiones():

    crear_peticion("627899040", 1, {"nombre":"Manuel", "apellidos":"Pérez", "dni":"12312345A", "telefono":"627899040", "motivo":"Para realizar otros trámites."}),
    crear_peticion("722643980", 2, {"dni" : "75849123L", "nombre" : "Juan González Aparicio", "servicio" : "IVA", "modalidad" : "presencial", "oficina" : "Delegación Especial de Castilla y León", "dia" : str(date(2026, 2, 12)), "hora" : "10:30"}),
    crear_peticion("834521234", 2, {"dni" : "12507943Z", "nombre" : "Sara Alonso García", "servicio" : "Certificados tributarios", "modalidad" : "telefonica"}),
    crear_peticion("952439538", 3, {"nombre":"Ana", "apellido1":"Gómez", "nacimiento":str(date(1950, 12, 21)), "motivo":"perdida", "centro_salud":"Barrio España", "localidad":"VALLADOLID", "calle":"Ejemplo de calle", "numero":"34", "piso":"2", "puerta":"B"})
    
    for i in range(26):   
        tel=random.randint(600000000, 999999999)
        
        opciones = [
            lambda: crear_peticion(str(tel), 1, {"nombre":"Manuel", "apellidos":"Pérez", "dni":"12312345A", "telefono":str(tel), "motivo":"Para realizar otros trámites."}),
            lambda: crear_peticion(str(tel), 2, {"dni" : "75849123L", "nombre" : "Juan González Aparicio", "servicio" : "IVA", "modalidad" : "presencial", "oficina" : "Delegación Especial de Castilla y León", "dia" : str(date(2026, 2, 12)), "hora" : "10:30"}),
            lambda: crear_peticion(str(tel), 2, {"dni" : "12507943Z", "nombre" : "Sara Alonso García", "servicio" : "Certificados tributarios", "modalidad" : "telefonica"}),
            lambda: crear_peticion(str(tel), 3, {"nombre":"Ana", "apellido1":"Gómez", "nacimiento":str(date(1950, 12, 21)), "motivo":"perdida", "centro_salud":"Barrio España", "localidad":"VALLADOLID", "calle":"Ejemplo de calle", "numero":"34", "piso":"2", "puerta":"B"})
        ]

        random.choice(opciones)()