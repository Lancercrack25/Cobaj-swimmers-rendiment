import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from Backend.asistente import talk

def interfaz_estadisticas():
    ventana = ctk.CTk()
    ventana.title("Estadisticas nadadores")
    ventana.geometry("400x420")
    ventana.configure(fg_color="#23303B")

    etiqueta_titulo = ctk.CTkLabel(ventana, text="Estadísticas del Nadador", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    boton_checar = ctk.CTkButton(ventana, text="Checar estadística individual", fg_color="#9C4C0A", command=lambda: personal_statistics_interface())
    boton_checar.pack(pady=8)

    boton_global = ctk.CTkButton(ventana, text="Estadisticas globales", fg_color="#C9BD10", command=lambda: global_statistics_interface())
    boton_global.pack(pady=8)

    boton_cerrar = ctk.CTkButton(ventana, text="Regresar", fg_color="#C91010", command=lambda: ventana.destroy())
    boton_cerrar.pack(pady=8)

    ventana.mainloop()

#esta interfaz podra el entrenador checar las estadisticas personales de uno de sus nadadores
def personal_statistics_interface():
    ventana = ctk.CTk()
    ventana.title("Estadisticas personales de mis nadadores")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#212324")
    etiqueta_titulo = ctk.CTkLabel(ventana, text=" Estadísticas individuales", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    input_nickname = ctk.CTkEntry(ventana, width=200, placeholder_text="Ingresa el codigo del nadador")
    input_nickname.pack(pady=5)

    boton_checar = ctk.CTkButton(ventana, text="Checar estadísticas", fg_color="#C7A534")
    boton_checar.pack(pady=8)
    
    ventana.mainloop()

#esta interfaz sera vista por el nadador en su seccion d estadisticas una vez precione el boton de consultar mis estadisticas, aqui podra checar sus estadisticas personales, como sus tiempos, su progreso, etc.
def personal_statistics_interface_swimmer():
    ventana = ctk.CTk()
    ventana.title("Mis estadísticas")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#212324")
    etiqueta_titulo = ctk.CTkLabel(ventana, text="Mis estadísticas", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    input_nickname = ctk.CTkEntry(ventana, width=200, placeholder_text="Ingresa el codigo del nadador")
    input_nickname.pack(pady=5)

    boton_checar = ctk.CTkButton(ventana, text="Checar estadísticas", fg_color="#C7A534")
    boton_checar.pack(pady=8)
    ventana.mainloop()

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