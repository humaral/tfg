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

def init_db():
    db = get_db()
    with open('datos/datos.sql') as f:
        db.executescript(f.read())


def print_tablas():
    db = get_db()
    cursor = db.cursor()

    print("Tablas en la base de datos:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
    for tablas in cursor.fetchall():
        cursor.execute(f"SELECT * FROM {tablas[0]};")
        print(f"\nContenido de {tablas[0]}:")
        for fila in cursor.fetchall():
            print(fila)

