# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con los trámites que gestiona la aplicación.

from . import db

class Tramite(db.Model):
    __tablename__ = 'tramite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, server_default=db.text("1"))

    peticiones = db.relationship('Peticion', back_populates='tramite')