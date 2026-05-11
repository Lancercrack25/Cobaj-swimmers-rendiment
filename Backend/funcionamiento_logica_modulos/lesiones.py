import psycopg2
from psycopg2 import sql
import os
from Backend.conection_database import obtener_conexion

# ================= LESIONES =================
def registrar_lesion(nadador_id, tipo, gravedad, fecha_inicio, fecha_fin, observaciones):
    print(f">>> nadador_id recibido: '{nadador_id}' tipo: {type(nadador_id)}")
    
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexion"

    try:
        cur = conn.cursor()

        cur.execute("SELECT id, codigo_acceso FROM nadadores")
        todos = cur.fetchall()
        print(f">>> Nadadores en BD: {todos}")

        cur.execute("SELECT id FROM nadadores WHERE codigo_acceso = %s", (str(nadador_id),))
        resultado = cur.fetchone()
        print(f">>> Resultado por codigo_acceso: {resultado}")

        if not resultado:
            try:
                cur.execute("SELECT id FROM nadadores WHERE id = %s", (int(nadador_id),))
                resultado = cur.fetchone()
                print(f">>> Resultado por id numerico: {resultado}")
            except (ValueError, Exception) as e:
                print(f">>> Error buscando por id numerico: {e}")

        if not resultado:
            return False, "Nadador no encontrado"

        id_real = resultado[0]
        print(f">>> id_real encontrado: {id_real}")

        cur.execute("""
            INSERT INTO lesiones
            (nadador_id, tipo_lesion, gravedad, fecha_inicio, fecha_fin, activo, observaciones)
            VALUES (%s,%s,%s,%s,%s,TRUE,%s)
        """, (id_real, tipo, gravedad, fecha_inicio, fecha_fin, observaciones))
        conn.commit()
        return True, "Lesion registrada correctamente"

    except Exception as e:
        conn.rollback()
        print(f">>> Error SQL: {e}")
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
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def obtener_historial_lesiones(nadador_id):
    """
    Retorna una lista de diccionarios con el historial médico del nadador.
    Ideal para rellenar las tablas de CustomTkinter.
    """
    conn = obtener_conexion()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, tipo_lesion, gravedad, fecha_inicio, fecha_fin, activo, observaciones
            FROM lesiones
            WHERE nadador_id = %s
            ORDER BY fecha_inicio DESC
        """, (nadador_id,))
        
        registros = cur.fetchall()
        historial = []
        
        # Transformamos la tupla en un diccionario para que sea más fácil leerlo en la interfaz
        for row in registros:
            historial.append({
                "id": row[0],
                "tipo_lesion": row[1],
                "gravedad": row[2],
                "fecha_inicio": row[3],
                "fecha_fin": row[4],
                "activo": row[5],
                "observaciones": row[6]
            })
            
        return historial

    except psycopg2.Error as e:
        print("❌ Error obteniendo historial de lesiones:", e)
        return []
    finally:
        conn.close()


def puede_entrenar(nadador_id):
    """
    Verifica si el nadador tiene alguna lesión activa.
    Ya cuenta con el blindaje try-except para evitar crasheos.
    """
    conn = obtener_conexion()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM lesiones
            WHERE nadador_id=%s AND activo=TRUE
        """, (nadador_id,))
        
        res = cur.fetchone()[0]
        return res == 0 # Retorna True si tiene 0 lesiones activas
        
    except psycopg2.Error as e:
        print("❌ Error verificando estado médico:", e)
        # Por seguridad, si falla la base de datos, asumimos que NO puede entrenar
        return False 
    finally:
        conn.close()