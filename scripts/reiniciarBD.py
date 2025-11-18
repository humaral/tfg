# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: script para crear la base de datos desde el .sql, borrando las tablas antiguas.

import sqlite3
import os

ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_bd = os.path.join(ruta_base, "app\\data\\data.db")
ruta_sql = os.path.join(ruta_base, "app\\data\\data.sql")


conn = sqlite3.connect(ruta_bd)

with open(ruta_sql, 'r', encoding='utf-8') as f:
    sql_script = f.read()

conn.executescript(sql_script)

conn.close()