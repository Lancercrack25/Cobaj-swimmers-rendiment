#en este archivo el entrenador podra registrar los entrenamientos de cada nadador, aqui se podran agregar los tiempos de cada nadador, la fecha del entrenamiento, el tipo de entrenamiento, etc. es como un registro de entrenamientos para cada nadador
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import buscar_nadador_por_codigo_global

import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import buscar_nadador_por_codigo_global

def interfaz_registro_sesion(root, codigo_nadador):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Registrar Sesión")
    ventana.geometry("520x720")
    ventana.configure(fg_color="#0A1628")
    ventana.update()

    # ===================== FONDO =====================
    img_fondo = Image.open("Backgrounds/fondo7.webp")

    fondo_lbl = ctk.CTkLabel(ventana, text="")
    fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=450,
        height=670,
        corner_radius=24,
        fg_color="#0F2040"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.pack(expand=True, fill="both", padx=28, pady=22)

    # ===================== ACTUALIZAR FONDO =====================
    def actualizar(event=None):
        ventana.update_idletasks()
        w, h = ventana.winfo_width(), ventana.winfo_height()
        if w < 100 or h < 100:
            ventana.after(100, actualizar)
            return
        resized = img_fondo.resize((w, h))
        ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
        fondo_lbl.configure(image=ventana._bg_img)
        fondo_lbl.lower()
        card.lift()

    ventana.bind("<Configure>", actualizar)
    ventana.after(300, actualizar)

    # ===================== UI =====================
    ctk.CTkLabel(
        cnt,
        text="Registrar Sesión",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(0, 5))

    ctk.CTkLabel(
        cnt,
        text=f"Nadador: {codigo_nadador}",
        font=ctk.CTkFont(size=13),
        text_color="#94a3b8"
    ).pack(pady=(0, 15))

    e_fecha = ctk.CTkEntry(cnt, placeholder_text="Fecha (YYYY-MM-DD)")
    e_fecha.pack(fill="x", pady=5)

    e_tipo = ctk.CTkEntry(cnt, placeholder_text="Tipo de sesión")
    e_tipo.pack(fill="x", pady=5)

    e_desc = ctk.CTkEntry(cnt, placeholder_text="Descripción")
    e_desc.pack(fill="x", pady=5)

    e_dist = ctk.CTkEntry(cnt, placeholder_text="Distancia (m)")
    e_dist.pack(fill="x", pady=5)

    e_tiempo = ctk.CTkEntry(cnt, placeholder_text="Tiempo (seg)")
    e_tiempo.pack(fill="x", pady=5)

    ctk.CTkButton(
        cnt,
        text="Guardar sesión",
        fg_color="#0072FF",
        hover_color="#005FCC"
    ).pack(pady=15, fill="x")

    ctk.CTkButton(
        cnt,
        text="Cancelar",
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(fill="x")