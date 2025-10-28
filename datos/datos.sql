--Autor: Hugo Martín Alonso
--Fecha: 25-09-2025
--Descripción: código fuente de la base de datos.

--FIX Arreglar la lectura de caracteres especiales, tildes y demás

DROP TABLE IF EXISTS HITO;
DROP TABLE IF EXISTS PETICION;
DROP TABLE IF EXISTS EMPLEADO;
DROP TABLE IF EXISTS ESTADO;
DROP TABLE IF EXISTS TRAMITE;

--Tipos de trámites que se gestionan en la aplicación
CREATE TABLE IF NOT EXISTS TRAMITE(
	idTramite INTEGER PRIMARY KEY AUTOINCREMENT,
	valor TEXT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT 1
);

--Enum de los posibles estados de una petición
CREATE TABLE IF NOT EXISTS ESTADO(
    idEstado INTEGER PRIMARY KEY AUTOINCREMENT,
    valor TEXT NOT NULL,
    icono TEXT NOT NULL
);

--Almacena los datos de los empleados
CREATE TABLE IF NOT EXISTS EMPLEADO(
    idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, --Guarda el hash de la contraseña
    nombre TEXT NOT NULL,
    apellido1 TEXT NOT NULL,
    apellido2 TEXT,
    email TEXT UNIQUE NOT NULL,
    rol BOOLEAN NOT NULL DEFAULT 0, --0: Secretario, 1: Administrador
    fotoPerfil TEXT NOT NULL DEFAULT 'default.jpg' --Ruta de la foto de perfil
);

--Almacena la información de cada request
CREATE TABLE IF NOT EXISTS PETICION(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tramite INTEGER NOT NULL,
    telefono INTEGER NOT NULL,
    asignado_a INTEGER,
    informacion JSON NOT NULL, --Formato JSON con la información recuperada por la IA  
    --TODO Añadir un registro de llamadas
    FOREIGN KEY (tramite) REFERENCES TRAMITE(idTramite),
    FOREIGN KEY (asignado_a) REFERENCES EMPLEADO(idEmpleado)
);

--Guarda los registros de cambio de estado de cada petición
CREATE TABLE IF NOT EXISTS HITO(
    idHito INTEGER PRIMARY KEY AUTOINCREMENT,
    peticion INTEGER NOT NULL,
    estado INTEGER NOT NULL,
    updated_by INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (peticion) REFERENCES PETICION(id),
    FOREIGN KEY (estado) REFERENCES ESTADO(idEstado),
    FOREIGN KEY (updated_by) REFERENCES EMPLEADO(idEmpleado)
);


insert into TRAMITE values(1,'Certificado de Empadronamietno',1);
insert into TRAMITE values(2,'Cita AEAT',1);
insert into TRAMITE values(3,'Consulta Centros de Día',1);

insert into ESTADO values(1,'En Curso', 'mdi:progress-clock');
insert into ESTADO values(2,'Revisable', 'ic:twotone-error');
insert into ESTADO values(3,'Asignada', 'mdi:user-edit');
insert into ESTADO values(4,'Completada', 'charm:circle-check');
insert into ESTADO values(5,'Cancelada', 'charm:circle-cross');

insert into EMPLEADO (username, password, nombre, apellido1, apellido2, email, rol) values ('hugo', '0478721f1106c2a631a90181bac7efc77767a3903eb9220687bff8a14e940fa7', 'Hugo', 'Martín', 'Alonso', 'admin@admin.com', 1);