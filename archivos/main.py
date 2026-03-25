import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.dont_write_bytecode = True

#importar funciones de otros archivos desde aqui 
from archivos.Entrenador.interface_general import interfaz_general
from archivos.Nadadores.interface_swimmers import interfaz_nadador
from Backend.database import inicializar_sistema, obtener_conexion, registrar_entrenador, login_entrenador

# ================= CONFIG =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SESSION = {
    "id": None,
    "rol": None
}
# ================= FUNCIONES =================
def limpiar():
    user_entry.delete(0, 'end')
    pass_entry.delete(0, 'end')

# -------- CAMBIAR A NADADOR --------
def cambiar_a_nadador():
    limpiar()
    titulo.configure(text="Login Nadador")
    label_user.configure(text="Código de acceso")

    # Ocultar contraseña
    label_pass.pack_forget()
    pass_entry.pack_forget()

    btn_login.configure(text="Ingresar Nadador", command=login_nadador)
    btn_switch.configure(text="Modo Entrenador", command=cambiar_a_entrenador)

# -------- CAMBIAR A ENTRENADOR --------
def cambiar_a_entrenador():
    limpiar()
    titulo.configure(text="Login Entrenador")
    label_user.configure(text="Usuario")

    # Mostrar contraseña otra vez
    label_pass.pack(pady=(10, 0))
    pass_entry.pack(pady=5)

    btn_login.configure(text="Ingresar", command=login_entrenador_ui)
    btn_switch.configure(text="Modo Nadador", command=cambiar_a_nadador)

# ================= LOGIN ENTRENADOR =================
def login_entrenador_ui():
    nombre = user_entry.get().strip()
    password = pass_entry.get().strip()

    if not nombre or not password:
        messagebox.showerror("Error", "Completa todos los campos")
        return

    res = login_entrenador(nombre, password)

    if res:
        SESSION["id"] = res[0]
        SESSION["rol"] = "entrenador"

        messagebox.showinfo("Acceso", f"Bienvenido entrenador {res[1]}")
        ventana.destroy()
        interfaz_general()
    else:
        messagebox.showerror("Error", "Credenciales inválidas")


# ================= LOGIN NADADOR =================
def login_nadador():
    codigo = user_entry.get().strip()

    if not codigo:
        messagebox.showerror("Error", "Ingresa tu código de acceso")
        return

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre 
        FROM nadadores
        WHERE codigo_acceso = %s AND activo = TRUE
    """, (codigo,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        id_nadador, nombre = resultado

        SESSION["id"] = id_nadador
        SESSION["rol"] = "nadador"

        messagebox.showinfo("Bienvenido", f"Hola {nombre}")
        ventana.destroy()
        interfaz_nadador()
    else:
        messagebox.showerror("Error", "Código inválido o nadador inactivo")


# ================= REGISTRO ENTRENADOR =================
def ventana_registro():
    registro = ctk.CTkToplevel(ventana)
    registro.title("Registro Entrenador")
    registro.geometry("360x430")

    entries = {}

    for campo in ["Nombre", "Edad", "Experiencia (años)", "Especialidad", "Contraseña"]:
        ctk.CTkLabel(registro, text=campo).pack(pady=4)
        ent = ctk.CTkEntry(registro, show="*" if campo == "Contraseña" else "")
        ent.pack()
        entries[campo] = ent

    def registrar():
        try:
            nombre = entries["Nombre"].get()
            edad = int(entries["Edad"].get())
            exp = int(entries["Experiencia (años)"].get())
            esp = entries["Especialidad"].get()
            pwd = entries["Contraseña"].get()

            if not all([nombre, esp, pwd]):
                raise ValueError

        except:
            messagebox.showerror("Error", "Datos inválidos")
            return

        ok, msg = registrar_entrenador(nombre, edad, exp, esp, pwd)

        if ok:
            messagebox.showinfo("Registro exitoso", msg)
            registro.destroy()
        else:
            messagebox.showerror("Error", msg)

    ctk.CTkButton(registro, text="Registrar", command=registrar).pack(pady=15)

# ================= UI =================
ventana = ctk.CTk()
ventana.title("Sistema de Rendimiento Deportivo")
ventana.geometry("380x420")

titulo = ctk.CTkLabel(ventana, text="Login Entrenador", font=("Arial", 20))
titulo.pack(pady=20)

label_user = ctk.CTkLabel(ventana, text="Usuario")
label_user.pack()

user_entry = ctk.CTkEntry(ventana, width=220)
user_entry.pack(pady=5)

label_pass = ctk.CTkLabel(ventana, text="Contraseña")
label_pass.pack(pady=(10, 0))

pass_entry = ctk.CTkEntry(ventana, show="*", width=220)
pass_entry.pack(pady=5)

btn_login = ctk.CTkButton(ventana, text="Ingresar", command=login_entrenador_ui)
btn_login.pack(pady=15)

btn_switch = ctk.CTkButton(
    ventana,
    text="Modo Nadador",
    fg_color="red",
    command=cambiar_a_nadador
)
btn_switch.pack(pady=5)

ctk.CTkButton(
    ventana,
    text="Registrarse como entrenador",
    fg_color="#50a51f",
    command=ventana_registro
).pack(pady=10)

# Inicializar base de datos antes de iniciar
ventana.mainloop()
inicializar_sistema()