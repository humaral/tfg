--Autor: Hugo Martí­n Alonso
--Fecha: 25-09-2025
--Descripción: código fuente de la base de datos.


DROP TABLE IF EXISTS HITO;
DROP TABLE IF EXISTS PETICION;
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS ROL;
DROP TABLE IF EXISTS ESTADO;
DROP TABLE IF EXISTS TRAMITE;

--Tipos de trámites que se gestionan en la aplicación
CREATE TABLE IF NOT EXISTS TRAMITE(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	valor TEXT NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT 1
);

--Enum de los posibles estados de una petición
CREATE TABLE IF NOT EXISTS ESTADO(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor TEXT NOT NULL UNIQUE,
    icono TEXT NOT NULL,
    color TEXT NOT NULL
);

--Enum de los posibles roles de un usuario
CREATE TABLE IF NOT EXISTS ROL(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor TEXT NOT NULL UNIQUE
);

--Almacena los datos de los empleados
CREATE TABLE IF NOT EXISTS EMPLEADO(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, --Guarda el hash de la contraseña
    nombre TEXT NOT NULL,
    apellido1 TEXT NOT NULL,
    apellido2 TEXT,
    email TEXT UNIQUE NOT NULL,
    idRol INTEGER NOT NULL,
    fotoPerfil TEXT NOT NULL DEFAULT 'default.jpg', --Ruta de la foto de perfil
    activo BOOLEAN NOT NULL DEFAULT 1,
    
    FOREIGN KEY (idRol) REFERENCES ROL(id)
);

--Almacena la información de cada request
CREATE TABLE IF NOT EXISTS PETICION(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idTramite INTEGER NOT NULL,
    idEstadoActual INTEGER NOT NULL,
    idEmpleadoAsignado INTEGER,
    telefono INTEGER NOT NULL,
    informacion JSON NOT NULL, --Formato JSON con la información recuperada por la IA  
    
    FOREIGN KEY (idTramite) REFERENCES TRAMITE(id)
    FOREIGN KEY (idEstadoActual) REFERENCES ESTADO(id)
    FOREIGN KEY (idEmpleadoAsignado) REFERENCES EMPLEADO(id)
);

--Guarda los registros de cambio de estado de cada peticiÃ³n
CREATE TABLE IF NOT EXISTS HITO(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idPeticion INTEGER NOT NULL,
    idEstado INTEGER NOT NULL,
    updated_by INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (idPeticion) REFERENCES PETICION(id),
    FOREIGN KEY (idEstado) REFERENCES ESTADO(id),
    FOREIGN KEY (updated_by) REFERENCES EMPLEADO(id)
);


insert into TRAMITE values 
    (1,'Certificado de Empadronamiento',1),
    (2,'Cita AEAT',1),
    (3, 'Tarjeta Sanitaria SACYL', 1);

insert into ESTADO values
    (1,'Creada', 'qlementine-icons:new-16', '#022e59'),
    (2,'Pendiente', 'ic:twotone-error', '#cf6208ff'),
    (3,'Asignada', 'mdi:user-edit', '#00f7ffff'),
    (4,'Modificada', 'mdi:auto-fix', '#b49000ff'),
    (5,'Completada', 'charm:circle-tick', '#00af40ff'),
    (6,'Cancelada', 'charm:circle-cross', '#d80000ff');

insert into ROL values (1,'Administrador'), (2,'Secretario');

insert into EMPLEADO (username, password, nombre, apellido1, apellido2, email, idRol, fotoPerfil, activo) values 
    ('admin.admin', 'scrypt:32768:8:1$eZ0K7o9rPzItpk98$7fa1f1cef60c98cb6b7cb6c29615f7e93f3a3c0cdccee41fc034b02eb02134312a57dc861d080e26bb24fd8d00b2c3c600fa19f32ded252d881db6198c621216', 'Admin', 'Admin', '', 'admin.admin@tramitestelefonicos.es', 1, "admin.admin.jpeg",1), --Cuenta ADMIN, password = 'admin'
    ('hugo.martin', 'scrypt:32768:8:1$Xr5bpc4tVASnGIWN$5b097b1d7e8afe9b836425049911b41419674c9d136afd612f5569214d0b7eeddfb9804f8360be826d9d5b26488c5cd5da5e1f7fc2943a9692f9ac7b90ca9963', 'Hugo', 'Martín', 'Alonso', 'hugo.martin@tramitestelefonicos.es', 2, "hugo.martin.jpeg", 1); --Cuenta Secretario, password = 'hugo'