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

    etiqueta_titulo = ctk.CTkLabel(ventana, text="Estadísticas de Nadador individual", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    ingreso_nickname = ctk.CTkEntry(ventana, width=200, placeholder_text="Ingrese nombre del nadador")
    ingreso_nickname.pack(pady=5)

    boton_checar = ctk.CTkButton(ventana, text="Checar Estadísticas", fg_color="#9C4C0A")
    boton_checar.pack(pady=8)

    boton_global = ctk.CTkButton(ventana, text="Estadisticas globales", fg_color="#C9BD10")
    boton_global.pack(pady=8)

    boton_cerrar = ctk.CTkButton(ventana, text="Regresar", fg_color="#C91010", command=lambda: ventana.destroy())
    boton_cerrar.pack(pady=8)

    ventana.mainloop()
