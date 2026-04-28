#aqui se crea la interfaz y la logica de la validacion de si un nadador esta lesionado o no, en caso de que no se manda a llamar la interfaz del otro archivo
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.rendimiento_seciones.Registros_entrenamientos import interfaz_registro_sesion

def interfaz_validar_lesion(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Verificación Médica")
    ventana.geometry("520x650")
    ventana.resizable(False, False)
    ventana.configure(fg_color="#0A1628")

    # ===================== FONDO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo9.webp")

        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_lbl.lower()

        def actualizar(event=None):
            w = ventana.winfo_width()
            h = ventana.winfo_height()

            if w < 100 or h < 100:
                return

            resized = img_fondo.resize((w, h))
            img = CTkImage(light_image=resized, size=(w, h))

            # 🔥 clave para que no desaparezca
            ventana._bg_ref = img

            fondo_lbl.configure(image=img)
            fondo_lbl.lower()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=430,
        height=600,
        corner_radius=24,
        fg_color="#0F2040DD",   # 🔥 IMPORTANTE: semi transparente
        border_width=1,
        border_color="#1E4080"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.pack(expand=True, fill="both", padx=28, pady=24)

    # ===================== AVATAR =====================
    av = ctk.CTkFrame(
        cnt,
        width=72,
        height=72,
        corner_radius=36,
        fg_color="#0072FF",
        border_width=2,
        border_color="#00C6FF"
    )
    av.pack(pady=(0, 8))
    av.pack_propagate(False)

    ctk.CTkLabel(av, text="🏊", font=("Arial", 32),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    # ===================== TITULO =====================
    ctk.CTkLabel(
        cnt,
        text="Verificación Médica",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#0072FF").pack(fill="x", pady=10)

    # ===================== INPUT =====================
    e_codigo = ctk.CTkEntry(
        cnt,
        placeholder_text="Código del nadador"
    )
    e_codigo.pack(fill="x", pady=10)

    lbl = ctk.CTkLabel(cnt, text="")
    lbl.pack(pady=10)

    # ===================== BOTONES =====================
    def libre():
        lbl.configure(text="Sin lesiones activas", text_color="#1ABC9C")

    def lesion():
        lbl.configure(text="Lesión activa detectada", text_color="#FF6B6B")

    ctk.CTkButton(cnt, text="Simular libre", command=libre).pack(pady=5)
    ctk.CTkButton(cnt, text="Simular lesión", command=lesion).pack(pady=5)

    ctk.CTkButton(
        cnt,
        text="📋 Registrar sesión",
        command=lambda: [ventana.destroy(), interfaz_registro_sesion(root)]
    ).pack(pady=10)

    ctk.CTkButton(cnt, text="Cerrar", command=ventana.destroy).pack()

    ventana.mainloop()