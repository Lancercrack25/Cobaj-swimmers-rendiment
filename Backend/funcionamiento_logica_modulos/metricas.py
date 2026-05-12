import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion
from Backend.funcionamiento_logica_modulos.lesiones import puede_entrenar

# ================= RENDIMIENTO =================
def registrar_rendimiento(nadador_id, sesion_id, distancia, tiempo):
    if distancia <= 0 or tiempo <= 0:
        return False, "Datos invalidos"

    if not puede_entrenar(nadador_id):
        return False, "Nadador lesionado"

    ritmo = round(tiempo / distancia, 3)

    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexion"

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO rendimiento_nadador
            (nadador_id, sesion_id, distancia_m, tiempo_seg, ritmo)
            VALUES (%s,%s,%s,%s,%s)
        """, (nadador_id, sesion_id, distancia, tiempo, ritmo))
        conn.commit()
        return True, "Rendimiento registrado correctamente"
    except psycopg2.Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

# ================= METRICAS =================

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

def obtener_estadisticas_globales(nombre_entrenador):
    conn = obtener_conexion()
    if not conn:
        return None

    try:
        cur = conn.cursor()

        # busca el entrenador por nombre
        cur.execute("SELECT id FROM entrenadores WHERE nombre = %s", (nombre_entrenador,))
        entrenador = cur.fetchone()

        if not entrenador:
            return None

        entrenador_id = entrenador[0]

        # total de sesiones del entrenador
        cur.execute("""
            SELECT COUNT(*) FROM sesiones_entrenamiento
            WHERE entrenador_id = %s
        """, (entrenador_id,))
        total_sesiones = cur.fetchone()[0]

        # total de nadadores asignados al entrenador
        cur.execute("""
            SELECT COUNT(*) FROM nadadores
            WHERE entrenador_id = %s AND activo = TRUE
        """, (entrenador_id,))
        total_nadadores = cur.fetchone()[0]

        # promedios de rendimiento de todos los nadadores del entrenador
        cur.execute("""
            SELECT 
                AVG(rn.distancia_m),
                AVG(rn.tiempo_seg),
                AVG(rn.ritmo)
            FROM rendimiento_nadador rn
            JOIN nadadores n ON rn.nadador_id = n.id
            WHERE n.entrenador_id = %s
        """, (entrenador_id,))

        promedios = cur.fetchone()

        return {
            "total_sesiones": total_sesiones,
            "total_nadadores": total_nadadores,
            "distancia_promedio": float(promedios[0]) if promedios[0] else 0,
            "tiempo_promedio": float(promedios[1]) if promedios[1] else 0,
            "ritmo_promedio": float(promedios[2]) if promedios[2] else 0,
        }

    except Exception as e:
        print("❌ Error obteniendo estadísticas globales:", e)
        return None
    finally:
        conn.close()