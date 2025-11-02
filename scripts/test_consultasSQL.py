import sqlite3

conexion = sqlite3.connect("./app/datos/datos.db")
cursor = conexion.cursor()

stmt2 = "SELECT * FROM Hito WHERE idEstado==1"

stmt  = "SELECT idPeticion, idEstado, MAX(updated_at) FROM HITO GROUP BY idPeticion"


cursor.execute(stmt)

for row in cursor:
    print(row)

conexion.close()