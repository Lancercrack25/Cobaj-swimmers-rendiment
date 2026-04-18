import customtkinter as ctk
from tkinter import messagebox
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage

def global_statistics_interface():
    ventana = ctk.CTk()
    ventana.title("Estadisticas globales")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#212324")
    etiqueta_titulo = ctk.CTkLabel(ventana, text="Estadísticas globales", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    input_nickname = ctk.CTkEntry(ventana, width=200, placeholder_text="Ingrese el nombre del Entrenador")
    input_nickname.pack(pady=5)

    boton_checar = ctk.CTkButton(ventana, text="Checar estadísticas globales", fg_color="#C7A534")
    boton_checar.pack(pady=8)
    ventana.mainloop()