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