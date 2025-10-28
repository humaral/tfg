# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con el histórico de los cambios de estado de una petición.

from . import db

class Hito(db.Model):
    __tablename__ = 'hito'

    idHito = db.Column(db.Integer, primary_key=True, autoincrement=True)
    peticion = db.Column(db.Integer, db.ForeignKey('peticion.id'), nullable=False)
    estado = db.Column(db.Integer, db.ForeignKey('estado.idEstado'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleado'), nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    hitos = db.relationship('Hito', backref='peticion')