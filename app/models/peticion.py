# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con la información de una petición.

from . import db
from sqlalchemy.dialects.sqlite import JSON

class Peticion(db.Model):
    __tablename__ = 'peticion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTramite = db.Column(db.Integer, db.ForeignKey('tramite.id'), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    asignado_a = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    informacion = db.Column(JSON, nullable=False)

    hitos = db.relationship('Hito', back_populates='peticion')
    tramite = db.relationship('Tramite', back_populates='peticiones')
    empleado_asignado = db.relationship("Empleado", back_populates="peticiones_asignadas")