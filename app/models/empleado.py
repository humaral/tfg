# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo de la tabla de empleados.

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Empleado(db.Model, UserMixin):
    __tablename__ = "empleado"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) #Guarda el hash de la contraseña
    nombre = db.Column(db.String(100), nullable=False)
    apellido1 = db.Column(db.String(100), nullable=False)
    apellido2 = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    idRol = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    fotoPerfil = db.Column(db.String(255), nullable=False, server_default=db.text("'default.jpg'")) #Guarda la ruta de la foto de perfil

    rol = db.relationship("Rol", back_populates="empleados")
    hitos_editados = db.relationship("Hito", back_populates="empleado_editor")

    #NOTE como un toString para logs o console
    def __repr__(self):
        return f"<Empleado {self.username} --> {self.nombre} {self.apellido1} {self.apellido2 if self.apellido2 else ''} ({self.rol})>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
