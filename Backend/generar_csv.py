import psycopg2
import csv
import os

# Configuración de la base de datos
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "L123"),
    "dbname": os.getenv("DB_NAME", "jugadores_db"),
}

def exportar_tablas_a_csv():
    """
    Conecta a la base de datos y exporta las tablas 'jugadores' y 'rachas'
    a archivos CSV en la misma carpeta donde se ejecuta este script.
    """
    # Obtener la ruta del directorio donde está este archivo (backend)
    directorio_backend = os.path.dirname(os.path.abspath(__file__))
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        tablas = ["jugadores", "rachas"]

        for tabla in tablas:
            ruta_archivo = os.path.join(directorio_backend, f"{tabla}.csv")
    
            print(f"Exportando tabla '{tabla}' a {ruta_archivo}...")
            
            # Seleccionar todos los datos de la tabla
            cur.execute(f"SELECT * FROM {tabla}")
            
            # Obtener nombres de columnas y filas
            encabezados = [desc[0] for desc in cur.description]
            filas = cur.fetchall()

            # Escribir el archivo CSV
            with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(encabezados)
                writer.writerows(filas)
            
            print(f"-> Archivo generado: {ruta_archivo}")

        cur.close()
        conn.close()
        print("\n¡Exportación completada exitosamente!")

    except psycopg2.Error as e:
        print(f"Error de Base de Datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
