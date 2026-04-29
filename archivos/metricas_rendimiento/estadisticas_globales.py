import customtkinter as ctk
from tkinter import messagebox
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage

def global_statistics_interface(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Estadísticas globales")
    ventana.geometry("520x500")
    ventana.resizable(False, False)

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

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=340,
        height=300,
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
        text="Consulta el rendimiento general",
        font=ctk.CTkFont(size=12),
        text_color="#AAB8C2"
    ).pack(pady=(0, 15))

    input_nickname = ctk.CTkEntry(
        contenido,
        width=220,
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

    def consultar():
        nombre = input_nickname.get().strip()

        if not nombre:
            lbl_estado.configure(text="Ingresa un nombre", text_color="orange")
            return

        # 🔴 Aquí luego conectas tu lógica real
        lbl_estado.configure(text=f"Consultando estadísticas de {nombre}...", text_color="#1ABC9C")

    ctk.CTkButton(
        contenido,
        text="Consultar estadísticas",
        width=220,
        height=38,
        fg_color="#0072FF",
        hover_color="#005ACC",
        command=consultar
    ).pack(pady=6)

    ctk.CTkButton(
        contenido,
        text="Cerrar",
        width=220,
        height=36,
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(pady=(0, 20))