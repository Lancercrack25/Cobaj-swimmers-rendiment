import os
from Backend.conection_database import obtener_conexion, DB_CONFIG

def crear_tablas_si_no_existen():
    conn = obtener_conexion()
    if not conn:
        return
    try:
        cur = conn.cursor()
        # -------------------- ENTRENADORES --------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS entrenadores (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INT CHECK (edad > 0),
            experiencia_anios INT CHECK (experiencia_anios > 0),
            especialidad TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            activo BOOLEAN DEFAULT TRUE
        );
        """)

        # -------------------- NADADORES --------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS nadadores (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INT CHECK (edad > 0),
            codigo_acceso TEXT UNIQUE NOT NULL,
            genero TEXT CHECK (genero IN ('M','F','Otro')),
            peso NUMERIC(5,2) CHECK (peso > 0),
            estatura NUMERIC(4,2) CHECK (estatura > 0),
            password TEXT NOT NULL,
            problema_respiratorio BOOLEAN DEFAULT FALSE,
            entrenador_id INTEGER DEFAULT NULL,
            activo BOOLEAN DEFAULT TRUE,
            CONSTRAINT fk_entrenador
                FOREIGN KEY (entrenador_id)
                REFERENCES entrenadores(id)
                ON DELETE CASCADE
        );
        """)

        # -------------------- SESIONES --------------------
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

        # -------------------- RENDIMIENTO --------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rendimiento_nadador (
            id SERIAL PRIMARY KEY,
            nadador_id INTEGER NOT NULL,
            sesion_id INTEGER NOT NULL,
            distancia_m NUMERIC(6,2) CHECK (distancia_m > 0),
            tiempo_seg NUMERIC(8,2) CHECK (tiempo_seg > 0),
            ritmo NUMERIC(8,4),
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

        # -------------------- LESIONES --------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS lesiones (
            id SERIAL PRIMARY KEY,
            nadador_id INTEGER NOT NULL,
            tipo_lesion TEXT NOT NULL,
            gravedad TEXT CHECK (gravedad IN ('leve','media','grave')),
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

        # -------------------- REHABILITACIONES --------------------
        cur.execute("""
        CREATE TABLE IF NOT EXISTS rehabilitaciones (
            id SERIAL PRIMARY KEY,
            lesion_id INTEGER NOT NULL,
            nadador_id INTEGER NOT NULL,
            tipo_terapia TEXT NOT NULL,
            tiempo_estimado_dias INTEGER CHECK (tiempo_estimado_dias > 0),
            especificaciones_entrenador TEXT,
            fecha_inicio DATE DEFAULT CURRENT_DATE,
            fecha_fin DATE,
            CONSTRAINT fk_rehab_lesion
                FOREIGN KEY (lesion_id)
                REFERENCES lesiones(id)
                ON DELETE CASCADE,
            CONSTRAINT fk_rehab_nadador
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
if __name__ == "__main__":
    crear_tablas_si_no_existen()