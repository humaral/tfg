# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con el histórico de los cambios de estado de una petición.

from . import db

class Hito(db.Model):
    __tablename__ = 'hito'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPeticion = db.Column(db.Integer, db.ForeignKey('peticion.id'), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    peticion = db.relationship('Peticion', back_populates='hitos')
    empleado_editor = db.relationship("Empleado", back_populates="hitos_editados")
    estado = db.relationship('Estado', back_populates='hitos')