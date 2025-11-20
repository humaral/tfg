# Autor: Hugo Martín Alonso
# Fecha: 05/11/2025
# Descripción: Funciones auxiliares para el dashboard.

import string, secrets
from app.models import Peticion, Hito, Tramite
from app import db

def temporal_password():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))


def crear_peticion(telefono, idTramite, informacion):

    newPeticion = Peticion(telefono=telefono, idTramite=idTramite, idEstadoActual=1, informacion=informacion) #Creada
    db.session.add(newPeticion)
    db.session.flush()

    hitoCreacion = Hito(idPeticion=newPeticion.id, idEstado=newPeticion.idEstadoActual)
    db.session.add(hitoCreacion)
    db.session.flush()


    newPeticion.idEstadoActual = 2 #En Curso
    db.session.flush()
    hitoEnCurso = Hito(idPeticion = newPeticion.id, idEstado = newPeticion.idEstadoActual)
    db.session.add(hitoEnCurso)
    db.session.flush()

    if idTramite == 1: #Certificado de empadronamiento
        newPeticion.idEstadoActual = 3 #Pendiente
        db.session.flush()
        newHito = Hito(idPeticion = newPeticion.id, idEstado = newPeticion.idEstadoActual)
        db.session.add(newHito)

    db.session.commit()
    
    return newPeticion.id