#Script para crear las tablas de la base de datos (borra las antiguas si existen)

import sqlite3
import os

ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_bd = os.path.join(ruta_base, "datos.db")
ruta_sql = os.path.join(ruta_base, "datos.sql")

print(ruta_bd)

conn = sqlite3.connect(ruta_bd)

with open(ruta_sql, 'r') as f:
    sql_script = f.read()

conn.executescript(sql_script)

print(sql_script)

conn.close()