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
	valor TEXT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT 1
);

--Enum de los posibles estados de una petición
CREATE TABLE IF NOT EXISTS ESTADO(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor TEXT NOT NULL,
    icono TEXT NOT NULL
);

--Enum de los posibles roles de un usuario
CREATE TABLE IF NOT EXISTS ROL(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor TEXT NOT NULL
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

    FOREIGN KEY (idRol) REFERENCES ROL(id)
);

--Almacena la informaciÃ³n de cada request
CREATE TABLE IF NOT EXISTS PETICION(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idTramite INTEGER NOT NULL,
    telefono INTEGER NOT NULL,
    asignada BOOLEAN NOT NULL DEFAULT 0,
    informacion JSON NOT NULL, --Formato JSON con la información recuperada por la IA  
    --TODO Añadir un registro de llamadas
    FOREIGN KEY (idTramite) REFERENCES TRAMITE(id)
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


insert into TRAMITE values(1,'Certificado de Empadronamietno',1);
insert into TRAMITE values(2,'Cita AEAT',1);
insert into TRAMITE values(3,'Consulta Centros de Día',1);

insert into ESTADO values(1,'En Curso', 'mdi:progress-clock');
insert into ESTADO values(2,'Revisable', 'ic:twotone-error');
insert into ESTADO values(3,'Asignada', 'mdi:user-edit');
insert into ESTADO values(4,'Completada', 'charm:circle-check');
insert into ESTADO values(5,'Cancelada', 'charm:circle-cross');

insert into ROL values(1,'Administrador');
insert into ROL values(2,'Secretario');

insert into EMPLEADO (username, password, nombre, apellido1, apellido2, email, idRol, fotoPerfil) values ('hugo', 'scrypt:32768:8:1$Xr5bpc4tVASnGIWN$5b097b1d7e8afe9b836425049911b41419674c9d136afd612f5569214d0b7eeddfb9804f8360be826d9d5b26488c5cd5da5e1f7fc2943a9692f9ac7b90ca9963', 'Hugo', 'Martín', 'Alonso', 'admin@admin.com', 1, "test2.jpeg"); --Cuenta ADMIN, password = 'hugo'
insert into EMPLEADO (username, password, nombre, apellido1, apellido2, email, idRol, fotoPerfil) values ('ana', 'scrypt:32768:8:1$Eh7gm1DfhPhJxlpC$6946004565cbf141160315051bce87bae05a0fbe6b74110d4badc35bacb56aa153172b755fdc6ee43c38cbb9bf4f6d53dfaf249dc0e2ecfef483f68b14982f9f', 'Ana', 'Sanz', 'Sanz', 'ana@empleada.com', 2, "test1.jpg"); --Cuenta Secretario, password = 'ana'