# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo con los posibles estados de una petición.

from . import db

class Estado(db.Model):
    __tablename__ = "estado"

    idEstado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.String(100), nullable=False)
    icono = db.Column(db.String(100), nullable=False)

    hitos = db.relationship('Hito', backref='estado')