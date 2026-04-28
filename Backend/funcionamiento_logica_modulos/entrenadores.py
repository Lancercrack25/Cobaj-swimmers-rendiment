import psycopg2
from Backend.conection_database import obtener_conexion

# ================= ENTRENADORES =================

def registrar_entrenador(nombre, edad, experiencia, especialidad, password):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO entrenadores
            (nombre, edad, experiencia_anios, especialidad, password_hash, activo)
            VALUES (%s,%s,%s,%s,%s,TRUE)
        """, (nombre, edad, experiencia, especialidad, password))
        conn.commit()
        return True, "Entrenador registrado correctamente"
    except psycopg2.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def login_entrenador(nombre, password):
    conn = obtener_conexion()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre
            FROM entrenadores
            WHERE nombre=%s AND password_hash=%s AND activo=TRUE
        """, (nombre, password))
        res = cur.fetchone()
        return res
    except psycopg2.Error as e:
        print("❌ Error login:", e)
        return None
    finally:
        conn.close()

def obtener_entrenador_por_id(entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return None

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nombre
            FROM entrenadores
            WHERE id = %s AND activo = TRUE
        """, (entrenador_id,))

        res = cur.fetchone()

        if res:
            return {
                "id": res[0],
                "nombre": res[1]
            }

        return None

    except Exception as e:
        print("❌ Error obteniendo entrenador:", e)
        return None

    finally:
        conn.close()