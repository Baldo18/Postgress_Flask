-- Create puestos table
CREATE TABLE IF NOT EXISTS puestos (
    id SERIAL PRIMARY KEY,
    nombre_puesto VARCHAR(100) NOT NULL
);

-- Insert sample data for positions
INSERT INTO puestos (nombre_puesto) VALUES
    ('Gerente General'),
    ('Desarrollador Senior'),
    ('Analista de Datos'),
    ('Recursos Humanos'),
    ('Contador'),
    ('Desarrollador Junior'),
    ('Diseñador UX/UI'),
    ('Administrador de Sistemas'),
    ('Ejecutivo de Ventas'),
    ('Asistente Administrativo');


CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_p VARCHAR(100) NOT NULL,
    apellido_m VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    image VARCHAR(100),
    puesto_id INTEGER NOT NULL,
    FOREIGN KEY (puesto_id) REFERENCES puestos(id) ON DELETE CASCADE
);
