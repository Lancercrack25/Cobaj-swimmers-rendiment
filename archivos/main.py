import customtkinter as ctk
from tkinter import messagebox
import os
import sys
import psycopg2
from psycopg2 import sql
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interface_general import interfaz_general
from Backend.generar_csv import exportar_tablas_a_csv
from Backend.database import DB_CONFIG
from Backend.asistente import talk

def login():
	adminname = datos.get()
	password = contraseña_dato.get()
	
	if adminname == "Luis" and password == "admin123":
		talk(f"Bienvenido {adminname}, en unos momentos podras acceder al sistema.")
		messagebox.showinfo("Login Exitoso", f"preparando sistema para {adminname}...")
		time.sleep(2)
		window.destroy()
		interfaz_general()
		return
	else:
		talk("Usuario o contraseña  que ingresaste es incorrecto, intente de nuevo por favor.")	
		messagebox.showerror("Error de Login", "Ingresa de nuevo tus datos correctamente.")


def create_database_if_not_exists(cfg: dict):
	try:
		# Conectarse a la base de datos por defecto 'postgres' para operaciones administrativas
		admin_conn = psycopg2.connect(
			dbname="postgres",
			user=cfg["user"],
			password=cfg["password"],
			host=cfg["host"],
			port=cfg["port"],
		)
		admin_conn.autocommit = True
		cur = admin_conn.cursor()
		# Comprobar si la base de datos ya existe
		cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (cfg["dbname"],))
		exists = cur.fetchone() is not None
		if exists:
			print(f"La base de datos '{cfg['dbname']}' ya existe. No se creará de nuevo.")
		else:
			cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(cfg["dbname"])))
			create_tables_if_not_exists(DB_CONFIG)
			print(f"Base de datos '{cfg['dbname']}' creada correctamente.")

		cur.close()
	except Exception as e:
		print("Error al verificar/crear la base de datos:", e)
	finally:
		if admin_conn:
			admin_conn.close()

def get_connection(cfg: dict):
	if psycopg2 is None:
		print("psycopg2 no está instalado. Ejecuta: pip install psycopg2-binary")
		return None

	try:
		conn = psycopg2.connect(
			dbname=cfg["dbname"],
			user=cfg["user"],
			password=cfg["password"],
			host=cfg["host"],
			port=cfg["port"],
		)
		return conn
	except Exception as e:
		print("No se pudo conectar a la base de datos:", e)
		return None

def create_tables_if_not_exists(cfg: dict):
    """Crea las tablas iniciales si no existen en la base de datos objetivo."""
    conn = None

    try:
        conn = get_connection(cfg)
        if conn is None:
            print("No hay conexión a la base de datos. No se crearán tablas.")
            return

        with conn.cursor() as cur:

            # Tabla de jugadores
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jugadores (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    nickname TEXT UNIQUE,
                    creado_en TIMESTAMP DEFAULT now()
                );
            """)

            # Tabla de rachas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rachas (
                    id SERIAL PRIMARY KEY,
                    jugador_id INTEGER NOT NULL,
                    victorias INTEGER DEFAULT 0,
                    derrotas INTEGER DEFAULT 0,
                    fecha TIMESTAMP DEFAULT now(),
                    CONSTRAINT fk_jugador
                        FOREIGN KEY (jugador_id)
                        REFERENCES jugadores(id)
                        ON DELETE CASCADE
                );
            """)

        conn.commit()
        print("Tablas iniciales creadas/aseguradas correctamente.")

    except Exception as e:
        print("Error al crear tablas:", e)

    finally:
        if conn:
            conn.close()

window = ctk.CTk()
window.title("Login - Sistema de Inventario")
window.geometry("300x300")

titulo =ctk.CTkLabel(window,text="Ingrese su usuario").pack()
datos = ctk.CTkEntry(window, width=170, border_color="grey")
datos.pack(pady=3)

contraseña =ctk.CTkLabel(window,text="Ingrese su contraseña").pack()
contraseña_dato= ctk.CTkEntry(window, width=170, border_color="grey", show="*")
contraseña_dato.pack(pady=3)

verificacion = ctk.CTkButton(window,text="Login",fg_color="#459C0A",command=login).pack(pady =8)
create_database_if_not_exists(DB_CONFIG)
exportar_tablas_a_csv()
window.mainloop()