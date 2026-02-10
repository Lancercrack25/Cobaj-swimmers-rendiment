import customtkinter as ctk
from tkinter import messagebox
from interface_stadistics import regresar
from Backend.database import registrar_racha_db
from Backend.asistente import talk
    
def validar_campos(nickname, victorias, derrotas):
    if not nickname or not victorias or not derrotas:
        messagebox.showerror("Error de Validación", "Todos los campos son obligatorios.")
        return False
    if not victorias.isdigit() or not derrotas.isdigit():
        messagebox.showerror("Error de Validación", "Victorias y derrotas deben ser números enteros.")
        return False
    return True

def ejecutar_registro(entry_nickname, entry_victorias, entry_derrotas):
    nickname = entry_nickname.get()
    victorias = entry_victorias.get()
    derrotas = entry_derrotas.get()
    
    if validar_campos(nickname, victorias, derrotas):
        exito, mensaje = registrar_racha_db(nickname, victorias, derrotas)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            entry_nickname.delete(0, "end")
            entry_victorias.delete(0, "end")
            entry_derrotas.delete(0, "end")
        else:
            messagebox.showerror("Error", mensaje)

def registros_rachas():
    windows = ctk.CTk()
    windows.title("Registro de Rachas")
    windows.geometry("450x450")
    windows.configure(fg_color="#726253")

    etiqueta_titulo = ctk.CTkLabel(windows, text="Registro de Rachas de Victorias/Derrotas", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    ingreso_nickname = ctk.CTkEntry(windows, width=200, placeholder_text="Ingresa el nickname del jugador")
    ingreso_nickname.pack(pady=5)

    victorias = ctk.CTkEntry(windows, width=200, placeholder_text="Número de victorias")
    victorias.pack(pady=5)

    derrotas = ctk.CTkEntry(windows, width=200, placeholder_text="Número de derrotas")
    derrotas.pack(pady=5)

    boton_registrar = ctk.CTkButton(windows, text="Registrar", fg_color="#1A1D18", command=lambda: ejecutar_registro(ingreso_nickname, victorias, derrotas))
    boton_registrar.pack(pady=20)

    regresar_menu = ctk.CTkButton(windows, text="Regresar al Menú Principal", fg_color="#9C1D8B", command=lambda: regresar(windows))
    regresar_menu.pack(pady=10)

    windows.mainloop()
