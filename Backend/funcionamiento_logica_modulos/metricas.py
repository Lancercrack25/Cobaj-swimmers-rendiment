import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion
from Backend.funcionamiento_logica_modulos.lesiones import puede_entrenar

# ================= RENDIMIENTO =================

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