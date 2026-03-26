import psycopg2
from psycopg2 import sql
import os
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