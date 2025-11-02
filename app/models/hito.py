# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con el histórico de los cambios de estado de una petición.

from . import db
from sqlalchemy import select

class Hito(db.Model):
    __tablename__ = 'hito'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPeticion = db.Column(db.Integer, db.ForeignKey('peticion.id'), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    peticion = db.relationship('Peticion', back_populates='hitos')
    empleadoEditor = db.relationship("Empleado", back_populates="hitosEditados")
    estado = db.relationship('Estado', back_populates='hitos')

    #NOTE como un toString para logs o console
    def __repr__(self):
        return f"<Hito_{self.id}_{self.peticion.__repr__()}_{self.estado.__repr__()}{("_"+self.empleado_editor.__repr__()+"_") if self.updated_by else '_'}Fecha_{self.updated_at}>"
    