# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: script para crear la base de datos desde el .sql, borrando las tablas antiguas.

import os, random
from app import db
from app.utils import crear_peticion

def reiniciar_bd(app):

    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_sql = os.path.join(ruta_base, "data\\data.sql")

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
    for i in range(25):   
        tel=random.randint(600000000, 999999999)
        crear_peticion(tel, 1, {"nombre":"Juan", "apellidos":"Perez", "dni":"12312345A", "telefono":tel})