DROP TABLE IF EXISTS PETICION;
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS ESTADOPETICION;
DROP TABLE IF EXISTS TRAMITE;


CREATE TABLE TRAMITE(
	idTramite INTEGER PRIMARY KEY,
	valor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ESTADOPETICION(
    idEstado INTEGER PRIMARY KEY,
    valor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS EMPLEADO(
    idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, --Guarda el hash de la contraseña
    nombre TEXT NOT NULL,
    fechaNacimiento TEXT NOT NULL, --Formato "DD/MM/AAAA"
    email TEXT UNIQUE NOT NULL,
    fotoPerfil TEXT DEFAULT '/static/img/perfil/default.jpg' --Ruta de la foto de perfil
);


CREATE TABLE IF NOT EXISTS PETICION (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo INTEGER NOT NULL,
    telefono INTEGER NOT NULL,
    informacion TEXT NOT NULL, --Formato JSON
    estado INTEGER,
    comentario TEXT,
    created_at INT NOT NULL, --Timestamp
    updated_by TEXT,
    updated_at INT, --Timestamp

    FOREIGN KEY (tipo) REFERENCES TRAMITE(idTramite),
    FOREIGN KEY (estado) REFERENCES ESTADOPETICION(idEstado),
    FOREIGN KEY (updated_by) REFERENCES EMPLEADO(username)
);

insert into TRAMITE values(1,'Certificado de Empadronamietno');
insert into TRAMITE values(2,'Cita AEAT');
insert into TRAMITE values(3,'Consulta Centros de Día');

insert into ESTADOPETICION values(1,'En Curso');
insert into ESTADOPETICION values(2,'Revisable');
insert into ESTADOPETICION values(3,'Asignada');
insert into ESTADOPETICION values(4,'Completada');
insert into ESTADOPETICION values(5,'Cancelada');
