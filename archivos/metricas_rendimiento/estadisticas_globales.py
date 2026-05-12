import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.metricas import obtener_estadisticas_globales
from Backend.funcionamiento_logica_modulos.nadadores import obtener_nadadores

def global_statistics_interface(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Estadísticas globales")
    ventana.geometry("520x500")

    # ===================== FONDO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo7.webp")
        bg_ref = [None]

        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_lbl.lower()

        def actualizar(event=None):
            w, h = ventana.winfo_width(), ventana.winfo_height()
            if w < 100 or h < 100:
                return
            resized = img_fondo.resize((w, h))
            bg_ref[0] = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=bg_ref[0])
            fondo_lbl.lower()
            card.lift()  # ← sube el card

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=440,
        height=420,
        corner_radius=24,
        fg_color="#080808",
        border_width=1,
        border_color="#151516"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ===================== CONTENIDO =====================
    ctk.CTkLabel(
        contenido,
        text="Estadísticas Globales",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(30, 10))

    ctk.CTkLabel(
        contenido,
        text="Consulta el rendimiento general del equipo",
        font=ctk.CTkFont(size=12),
        text_color="#AAB8C2"
    ).pack(pady=(0, 15))

    input_nickname = ctk.CTkEntry(
        contenido,
        width=340,
        height=38,
        placeholder_text="Nombre del entrenador"
    )
    input_nickname.pack(pady=5)

    lbl_estado = ctk.CTkLabel(
        contenido,
        text="",
        font=ctk.CTkFont(size=12)
    )
    lbl_estado.pack(pady=8)

    # ===================== RESULTADOS =====================
    resultado_frame = ctk.CTkFrame(contenido, fg_color="#0A1A2A", corner_radius=12, border_width=1, border_color="#1E4080")
    lbl_resultado = ctk.CTkLabel(resultado_frame, text="", font=ctk.CTkFont(size=13), text_color="#E8F4FD", justify="left")
    lbl_resultado.pack(padx=16, pady=12)

    def consultar():
        nombre = input_nickname.get().strip()

        if not nombre:
            lbl_estado.configure(text="⚠️ Ingresa un nombre", text_color="orange")
            resultado_frame.pack_forget()
            return

        estadisticas = obtener_estadisticas_globales(nombre)

        if not estadisticas:
            lbl_estado.configure(text=f"Sin datos para: {nombre}", text_color="#FF6B6B")
            resultado_frame.pack_forget()
            return

        lbl_estado.configure(text=f"✅ Estadísticas de {nombre}", text_color="#1ABC9C")

        texto = (
            f"Total sesiones: {estadisticas.get('total_sesiones', 0)}\n"
            f"Total nadadores: {estadisticas.get('total_nadadores', 0)}\n"
            f"Distancia promedio: {estadisticas.get('distancia_promedio', 0):.2f} m\n"
            f"Tiempo promedio: {estadisticas.get('tiempo_promedio', 0):.2f} seg\n"
            f"Ritmo promedio: {estadisticas.get('ritmo_promedio', 0):.4f}"
        )

        lbl_resultado.configure(text=texto)
        resultado_frame.pack(fill="x", padx=28, pady=6)
        
        # Botón opcional para ver comparativa visual
        if estadisticas.get('total_nadadores', 0) > 0:
            btn_grafica_global.pack(pady=5)

    def mostrar_grafica_global():
        nombre = input_nickname.get().strip()
        est = obtener_estadisticas_globales(nombre)
        
        v_g = ctk.CTkToplevel(ventana)
        v_g.title("Gráfica de Promedios del Equipo")
        v_g.geometry("600x400")
        
        # Gráfica de barras para promedios globales
        fig, ax = plt.subplots(figsize=(5, 3))
        fig.patch.set_facecolor('#080808')
        ax.set_facecolor('#0A1A2A')
        
        labels = ['Distancia (m)', 'Tiempo (s)', 'Ritmo (s/m)']
        valores = [est['distancia_promedio'], est['tiempo_promedio'], est['ritmo_promedio'] * 100] # Escalado para visibilidad
        ax.bar(labels, valores, color=['#0072FF', '#1ABC9C', '#F39C12'])
        ax.set_title(f"Promedios de Equipo - Entrenador {nombre}", color="white")
        
        canvas = FigureCanvasTkAgg(fig, master=v_g)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    ctk.CTkButton(
        contenido,
        text="Consultar estadísticas",
        width=340,
        height=38,
        fg_color="#0072FF",
        hover_color="#005ACC",
        command=consultar
    ).pack(pady=6)

    btn_grafica_global = ctk.CTkButton(
        contenido,
        text="📊 Ver Gráfica Comparativa",
        width=340,
        height=38,
        fg_color="#1ABC9C",
        command=mostrar_grafica_global
    )

    ctk.CTkButton(
        contenido,
        text="Cerrar",
        width=340,
        height=36,
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(pady=(0, 20))