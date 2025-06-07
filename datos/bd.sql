CREATE TABLE IF NOT EXISTS TRAMITE(
	idTramite INT PRIMARY KEY,
	valor VARCHAR(50) NOT NULL,
);
	
CREATE TABLE IF NOT EXISTS ESTADOPETICION(
    idEstado INT PRIMARY KEY,
    valor VARCHAR(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS EMPLEADO(
    username VARCHAR(10) PRIMARY KEY,
    password VARCHAR(64) NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    fechaNacimiento DATE NOT NULL,
    email VARCHAR(320) NOT NULL,
);

/*CHECK(fechaPresentacion < DATE('2023-11-30'))*/

CREATE TABLE IF NOT EXISTS PETICION (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo INT FOREIGN KEY REFERENCES TRAMITE(idTramite),
    telefono INT,
    informacion JSON,
    estado INT FOREIGN KEY REFERENCES ESTADOPETICION(idEstado),
    comentario TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(60) FOREIGN KEY REFERENCES EMPLEADO(username),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
);

insert into TRAMITE values(1,'Certificado de Empadronamietno');
insert into TRAMITE values(2,'Cita AEAT');
insert into TRAMITE values(3,'Consulta Centros de Día');

insert into ESTADOPETICION values(1,'En Curso');
insert into ESTADOPETICION values(2,'Revisable');
insert into ESTADOPETICION values(3,'Asignada');
insert into ESTADOPETICION values(4,'Completada');
insert into ESTADOPETICION values(5,'Cancelada');