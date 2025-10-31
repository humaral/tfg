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
    telefono = db.Column(db.Integer, nullable=False)
    informacion = db.Column(JSON, nullable=False)

    hitos = db.relationship('Hito', back_populates='peticion')
    tramite = db.relationship('Tramite', back_populates='peticiones')

    #NOTE como un toString para logs o console
    def __repr__(self):
        return f"<Petición_{self.id}_{self.tramite.__repr__()}_Teléfono_{self.telefono}>"
    

    def estado_actual(self):
        hito_actual = max(self.hitos, key=lambda h: h.updated_at)
        return hito_actual.estado.valor
    
    def is_Asignada(self):
        hito_actual = max(self.hitos, key=lambda h: h.updated_at)
        if hito_actual.updated_by is None:
            return False
        else:
            return True
        
    def fecha_Creacion(self):
        hito_creacion = min(self.hitos, key=lambda h: h.updated_at)
        return hito_creacion.updated_at

    #FIX
    def filtrar(self, telefono, estado, tramite, orden, direccion):
        stmt = select(self).where(self.telefono==telefono, self.estado_actual()==estado, self.tramite.valor==tramite).filter_by(self.orden.desc() if direccion=="Descendente" else self.orden.asc())
        db.session.scalars(stmt).limit(10)