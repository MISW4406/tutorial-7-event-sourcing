CREATE TABLE usuarios_legado(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Llave primaria',
    nombres VARCHAR(255),
    apellidos VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)

) COMMENT 'Tabla legado de los usuarios';