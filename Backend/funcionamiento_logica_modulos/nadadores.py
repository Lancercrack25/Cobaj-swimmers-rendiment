import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion

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
