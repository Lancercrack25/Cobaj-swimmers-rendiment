import psycopg2
from psycopg2 import sql
import os

# ================= CONFIGURACIÓN =================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "L123"),
    "dbname": os.getenv("DB_NAME", "nadadores_db"),
}

# ================= CONEXIÓN =================
def obtener_conexion():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print("❌ Error de conexión:", e)
        return None