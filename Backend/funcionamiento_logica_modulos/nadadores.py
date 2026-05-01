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
        conn.rollback()
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

def buscar_nadador_por_codigo_global(codigo):
    conn = obtener_conexion()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, codigo_acceso
            FROM nadadores
            WHERE codigo_acceso = %s
        """, (codigo,))
        res = cur.fetchone()
        print(f"DB resultado: {res}")  # ← agrega esto también
        return {"id": res[0], "nombre": res[1], "codigo_acceso": res[2]} if res else None
    except Exception as e:
        print("❌ Error:", e)
        return None
    finally:
        conn.close()

def vincular_nadador_entrenador(nadador_id, entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE nadadores
            SET entrenador_id = %s
            WHERE id = %s
        """, (entrenador_id, nadador_id))
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print("❌ Error:", e)
        return False
    finally:
        conn.close()

def desvincular_nadador_entrenador(nadador_id, entrenador_id):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE nadadores
            SET entrenador_id = NULL
            WHERE id = %s AND entrenador_id = %s
        """, (nadador_id, entrenador_id))
        conn.commit()
        return cur.rowcount > 0
    except psycopg2.Error as e:
        conn.rollback()
        print("❌ Error al desvincular nadador:", e)
        return False
    finally:
        conn.close()

def obtener_nadador_por_id(nadador_id):
    conn = obtener_conexion()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, edad, codigo_acceso, genero,
                   peso, estatura, problema_respiratorio
            FROM nadadores
            WHERE id = %s AND activo = TRUE
        """, (nadador_id,))
        res = cur.fetchone()
        if not res:
            return None
        cols = [d[0] for d in cur.description]
        return dict(zip(cols, res))
    except Exception as e:
        print("❌ Error:", e)
        return None
    finally:
        conn.close()

def actualizar_nadador(nadador_id, nombre, edad, peso, estatura, problema):
    """
    Actualiza los datos físicos y generales del nadador.
    """
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE nadadores
            SET nombre = %s, edad = %s, peso = %s, estatura = %s, problema_respiratorio = %s
            WHERE id = %s AND activo = TRUE
        """, (nombre, edad, peso, estatura, problema, nadador_id))
        
        conn.commit()
        return True, "Datos actualizados correctamente"

    except psycopg2.Error as e:
        conn.rollback()
        print("❌ Error al actualizar nadador:", e)
        return False, "Error al actualizar en la base de datos"

    finally:
        conn.close()