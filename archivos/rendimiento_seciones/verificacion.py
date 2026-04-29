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
    ventana.configure(fg_color="#000000")

    # ===================== FONDO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo9.webp")

        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        def actualizar(event=None):
            w = ventana.winfo_width()
            h = ventana.winfo_height()

            if w < 100 or h < 100:
                return

            resized = img_fondo.resize((w, h))
            img = CTkImage(light_image=resized, size=(w, h))

            ventana._bg_ref = img
            fondo_lbl.configure(image=img)
            fondo_lbl.lower()
            card.lift()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=430,
        height=480,
        corner_radius=24,
        fg_color="#000000",
        border_width=1,
        border_color="#1E4080"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

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
    av.pack(pady=(24, 8))
    av.pack_propagate(False)

    ctk.CTkLabel(
        av,
        text="🏊",
        font=("Arial", 32),
        fg_color="transparent"
    ).place(relx=0.5, rely=0.5, anchor="center")

    # ===================== TITULO =====================
    ctk.CTkLabel(
        cnt,
        text="Verificación Médica",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#0072FF").pack(fill="x", padx=28, pady=10)

    # ===================== INPUT =====================
    e_codigo = ctk.CTkEntry(
        cnt,
        placeholder_text="Código del nadador",
        width=340,
        height=42,
        font=ctk.CTkFont(size=14)
    )
    e_codigo.pack(pady=(10, 6))

    # ===================== RESULTADO =====================
    lbl = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=14))
    lbl.pack(pady=8)

    # ===================== LOGICA VALIDACION =====================
    def validar():
        codigo = e_codigo.get().strip()

        if not codigo:
            lbl.configure(text="⚠️ Ingresa un código", text_color="#F39C12")
            return

        # --- Aquí conectas tu lógica real (BD, lista, etc.) ---
        # Por ahora busca en una lista de ejemplo
        nadadores_lesionados = ["NAD002", "NAD005", "NAD009"]  # reemplaza con tu fuente real

        if codigo in nadadores_lesionados:
            lbl.configure(text="🚫 Lesión activa detectada", text_color="#FF6B6B")
        else:
            lbl.configure(text="✅ Sin lesiones activas", text_color="#1ABC9C")

    # ===================== BOTONES =====================
    ctk.CTkButton(
        cnt,
        text="Validar",
        width=340,
        height=42,
        font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="#0072FF",
        hover_color="#005FCC",
        command=validar
    ).pack(pady=(4, 10))

    ctk.CTkButton(
        cnt,
        text="📋 Registrar sesión",
        width=340,
        height=42,
        fg_color="#1ABC9C",
        hover_color="#17A589",
        command=lambda: [ventana.destroy(), interfaz_registro_sesion(root)]
    ).pack(pady=5)

    ctk.CTkButton(
        cnt,
        text="Cerrar",
        width=340,
        height=42,
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(pady=(5, 20))

    ventana.mainloop()