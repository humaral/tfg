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
    icono TEXT NOT NULL
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
    --TODO Añadir un registro de llamadas
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
    (3,'Consulta Centros de Día',1);

insert into ESTADO values
    (1,'En Curso', 'mdi:progress-clock'),
    (2,'Revisable', 'ic:twotone-error'),
    (3,'Asignada', 'mdi:user-edit'),
    (4,'Completada', 'charm:circle-check'),
    (5,'Cancelada', 'charm:circle-cross');

insert into ROL values (1,'Administrador'), (2,'Secretario');

insert into EMPLEADO (username, password, nombre, apellido1, apellido2, email, idRol, fotoPerfil, activo) values 
    ('hugo.martin', 'scrypt:32768:8:1$Xr5bpc4tVASnGIWN$5b097b1d7e8afe9b836425049911b41419674c9d136afd612f5569214d0b7eeddfb9804f8360be826d9d5b26488c5cd5da5e1f7fc2943a9692f9ac7b90ca9963', 'Hugo', 'Martín', 'Alonso', 'admin@admin.com', 1, "hugo.martin.jpeg",1), --Cuenta ADMIN, password = 'hugo'
    ('ana.sanz', 'scrypt:32768:8:1$Eh7gm1DfhPhJxlpC$6946004565cbf141160315051bce87bae05a0fbe6b74110d4badc35bacb56aa153172b755fdc6ee43c38cbb9bf4f6d53dfaf249dc0e2ecfef483f68b14982f9f', 'Ana', 'Sanz', 'Sanz', 'ana@empleada.com', 2, "ana.sanz.jpeg", 1); --Cuenta Secretario, password = 'ana'

insert into PETICION(idTramite, telefono, idEstadoActual, idEmpleadoAsignado, informacion) values 
    (2, 654654654, 1, null, '{
            "dni": "69834521J",
            "nombre": "Fran García",
            "modalidad": "Presencial",
            "oficina": "Administración de la Aeat en el Ejido",
            "direccion": "Av Bulevar de El Ejido - 168...",
            "servicio": "IVA",
            "fecha": "2026-01-11 13:30:00"
        }'),
    (1, 612897211, 1, null, '{}'),
    (2, 983983983, 1, 1, '{}'),
    (3, 999888777, 1, 2, '{}'),
    (1, 676000000, 1, 1, '{}'),
    (3, 717717717, 1, 2, '{}'),
    (2, 777777777, 1, null, '{}'),
    (1, 622112134, 1, null, '{}'),
    (2, 654666666, 1, null, '{}'),
    (3, 917171717, 1, null, '{}'),
    (1, 623457893, 1, null, '{}'),
    (3, 758912430, 1, null, '{}'),
    (2, 600010101, 1, null, '{}'),
    (1, 623457876, 1, null, '{}'),
    (2, 623462631, 1, null, '{}'),
    (3, 927485234, 1, null, '{}'),
    (1, 724354521, 1, null, '{}'),
    (3, 632451113, 1, null, '{}'),
    (2, 609939409, 1, null, '{}'),
    (1, 909467980, 1, null, '{}'),
    (2, 948670000, 1, null, '{}'),
    (3, 623452617, 1, null, '{}'),
    (1, 623457885, 1, null, '{}'),
    (3, 777345345, 1, null, '{}'),
    (2, 600000000, 1, null, '{}');

insert into HITO(idPeticion, idEstado, updated_by) values
    (1, 1, null),
    (2, 1, null),
    (3, 1, 1),
    (4, 1, 2),
    (5, 1, 1),
    (6, 1, 2),
    (7, 1, null),
    (8, 1, null),
    (9, 1, null),
    (10, 1, null),
    (11, 1, null),
    (12, 1, null),
    (13, 1, null),
    (14, 1, null),
    (15, 1, null),
    (16, 1, null),
    (17, 1, null),
    (18, 1, null),
    (19, 1, null),
    (20, 1, null),
    (21, 1, null),
    (22, 1, null),
    (23, 1, null),
    (24, 1, null),
    (25, 1, null);