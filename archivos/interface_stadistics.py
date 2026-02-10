import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from Backend.database import obtener_rachas_jugador
from Backend.asistente import talk

def interfaz_estadisticas():
    ventana = ctk.CTk()
    ventana.title("Estadisticas de Jugadores")
    ventana.geometry("400x420")
    ventana.configure(fg_color="#23303B")

    etiqueta_titulo = ctk.CTkLabel(ventana, text="Estadísticas de Jugadores", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    ingreso_nickname = ctk.CTkEntry(ventana, width=200, placeholder_text="Ingrese el nickname del jugador")
    ingreso_nickname.pack(pady=5)

    boton_checar = ctk.CTkButton(ventana, text="Checar Estadísticas", fg_color="#9C4C0A", command=lambda: stadistics(ingreso_nickname.get()))
    boton_checar.pack(pady=8)

    boton_cerrar = ctk.CTkButton(ventana, text="Regresar", fg_color="#C91010", command=lambda: regresar(ventana))
    boton_cerrar.pack(pady=8)

    ventana.mainloop()

def regresar(ventana):
    talk("Regresando al menú principal.")
    ventana.destroy()

def stadistics(nickname):
    if not nickname:
        talk("Ingresa un nickname para que pueda buscar las estadísticas porfavor.")
        messagebox.showwarning("Campo Vacío", "Por favor, ingresa un nickname para buscar.")
        return
    try:
        resultados, mensaje = obtener_rachas_jugador(nickname)
        
        if resultados is None:
             messagebox.showerror("Error", mensaje)
             return

        if not resultados:
            talk(f"Al parecer no se encontraron registros en la base de datos para el jugador {nickname}.")
            messagebox.showinfo("Sin Datos", f"el jugador '{nickname} no existe en la base de datos'.")
            return
        talk(f"Preparando las estadísticas de {nickname}.")
        # Procesamiento de datos con numpy
        victorias = np.array([fila[0] for fila in resultados])
        derrotas = np.array([fila[1] for fila in resultados])
        fechas = [fila[2].strftime("%Y-%m-%d %H:%M") for fila in resultados]
        indices = np.arange(len(resultados))

        # Generación de la gráfica con matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(indices, victorias, label='Victorias', marker='o', color='green', linestyle='-')
        plt.plot(indices, derrotas, label='Derrotas', marker='x', color='red', linestyle='--')
        
        plt.title(f"Comportamiento de Rachas: {nickname}")
        plt.xlabel("Registro (Cronológico)")
        plt.ylabel("Cantidad")
        plt.xticks(indices, fechas, rotation=45, ha="right")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")
