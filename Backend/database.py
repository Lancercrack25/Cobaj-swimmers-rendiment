import psycopg2
import os

# Configuración centralizada (OJO: Cambiamos el dbname a natacion_db)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "admin"), # CONTRASENA
    "dbname": os.getenv("DB_NAME", "natacion_db"), 
}

def obtener_conexion():
    """Crea y retorna una conexión a la base de datos."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error de conexión: {e}")
        return None

def crear_tablas():
    """Genera la estructura relacional de la base de datos desde cero."""
    conn = obtener_conexion()
    if not conn: return
    
    tablas_sql = """
    -- 1. Tabla principal
    CREATE TABLE IF NOT EXISTS nadadores (
        id_nadador SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        rama VARCHAR(20),
        fecha_nacimiento DATE
    );

    -- 2. Entrenamientos (El reemplazo de las 'rachas')
    CREATE TABLE IF NOT EXISTS entrenamientos (
        id_entrenamiento SERIAL PRIMARY KEY,
        id_nadador INTEGER REFERENCES nadadores(id_nadador) ON DELETE CASCADE,
        fecha DATE DEFAULT CURRENT_DATE,
        tipo_piscina VARCHAR(20) -- 25m o 50m
    );

    -- 3. Pruebas de nado (Aquí van los tiempos)
    CREATE TABLE IF NOT EXISTS pruebas_nado (
        id_prueba SERIAL PRIMARY KEY,
        id_entrenamiento INTEGER REFERENCES entrenamientos(id_entrenamiento) ON DELETE CASCADE,
        estilo VARCHAR(50),
        distancia_m INTEGER,
        tiempo_segundos NUMERIC(6,2),
        brazadas INTEGER
    );

    -- 4. Lesiones
    CREATE TABLE IF NOT EXISTS lesiones (
        id_lesion SERIAL PRIMARY KEY,
        id_nadador INTEGER REFERENCES nadadores(id_nadador) ON DELETE CASCADE,
        zona_afectada VARCHAR(100),
        fecha_incidente DATE,
        estado_actual VARCHAR(50)
    );

    -- 5. Rehabilitaciones
    CREATE TABLE IF NOT EXISTS rehabilitaciones (
        id_rehab SERIAL PRIMARY KEY,
        id_lesion INTEGER REFERENCES lesiones(id_lesion) ON DELETE CASCADE,
        tipo_terapia VARCHAR(100),
        tiempo_estimado_dias INTEGER,
        especificaciones_entrenador TEXT,
        fecha_inicio DATE DEFAULT CURRENT_DATE,
        fecha_fin DATE
    );
    """
    
    try:
        cur = conn.cursor()
        cur.execute(tablas_sql)
        conn.commit()
        print("Tablas creadas y estructuradas con éxito.")
    except psycopg2.Error as e:
        print(f"Error al crear tablas: {e}")
    finally:
        cur.close()
        conn.close()

# ================= MÉTODOS CRUD =================

def insertar_nadador(nombre, rama, fecha_nacimiento):
    """Guarda un nuevo nadador en el sistema."""
    conn = obtener_conexion()
    if not conn: return False, "Error de conexión con la base de datos"
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO nadadores (nombre, rama, fecha_nacimiento) VALUES (%s, %s, %s)", 
                    (nombre, rama, fecha_nacimiento))
        conn.commit()
        return True, "Nadador registrado exitosamente"
    except psycopg2.Error as e:
        return False, f"Error de BD: {str(e)}"
    finally:
        cur.close()
        conn.close()

def registrar_rehabilitacion(id_lesion, tipo_terapia, dias, especificaciones):
    """Registra el plan de rehabilitación estructurado por el entrenador."""
    conn = obtener_conexion()
    if not conn: return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO rehabilitaciones (id_lesion, tipo_terapia, tiempo_estimado_dias, especificaciones_entrenador) 
            VALUES (%s, %s, %s, %s)
            """, (id_lesion, tipo_terapia, dias, especificaciones))
        conn.commit()
        return True, "Rehabilitación asignada correctamente"
    except psycopg2.Error as e:
        return False, f"Error de BD: {str(e)}"
    finally:
        cur.close()
        conn.close()

# Si ejecutas este archivo directamente, crea las tablas.
if __name__ == "__main__":
    crear_tablas()