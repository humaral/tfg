import sqlite3

conexion = sqlite3.connect("./app/datos/datos.db")
cursor = conexion.cursor()

stmt2 = "SELECT * FROM Hito WHERE idEstado==1"


subq = "SELECT * FROM EMPLEADO e WHERE e.nombre LIKE '%h%' or e.apellido1 LIKE '%h%' or e.username LIKE '%h%'"

stmt  = f"SELECT * FROM PETICION p JOIN ({subq}) e  ON p.idEmpleadoAsignado==e.id "


cursor.execute(stmt)

for row in cursor:
    print(row)

conexion.close()