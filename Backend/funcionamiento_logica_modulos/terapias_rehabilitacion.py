import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion

# ================= REHABILITACIONES =================
def registrar_rehabilitacion(nadador_id, tipo_terapia, tiempo_estimado_dias, especificaciones_entrenador=None, fecha_fin=None):
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexion"

    try:
        cur = conn.cursor()

        # busca la lesion activa mas reciente del nadador
        cur.execute("""
            SELECT id FROM lesiones
            WHERE nadador_id = %s AND activo = TRUE
            ORDER BY fecha_inicio DESC
            LIMIT 1
        """, (nadador_id,))
        lesion = cur.fetchone()

        if not lesion:
            return False, "No hay lesion activa para este nadador"

        lesion_id = lesion[0]

        cur.execute("""
            INSERT INTO rehabilitaciones
            (lesion_id, nadador_id, tipo_terapia, tiempo_estimado_dias,
             especificaciones_entrenador, fecha_fin)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (lesion_id, nadador_id, tipo_terapia, tiempo_estimado_dias,
              especificaciones_entrenador, fecha_fin))
        conn.commit()
        return True, "Terapia registrada correctamente"

    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def obtener_historial_rehabilitaciones(nadador_id):
    conn = obtener_conexion()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, lesion_id, nadador_id, tipo_terapia, tiempo_estimado_dias,
                   especificaciones_entrenador, fecha_inicio, fecha_fin
            FROM rehabilitaciones
            WHERE nadador_id = %s
            ORDER BY fecha_inicio DESC
        """, (nadador_id,))

        registros = cur.fetchall()
        historial = []

        for row in registros:
            historial.append({
                "id": row[0],
                "lesion_id": row[1],
                "nadador_id": row[2],
                "tipo_terapia": row[3],
                "tiempo_estimado_dias": row[4],
                "especificaciones": row[5],
                "fecha_inicio": row[6],
                "fecha_fin": row[7]
            })

        return historial

    except psycopg2.Error as e:
        print("Error obteniendo historial:", e)
        return []
    finally:
        conn.close()

def actualizar_rehabilitacion(rehab_id, tipo_terapia, tiempo_estimado, especificaciones):
    """
    Permite editar los detalles de la rehabilitación en caso de error.
    """
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE rehabilitaciones
            SET tipo_terapia = %s, tiempo_estimado_dias = %s, especificaciones_entrenador = %s
            WHERE id = %s
        """, (tipo_terapia, tiempo_estimado, especificaciones, rehab_id))
        
        conn.commit()
        return True, "Datos de rehabilitación actualizados"
        
    except psycopg2.Error as e:
        conn.rollback()
        return False, str(e)
        
    finally:
        conn.close()

def finalizar_rehabilitacion(rehab_id):
    """
    Marca la rehabilitación como terminada, asignando la fecha de hoy.
    """
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE rehabilitaciones
            SET fecha_fin = CURRENT_DATE
            WHERE id = %s
        """, (rehab_id,))
        
        conn.commit()
        return True, "Rehabilitación finalizada con éxito"
        
    except psycopg2.Error as e:
        conn.rollback()
        return False, str(e)
        
    finally:
        conn.close()

def eliminar_rehabilitacion(rehab_id):
    """
    Borra un registro de rehabilitación en caso de que se haya creado por error.
    """
    conn = obtener_conexion()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM rehabilitaciones
            WHERE id = %s
        """, (rehab_id,))
        
        conn.commit()
        return cur.rowcount > 0 
        
    except psycopg2.Error as e:
        conn.rollback()
        print("❌ Error al eliminar rehabilitación:", e)
        return False
        
    finally:
        conn.close()