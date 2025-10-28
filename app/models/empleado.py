# Autor: Hugo Martín Alonso
# Fecha: 17-10-2025
# Descripción: Modelo de la tabla de empleados.

from app import db

class Empleado(db.Model):
    __tablename__ = "empleado"

    idEmpleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) #Guarda el hash de la contraseña
    nombre = db.Column(db.String(100), nullable=False)
    apellido1 = db.Column(db.String(100), nullable=False)
    apellido2 = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    rol = db.Column(db.Boolean, nullable=False, server_default=db.text("0")) # False = Secretario, True = Administrador
    fotoPerfil = db.Column(db.String(255), nullable=False, server_default=db.text("'default.jpg'")) #Guarda la ruta de la foto de perfil

    peticiones_asignadas = db.relationship("Peticion", backref="empleado_asignado")
    hitos_editados = db.relationship("Hito", backref="empleado_editor")

    #NOTE como un toString para logs o console
    # def __repr__(self):
    #     return f"<Empleado {self.username}"