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
    
    tramite = db.session.scalar(db.select(Tramite).where(Tramite.id == idTramite))
    
    if not tramite or not tramite.activo:
        newPeticion = Peticion(telefono=telefono, idTramite=idTramite, idEstadoActual=5, informacion=informacion) #Cancelada
        db.session.add(newPeticion)
        db.session.flush()
        hitoCancelacion = Hito(idPeticion=newPeticion.id, idEstado=newPeticion.idEstadoActual)
        db.session.add(hitoCancelacion)
        db.session.commit()

    else:
        newPeticion = Peticion(telefono=telefono, idTramite=idTramite, idEstadoActual=1, informacion=informacion) #Creada
        db.session.add(newPeticion)
        db.session.flush()
        hitoCreacion = Hito(idPeticion=newPeticion.id, idEstado=newPeticion.idEstadoActual)
        db.session.add(hitoCreacion)
        db.session.flush()

        if idTramite == 1: #Certificado de empadronamiento
            newPeticion.idEstadoActual = 2 #Pendiente
            db.session.flush()
            hitoPendiente = Hito(idPeticion = newPeticion.id, idEstado = newPeticion.idEstadoActual)
            db.session.add(hitoPendiente)

        db.session.commit()
    
    return newPeticion.id