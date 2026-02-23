import psycopg2
from psycopg2 import sql
import os

# ================= CONFIGURACIÓN =================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "L123"),
    "dbname": os.getenv("DB_NAME", "nadadores_db"),
}

# ================= CONEXIÓN =================

def obtener_conexion():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print("❌ Error de conexión:", e)
        return None

# ================= CREAR BD =================

def crear_bd_si_no_existe():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_CONFIG["dbname"],))
        existe = cur.fetchone()

        if not existe:
            cur.execute(
                sql.SQL("CREATE DATABASE {};").format(
                    sql.Identifier(DB_CONFIG["dbname"])
                )
            )
            print("✔ Base de datos creada correctamente")
        else:
            print("✔ Base de datos ya existe")

        cur.close()
    except Exception as e:
        print("❌ Error creando base de datos:", e)
    finally:
        if conn:
            conn.close()

# ================= CREAR TABLAS =================

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

# ================= ENTRENADORES =================

def registrar_entrenador(nombre, edad, experiencia, especialidad, password):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO entrenadores
            (nombre, edad, experiencia_anios, especialidad, password, activo)
            VALUES (%s,%s,%s,%s,%s,TRUE)
        """, (nombre, edad, experiencia, especialidad, password))
        conn.commit()
        return True, "Entrenador registrado correctamente"
    except psycopg2.Error as e:
        return False, str(e)
    finally:
        conn.close()

def login_entrenador(nombre, password):
    conn = obtener_conexion()
    if not conn:
        return None

    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre
        FROM entrenadores
        WHERE nombre=%s AND password=%s AND activo=TRUE
    """, (nombre, password))

    res = cur.fetchone()
    conn.close()
    return res

# ================= NADADORES =================

def registrar_nadador(nombre, edad, genero, peso, estatura,
                      problema_respiratorio, entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO nadadores
            (nombre, edad, genero, peso, estatura,
             problema_respiratorio, entrenador_id, activo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,TRUE)
        """, (nombre, edad, genero, peso, estatura,
              problema_respiratorio, entrenador_id))
        conn.commit()
        return True, "Nadador registrado correctamente"
    except psycopg2.Error as e:
        return False, str(e)
    finally:
        conn.close()

def obtener_nadadores(entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return []

    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, edad, genero, peso, estatura,
               problema_respiratorio
        FROM nadadores
        WHERE entrenador_id=%s AND activo=TRUE
        ORDER BY nombre
    """, (entrenador_id,))

    res = cur.fetchall()
    conn.close()
    return res

# ================= SESIONES =================

def crear_sesion(entrenador_id, fecha, tipo, descripcion):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sesiones_entrenamiento
            (entrenador_id, fecha, tipo, descripcion)
            VALUES (%s,%s,%s,%s)
        """, (entrenador_id, fecha, tipo, descripcion))
        conn.commit()
        return True, "Sesión creada correctamente"
    except psycopg2.Error as e:
        return False, str(e)
    finally:
        conn.close()

# ================= RENDIMIENTO =================

def puede_entrenar(nadador_id):
    conn = obtener_conexion()
    if not conn:
        return False

    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM lesiones
        WHERE nadador_id=%s AND activo=TRUE
    """, (nadador_id,))

    res = cur.fetchone()[0]
    conn.close()
    return res == 0

def registrar_rendimiento(nadador_id, sesion_id, distancia, tiempo):
    if distancia <= 0 or tiempo <= 0:
        return False, "Datos inválidos"

    if not puede_entrenar(nadador_id):
        return False, "Nadador lesionado"

    ritmo = round(tiempo / distancia, 3)

    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO rendimiento_nadador
            (nadador_id, sesion_id, distancia_m, tiempo_seg, ritmo, fecha)
            VALUES (%s,%s,%s,%s,%s,CURRENT_DATE)
        """, (nadador_id, sesion_id, distancia, tiempo, ritmo))
        conn.commit()
        return True, "Rendimiento registrado correctamente"
    except psycopg2.Error as e:
        return False, str(e)
    finally:
        conn.close()

# ================= LESIONES =================

def registrar_lesion(nadador_id, tipo, gravedad, observaciones):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO lesiones
            (nadador_id, tipo_lesion, gravedad,
             fecha_inicio, activo, observaciones)
            VALUES (%s,%s,%s,CURRENT_DATE,TRUE,%s)
        """, (nadador_id, tipo, gravedad, observaciones))
        conn.commit()
        return True, "Lesión registrada correctamente"
    except psycopg2.Error as e:
        return False, str(e)
    finally:
        conn.close()

def finalizar_lesion(lesion_id):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE lesiones
            SET activo=FALSE, fecha_fin=CURRENT_DATE
            WHERE id=%s
        """, (lesion_id,))
        conn.commit()
        return True, "Lesión finalizada correctamente"
    except psycopg2.Error as e:
        return False, str(e)
    finally:
        conn.close()

# ================= INICIALIZACIÓN =================

def inicializar_sistema():
    crear_bd_si_no_existe()
    crear_tablas_si_no_existen()