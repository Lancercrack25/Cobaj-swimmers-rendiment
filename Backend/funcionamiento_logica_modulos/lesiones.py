import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion

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