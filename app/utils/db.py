# Autor: Hugo Martín Alonso
# Fecha: 25-09-2025
# Descripción: Controla la conexión con la base de datos.
#DELETE ARCHIVO
import sqlite3
from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('datos/datos.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

#DELETE: esta funcion no es necesario
def init_db():
    db = get_db()
    with open('datos/datos.sql') as f:
        db.executescript(f.read())


