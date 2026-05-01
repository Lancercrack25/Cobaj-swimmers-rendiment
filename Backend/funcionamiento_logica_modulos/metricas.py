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
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def obtener_metricas_nadador(nadador_id):
    """
    Extrae el historial de rendimiento de un nadador.
    Los datos vienen ordenados por fecha de forma ascendente (del más viejo al más nuevo),
    lo cual es perfecto para alimentar el Eje X y Eje Y de una gráfica.
    """
    conn = obtener_conexion()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, sesion_id, distancia_m, tiempo_seg, ritmo, fecha
            FROM rendimiento_nadador
            WHERE nadador_id = %s
            ORDER BY fecha ASC
        """, (nadador_id,))
        
        registros = cur.fetchall()
        metricas = []
        
        for row in registros:
            metricas.append({
                "id": row[0],
                "sesion_id": row[1],
                "distancia_m": row[2],
                "tiempo_seg": row[3],
                "ritmo": float(row[4]), # Se castea a float por si la DB lo regresa como Decimal
                "fecha": row[5]
            })
            
        return metricas

    except psycopg2.Error as e:
        print("❌ Error obteniendo métricas:", e)
        return []
    finally:
        conn.close()