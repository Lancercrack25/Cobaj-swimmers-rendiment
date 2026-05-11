import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.metricas_rendimiento.estadisticas_globales import global_statistics_interface

def fondo_card(ventana, card):
    try:
        img_fondo = Image.open("Backgrounds/fondo4.webp")
        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        def actualizar(event=None):
            w, h = ventana.winfo_width(), ventana.winfo_height()
            if w < 100 or h < 100:
                return
            resized = img_fondo.resize((w, h))
            ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=ventana._bg_img)
            fondo_lbl.lower()
            card.lift()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)
    except Exception as e:
        print("Error fondo:", e)


# ================= interfaz que puede ver el ENTRENADOR =================
def interfaz_estadisticas(entrenador, root):
    v = ctk.CTkToplevel(root)
    v.title("Cobaj Sports — Estadísticas")
    v.geometry("520x420")
    v.configure(fg_color="#0A1628")

    card = ctk.CTkFrame(v, width=440, height=360, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")
    fondo_card(v, card)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    # Avatar
    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36,
                      fg_color="#D4A030", border_width=2, border_color="#F0C040")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="📊", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Estadísticas",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#D4A030").pack(fill="x", padx=28, pady=10)

    botones_frame = ctk.CTkFrame(cnt, fg_color="transparent")
    botones_frame.pack(fill="x", padx=28)

    ctk.CTkButton(botones_frame, text="📋  Estadística individual",
                  height=44, corner_radius=12, anchor="w",
                  fg_color="#2A2000", hover_color="#D4A030",
                  font=ctk.CTkFont(size=14, weight="bold"),
                  command=lambda: personal_statistics_interface(entrenador, v)
                  ).pack(fill="x", pady=6)

    ctk.CTkButton(botones_frame, text="🌐  Estadísticas globales",
                  height=44, corner_radius=12, anchor="w",
                  fg_color="#1E0A35", hover_color="#9333EA",
                  font=ctk.CTkFont(size=14, weight="bold"),
                  command=lambda: global_statistics_interface(v)
                  ).pack(fill="x", pady=6)

    ctk.CTkFrame(cnt, height=1, fg_color="#1E4080").pack(fill="x", padx=28, pady=(12, 6))

    ctk.CTkButton(cnt, text="Cerrar", height=40, corner_radius=12,
                  fg_color="#2C3E50", hover_color="#1A252F", width=380,
                  command=v.destroy).pack(pady=(0, 20))


# ================= ESTADÍSTICAS INDIVIDUALES  del nadador que podra visualizar el ENTRENADOR =================
def personal_statistics_interface(entrenador, root):
    v = ctk.CTkToplevel(root)
    v.title("Cobaj Sports — Estadística Individual")
    v.geometry("520x420")
    v.configure(fg_color="#0A1628")

    card = ctk.CTkFrame(v, width=440, height=360, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")
    fondo_card(v, card)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36,
                      fg_color="#C7A534", border_width=2, border_color="#F0C040")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="📋", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Estadística Individual",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#C7A534").pack(fill="x", padx=28, pady=10)

    e_codigo = ctk.CTkEntry(cnt, placeholder_text="Código del nadador",
                            height=40, width=360, font=ctk.CTkFont(size=13))
    e_codigo.pack(pady=(0, 10))

    lbl = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=12))
    lbl.pack(pady=(0, 8))

    ctk.CTkButton(cnt, text="📊  Checar estadísticas",
                  height=44, width=360, corner_radius=12,
                  fg_color="#2A2000", hover_color="#C7A534",
                  font=ctk.CTkFont(size=14, weight="bold"),
                  command=lambda: lbl.configure(text="Próximamente...", text_color="#AAB8C2")
                  ).pack(pady=(0, 10))

    ctk.CTkButton(cnt, text="Cerrar", height=40, width=360, corner_radius=12,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=v.destroy).pack(pady=(0, 20))


# ================= ESTADÍSTICAS PERSONALES NADADOR =================
def personal_statistics_interface_swimmer(nadador, root):
    v = ctk.CTkToplevel(root)
    nadador_nombre = nadador["nombre"]
    v.title("Cobaj Sports — Mis Estadísticas")
    v.geometry("520x420")
    v.configure(fg_color="#0A1628")

    card = ctk.CTkFrame(v, width=440, height=360, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")
    fondo_card(v, card)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36,
                      fg_color="#0072FF", border_width=2, border_color="#00C6FF")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="📊", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Mis Estadísticas",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 2))

    ctk.CTkLabel(cnt, text=nadador_nombre,
                 font=ctk.CTkFont(size=13),
                 text_color="#AAB8C2").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#0072FF").pack(fill="x", padx=28, pady=10)

    lbl = ctk.CTkLabel(cnt, text="Próximamente...",
                       font=ctk.CTkFont(size=13), text_color="#AAB8C2")
    lbl.pack(pady=(20, 0))

    ctk.CTkFrame(cnt, height=1, fg_color="#1E4080").pack(fill="x", padx=28, pady=(20, 8))

    ctk.CTkButton(cnt, text="Cerrar", height=40, width=360, corner_radius=12,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=v.destroy).pack(pady=(0, 20))