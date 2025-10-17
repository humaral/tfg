#Script para crear la base de datos desde el .sql, borrando las tablas antiguas.

import sqlite3
import os

ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_bd = os.path.join(ruta_base, "datos\\datos.db")
ruta_sql = os.path.join(ruta_base, "datos\\datos.sql")


conn = sqlite3.connect(ruta_bd)

with open(ruta_sql, 'r') as f:
    sql_script = f.read()

conn.executescript(sql_script)

conn.close()