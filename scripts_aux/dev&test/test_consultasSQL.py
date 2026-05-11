# Autor: Hugo Martín Alonso
# Fecha: 1-11-2025
# Descripción: Script para realizar una consulta en la base de datos, útil para depuración y desarrollo.

import sqlite3

conexion = sqlite3.connect("./app/data/data.db")
cursor = conexion.cursor()

stmt2 = "SELECT * FROM Hito WHERE idEstado==1"


subq = "SELECT * FROM EMPLEADO e WHERE e.nombre LIKE '%h%' or e.apellido1 LIKE '%h%' or e.username LIKE '%h%'"

stmt  = f"SELECT * FROM PETICION p JOIN ({subq}) e  ON p.idEmpleadoAsignado==e.id "


cursor.execute(stmt)

for row in cursor:
    print(row)

conexion.close()