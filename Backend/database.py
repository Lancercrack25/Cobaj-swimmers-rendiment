import psycopg2
import os

# Configuración centralizada
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "L123"),
    "dbname": os.getenv("DB_NAME", "jugadores_db"),
}

def obtener_conexion():
    """Crea y retorna una conexión a la base de datos."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error de conexión: {e}")
        return None

def insertar_jugador(nombre, nickname):
    """Guarda un nuevo jugador."""
    conn = obtener_conexion()
    if not conn: return False, "Error de conexión con la base de datos"
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO jugadores (nombre, nickname) VALUES (%s, %s)", (nombre, nickname))
        conn.commit()
        cur.close()
        conn.close()
        return True, "Jugador registrado exitosamente"
    except psycopg2.Error as e:
        return False, f"Error de BD: {str(e)}"

def eliminar_jugador_db(nickname):
    """Elimina un jugador."""
    conn = obtener_conexion()
    if not conn: return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM jugadores WHERE nickname = %s", (nickname,))
        filas = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if filas > 0:
            return True, "Jugador eliminado correctamente"
        else:
            return False, "No se encontró el jugador"
    except psycopg2.Error as e:
        return False, f"Error de BD: {str(e)}"

def obtener_rachas_jugador(nickname):
    """Obtiene historial de rachas."""
    conn = obtener_conexion()
    if not conn: return None, "Error de conexión"

    try:
        cur = conn.cursor()
        query = """
            SELECT r.victorias, r.derrotas, r.fecha
            FROM rachas r
            JOIN jugadores j ON r.jugador_id = j.id
            WHERE j.nickname = %s
            ORDER BY r.fecha ASC
        """
        cur.execute(query, (nickname,))
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return resultados, "Ok"
    except psycopg2.Error as e:
        return None, str(e)

def registrar_racha_db(nickname, victorias, derrotas):
    """Registra una racha."""
    conn = obtener_conexion()
    if not conn: return False, "Error de conexión"

    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM jugadores WHERE nickname = %s", (nickname,))
        res = cur.fetchone()
        
        if not res:
            conn.close()
            return False, "El jugador no existe"
            
        jugador_id = res[0]
        cur.execute(
            "INSERT INTO rachas (jugador_id, victorias, derrotas) VALUES (%s, %s, %s)",
            (jugador_id, int(victorias), int(derrotas))
        )
        conn.commit()
        cur.close()
        conn.close()
        return True, "Racha registrada correctamente"
    except psycopg2.Error as e:
        return False, f"Error de BD: {str(e)}"