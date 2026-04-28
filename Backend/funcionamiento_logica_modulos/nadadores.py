import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion
# ================= NADADORES =================
def registrar_nadador(nombre, edad, codigo, genero, peso, estatura, problema,password):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO nadadores
        (nombre, edad, codigo_acceso, genero, peso, estatura, password, problema_respiratorio, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
    """, (nombre, edad, codigo, genero, peso, estatura, password, problema))
        conn.commit()
        return True, "Nadador registrado correctamente"

    except psycopg2.Error as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()

def login_nadador(codigo, password):
    conn = obtener_conexion()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre
            FROM nadadores
            WHERE codigo_acceso=%s AND password=%s AND activo=TRUE
        """, (codigo, password))

        res = cur.fetchone()
        return res

    except psycopg2.Error as e:
        print("❌ Error login nadador:", e)
        return None

    finally:
        conn.close()

def obtener_nadadores(entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, edad, genero, codigo_acceso,
                   peso, estatura, problema_respiratorio
            FROM   nadadores
            WHERE  entrenador_id = %s AND activo = TRUE
            ORDER  BY nombre
        """, (entrenador_id,))

        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    except psycopg2.Error as e:
        print("❌ Error al obtener nadadores:", e)
        return []

    finally:
        conn.close()

def eliminar_nadador(nadador_id, entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE nadadores
            SET    activo = FALSE
            WHERE  id = %s
              AND  entrenador_id = %s
              AND  activo = TRUE
        """, (nadador_id, entrenador_id))

        conn.commit()
        return cur.rowcount > 0

    except psycopg2.Error as e:
        print("❌ Error al eliminar nadador:", e)
        return False

    finally:
        conn.close()

def buscar_nadador_por_codigo(codigo, entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, codigo_acceso
            FROM   nadadores
            WHERE  codigo_acceso = %s
              AND  entrenador_id = %s
              AND  activo = TRUE
            LIMIT 1
        """, (codigo, entrenador_id))

        res = cur.fetchone()

        if not res:
            return None

        return {
            "id": res[0],
            "nombre": res[1],
            "codigo_acceso": res[2]
        }

    except psycopg2.Error as e:
        print("❌ Error al buscar nadador por código:", e)
        return None

    finally:
        conn.close()