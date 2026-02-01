import customtkinter as ctk
from tkinter import messagebox
from interface_stadistics import regresar
from Backend.database import insertar_jugador, eliminar_jugador_db

def registro():
    window = ctk.CTk()
    window.title("Registro de Jugadores")
    window.geometry("400x420")
    window.configure(fg_color="#181A17")

    etiqueta_titulo = ctk.CTkLabel(window, text="Registro de Jugadores", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    ingreso_nombre = ctk.CTkEntry(window, width=200, placeholder_text="Ingresa tu nombre")
    ingreso_nombre.pack(pady=5)

    ingreso_nickname = ctk.CTkEntry(window, width=200, placeholder_text="Ingresa tu nickname")
    ingreso_nickname.pack(pady=5)
    boton_registrar = ctk.CTkButton(window, text="Registrar", fg_color="#459C0A", command=lambda: ejecutar_registro(ingreso_nombre, ingreso_nickname))
    boton_registrar.pack(pady=8)

    retur_button = ctk.CTkButton(window, text="Regresar al Menú Principal", fg_color="#9C510A", command=lambda: regresar(window))
    retur_button.pack(pady=8)
    window.mainloop()

def ejecutar_registro(ingreso_nombre, ingreso_nickname):
    if validacion(ingreso_nombre, ingreso_nickname):
        nombre = ingreso_nombre.get()
        nickname = ingreso_nickname.get()
        
        exito, mensaje = insertar_jugador(nombre, nickname)
        
        if exito:
            messagebox.showinfo("Registro Exitoso", mensaje)
            ingreso_nombre.delete(0, "end")
            ingreso_nickname.delete(0, "end")
        else:
            messagebox.showerror("Error", mensaje)


def validacion(ingreso_nombre, ingreso_nickname):

    nombre = ingreso_nombre.get()
    nickname = ingreso_nickname.get()

    if not nombre or not nickname:
        messagebox.showerror("Error de Validación", "Todos los campos son obligatorios.")
        return False
    if nombre == nickname:
        messagebox.showerror("Error de Validación", "El nombre y el nickname no pueden ser iguales, debes de ser creativo con tu nickname")
        return False
    if nombre.isdigit() or nickname.isdigit():
        messagebox.showerror("Error de Validación", "El nombre y el nickname no pueden ser solo números.")
        return False
    else:
        return True

def eliminacion():
    window = ctk.CTk()
    window.title("Eliminacion de Jugadores")
    window.geometry("400x200")
    window.configure(fg_color="#181A17")
    etiqueta_titulo = ctk.CTkLabel(window, text="Eliminacion de Jugadores", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)
    ingreso_nickname = ctk.CTkEntry(window, width=200, placeholder_text="Ingresa el nickname del jugador a eliminar")
    ingreso_nickname.pack(pady=5)
    boton_eliminar = ctk.CTkButton(window, text="Eliminar", fg_color="#C90A0A", command=lambda: ejecutar_eliminacion(ingreso_nickname))
    boton_eliminar.pack(pady=8)
    btn_regresar = ctk.CTkButton(window, text="Regresar al Menú Principal", fg_color="#0A319C", command=lambda: regresar(window))
    btn_regresar.pack(pady=8)
    window.mainloop()


def ejecutar_eliminacion(ingreso_nickname):
    nickname = ingreso_nickname.get()
    
    if not nickname:
        messagebox.showwarning("Campo vacío", "Por favor, ingrese el nickname del jugador a eliminar.")
        return

    if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de que desea eliminar al jugador '{nickname}'?"):
        return

    exito, mensaje = eliminar_jugador_db(nickname)
    
    if exito:
        messagebox.showinfo("Éxito", mensaje)
        ingreso_nickname.delete(0, "end")
    else:
        messagebox.showerror("Error", mensaje)