#Script para realizar consultas a la base de datos

import sqlite3




def existUser(username, password):
    conexion = sqlite3.connect("/datos/datos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM EMPLEADOS WHERE username=? AND password=?;", (username, password))
    if cursor.rowcount == 0:
        respuesta = False
    else:
        respuesta = True

    conexion.close()
    return respuesta


