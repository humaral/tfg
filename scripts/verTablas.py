#Script para ver las tablas de la base de datos

import sqlite3
import os


raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rutaBD = os.path.join(raiz, "datos\\datos.db")

conexion = sqlite3.connect(rutaBD)

cursor = conexion.cursor()

print("Tablas en la base de datos:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
for tablas in cursor.fetchall():
    cursor.execute(f"SELECT * FROM {tablas[0]};")
    print(f"\nContenido de {tablas[0]}:")
    for fila in cursor.fetchall():
        print(fila)


conexion.close()




