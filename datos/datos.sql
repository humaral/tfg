DROP TABLE IF EXISTS HITOPETICION;
DROP TABLE IF EXISTS PETICION;
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS ESTADOPETICION;
DROP TABLE IF EXISTS TRAMITE;

CREATE TABLE TRAMITE(
	idTramite INTEGER PRIMARY KEY,
	valor TEXT NOT NULL,
    activo BOOLEAN DEFAULT 1
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
    email TEXT UNIQUE NOT NULL,
    rol BOOLEAN DEFAULT 0, --0: Secretario, 1: Administrador
    fotoPerfil TEXT DEFAULT '/static/img/perfil/default.jpg' --Ruta de la foto de perfil
);


CREATE TABLE IF NOT EXISTS PETICION(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tramite INTEGER NOT NULL,
    telefono INTEGER NOT NULL,
    informacion TEXT NOT NULL, --Formato JSON
    estado INTEGER,
    comentario TEXT,    

    FOREIGN KEY (tramite) REFERENCES TRAMITE(idTramite),
    FOREIGN KEY (estado) REFERENCES ESTADOPETICION(idEstado)
);


CREATE TABLE IF NOT EXISTS HITOPETICION(
    idHito INTEGER PRIMARY KEY AUTOINCREMENT,
    peticion INTEGER NOT NULL,
    estado INTEGER NOT NULL,
    updated_by INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, --Timestamp

    FOREIGN KEY (peticion) REFERENCES PETICION(id),
    FOREIGN KEY (estado) REFERENCES ESTADOPETICION(idEstado),
    FOREIGN KEY (updated_by) REFERENCES EMPLEADO(idEmpleado)
);

insert into TRAMITE values(1,'Certificado de Empadronamietno',1);
insert into TRAMITE values(2,'Cita AEAT',1);
insert into TRAMITE values(3,'Consulta Centros de Día',1);

insert into ESTADOPETICION values(1,'En Curso');
insert into ESTADOPETICION values(2,'Revisable');
insert into ESTADOPETICION values(3,'Asignada');
insert into ESTADOPETICION values(4,'Completada');
insert into ESTADOPETICION values(5,'Cancelada');

insert into EMPLEADO (username, password, nombre, email, rol) values ('hugo', '0478721f1106c2a631a90181bac7efc77767a3903eb9220687bff8a14e940fa7', 'Hugo Martín Alonso', 'admin@admin.com', 1);