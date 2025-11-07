# Autor: Hugo Martín Alonso
# Fecha: 29/10/2025
# Descripción: Modelo de la tabla del rol.

from app import db

class Rol(db.Model):
    __tablename__ = "rol"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.String(100), unique=True, nullable=False)

    empleados = db.relationship("Empleado", back_populates="rol")

    def __repr__(self):
        return f"<Rol_{self.valor}>"
    