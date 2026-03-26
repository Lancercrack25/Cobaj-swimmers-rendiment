import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion,DB_CONFIG

def crear_tablas_si_no_existen():
    conn = obtener_conexion()
    if not conn:
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS entrenadores (
                id SERIAL PRIMARY KEY,
                nombre TEXT NOT NULL,
                edad INT NOT NULL,
                experiencia_anios INT NOT NULL,
                especialidad TEXT NOT NULL,
                password TEXT NOT NULL,
                activo BOOLEAN DEFAULT TRUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS nadadores (
                id SERIAL PRIMARY KEY,
                nombre TEXT NOT NULL,
                edad INT NOT NULL,
                codigo_acceso TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'activo',
                genero TEXT NOT NULL,
                peso REAL NOT NULL,
                estatura REAL NOT NULL,
                problema_respiratorio BOOLEAN DEFAULT FALSE,
                entrenador_id INTEGER NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                CONSTRAINT fk_entrenador
                    FOREIGN KEY (entrenador_id)
                    REFERENCES entrenadores(id)
                    ON DELETE CASCADE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sesiones_entrenamiento (
                id SERIAL PRIMARY KEY,
                entrenador_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT,
                CONSTRAINT fk_sesion_entrenador
                    FOREIGN KEY (entrenador_id)
                    REFERENCES entrenadores(id)
                    ON DELETE CASCADE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS rendimiento_nadador (
                id SERIAL PRIMARY KEY,
                nadador_id INTEGER NOT NULL,
                sesion_id INTEGER NOT NULL,
                distancia_m REAL NOT NULL,
                tiempo_seg REAL NOT NULL,
                ritmo REAL NOT NULL,
                fecha DATE NOT NULL,
                CONSTRAINT fk_nadador
                    FOREIGN KEY (nadador_id)
                    REFERENCES nadadores(id)
                    ON DELETE CASCADE,
                CONSTRAINT fk_sesion
                    FOREIGN KEY (sesion_id)
                    REFERENCES sesiones_entrenamiento(id)
                    ON DELETE CASCADE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS lesiones (
                id SERIAL PRIMARY KEY,
                nadador_id INTEGER NOT NULL,
                tipo_lesion TEXT NOT NULL,
                gravedad TEXT NOT NULL,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE,
                activo BOOLEAN DEFAULT TRUE,
                observaciones TEXT,
                CONSTRAINT fk_lesion_nadador
                    FOREIGN KEY (nadador_id)
                    REFERENCES nadadores(id)
                    ON DELETE CASCADE
            );
        """)

        conn.commit()
        print("✔ Tablas creadas/verificadas correctamente")

    except Exception as e:
        print("❌ Error creando tablas:", e)
    finally:
        conn.close()