import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from archivos.metricas_rendimiento.interface_stadistics import personal_statistics_interface_swimmer
from archivos.Nadadores.info_swimer_profile import profile_swimmer
from archivos.Nadadores.interfaz_submenu import interfaz_gestion_salud

def interfaz_nadador(nadador_actual):
    nadador_id = nadador_actual["id"]
    nadador_nombre = nadador_actual["nombre"]
    ventana = ctk.CTk()
    ventana.title("Cobaj Sports — Panel Nadador")
    ventana.geometry("520x600")
    ventana.resizable(False, False)
    ventana.configure(fg_color="#0A1628")

    # ===================== FONDO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo 6.png")
        bg_ref = [None]

        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_lbl.lower()

        def actualizar_fondo(event=None):
            w = ventana.winfo_width()
            h = ventana.winfo_height()
            if w < 100 or h < 100:
                return
            resized = img_fondo.resize((w, h))
            bg_ref[0] = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=bg_ref[0])
            fondo_lbl.lower()

        ventana.bind("<Configure>", actualizar_fondo)
        ventana.after(100, actualizar_fondo)
    except Exception:
        pass

    # ===================== CARD PRINCIPAL =====================
    card = ctk.CTkFrame(
        ventana,
        width=420,
        height=540,
        corner_radius=24,
        fg_color="#0F2040",
        border_width=1,
        border_color="#1E4080"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.pack(expand=True, fill="both", padx=28, pady=24)

    # ===================== AVATAR =====================
    avatar_frame = ctk.CTkFrame(
        contenido,
        width=72,
        height=72,
        corner_radius=36,
        fg_color="#0072FF",
        border_width=2,
        border_color="#00C6FF"
    )
    avatar_frame.pack(pady=(0, 8))
    avatar_frame.pack_propagate(False)

    ctk.CTkLabel(
        avatar_frame,
        text="🏊",
        font=("Arial", 32),
        fg_color="transparent"
    ).place(relx=0.5, rely=0.5, anchor="center")

    # ===================== BIENVENIDA =====================
    ctk.CTkLabel(
        contenido,
        text="Bienvenido,",
        font=ctk.CTkFont(family="Georgia", size=13),
        text_color="#7BA7C7"
    ).pack(pady=(0, 2))

    ctk.CTkLabel(
        contenido,
        text="Menú Principal",
        font=ctk.CTkFont(family="Georgia", size=22, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(0, 4))

    # ===================== LÍNEA DECORATIVA =====================
    ctk.CTkFrame(
        contenido, height=2,
        fg_color="#0072FF",
        corner_radius=2
    ).pack(fill="x", pady=(4, 20))

    ctk.CTkLabel(
        contenido,
        text="¿Qué deseas hacer hoy?",
        font=ctk.CTkFont(family="Georgia", size=13),
        text_color="#7BA7C7"
    ).pack(pady=(0, 16))

    # ===================== BOTONES =====================
    botones = [
        ("👤  Mi perfil",            "#1A3A6B", "#00A8D6", lambda: profile_swimmer(nadador_actual, ventana)),
        ("📊  Mis estadísticas",     "#2A2000", "#D4A030", lambda: personal_statistics_interface_swimmer(nadador_actual, ventana)),
        ("🩹  Mis lesiones y terapia",         "#1E0A35", "#9333EA", lambda: interfaz_gestion_salud(ventana, nadador_actual)),
    ]

    for texto, color, hover, cmd in botones:
        ctk.CTkButton(
            contenido,
            text=texto,
            fg_color=color,
            hover_color=hover,
            text_color="#E8F4FD",
            font=ctk.CTkFont(family="Georgia", size=14, weight="bold"),
            height=48,
            corner_radius=12,
            anchor="w",
            command=cmd
        ).pack(fill="x", pady=6)

    # ===================== SEPARADOR =====================
    ctk.CTkFrame(
        contenido, height=1,
        fg_color="#1E4080",
        corner_radius=1
    ).pack(fill="x", pady=(16, 8))

    # ===================== SALIR =====================
    ctk.CTkButton(
        contenido,
        text="⏻  Cerrar sesión",
        fg_color="#2A0A0A",
        hover_color="#DC2626",
        text_color="#FF8080",
        font=ctk.CTkFont(family="Georgia", size=13),
        height=40,
        corner_radius=12,
        anchor="w",
        command=ventana.destroy
    ).pack(fill="x", pady=(0, 4))

    # ===================== FOOTER =====================
    ctk.CTkLabel(
        contenido,
        text="Cobaj Sports Rendiment • v1.0",
        font=ctk.CTkFont(size=10),
        text_color="#2A4A6A"
    ).pack(pady=(8, 0))

    ventana.mainloop()