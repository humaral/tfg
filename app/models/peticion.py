# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con la información de una petición.

from . import db
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy import select

class Peticion(db.Model):
    __tablename__ = 'peticion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTramite = db.Column(db.Integer, db.ForeignKey('tramite.id'), nullable=False)
    idEstadoActual = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    idEmpleadoAsignado = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    informacion = db.Column(JSON, nullable=False)

    hitos = db.relationship('Hito', back_populates='peticion')
    tramite = db.relationship('Tramite', back_populates='peticiones')
    estadoActual = db.relationship('Estado', back_populates='peticiones')
    empleadoAsignado = db.relationship('Empleado', back_populates='peticionesAsignadas')

    #NOTE como un toString para logs o console
    def __repr__(self):
        return f"<Petición_{self.id}_{self.tramite.__repr__()}_Teléfono_{self.telefono}>"

    def get_fechaCreacion(self):
        hito_creacion = min(self.hitos, key=lambda h: h.updated_at)
        return hito_creacion.updated_at.strftime("%d/%m/%Y %H:%Mh")