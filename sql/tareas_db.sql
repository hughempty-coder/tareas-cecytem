-- =====================================================================
--  TareasCECyTEM  ·  Script de creación de la base de datos
--  Se ejecuta en phpMyAdmin de XAMPP (pestaña SQL), dentro de tareas_db
--  IMPORTANTE: todas las tablas tienen PRIMARY KEY porque Aiven
--  (sql_require_primary_key = ON) rechaza tablas sin llave primaria.
-- =====================================================================

-- Asegura que los acentos y la ñ se guarden correctamente
SET NAMES utf8mb4;

-- Tabla 1: categorías de tareas
CREATE TABLE IF NOT EXISTS categorias (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    nombre  VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla 2: tareas
CREATE TABLE IF NOT EXISTS tareas (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    titulo        VARCHAR(120) NOT NULL,
    descripcion   TEXT,
    categoria_id  INT NOT NULL,
    prioridad     ENUM('Baja','Media','Alta') NOT NULL DEFAULT 'Media',
    fecha_limite  DATE NULL,
    completada    TINYINT(1) NOT NULL DEFAULT 0,
    creada_en     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tareas_categoria
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos iniciales
INSERT INTO categorias (nombre) VALUES
    ('Escuela'), ('Casa'), ('Proyecto'), ('Personal');

INSERT INTO tareas (titulo, descripcion, categoria_id, prioridad, fecha_limite) VALUES
    ('Entregar práctica de BD', 'Subir evidencias a la plataforma', 1, 'Alta',  '2026-11-06'),
    ('Repasar consultas JOIN',   'Ejercicios del cuaderno',         1, 'Media', '2026-11-10'),
    ('Configurar Render',        'Variables de entorno de Aiven',   3, 'Alta',  NULL);
