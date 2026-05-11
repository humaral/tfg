# Autor: Hugo Martín Alonso
# Fecha: 17-06-2025
# Descripción: Script para ver las tablas de la base de datos, útil para depuración y desarrollo.

import sqlite3
import os

raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rutaBD = os.path.join(raiz, "app\\data\\data.db")
print(rutaBD)
conexion = sqlite3.connect(rutaBD)
conexion.text_factory = str
cursor = conexion.cursor()

print("Tablas en la base de datos:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name!='sqlite_sequence';")
for tablas in cursor.fetchall():
    cursor.execute(f"SELECT * FROM {tablas[0]};")
    print(f"\nContenido de {tablas[0]}:")
    for fila in cursor.fetchall():
        print(fila)


conexion.close()




