import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion

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

    