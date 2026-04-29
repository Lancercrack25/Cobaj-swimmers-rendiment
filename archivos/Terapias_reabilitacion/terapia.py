import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage

def interfaz_registrar_terapia(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Registrar Terapia de Rehabilitación")
    ventana.geometry("520x620")
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
        width=360,
        height=520,
        corner_radius=24,
        fg_color="#080808",
        border_width=1,
        border_color="#151516"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ===================== HEADER =====================
    ctk.CTkLabel(
        contenido,
        text="Nueva Terapia",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(25, 5))

    ctk.CTkLabel(
        contenido,
        text="Registro de rehabilitación del nadador",
        font=ctk.CTkFont(size=12),
        text_color="#AAB8C2"
    ).pack(pady=(0, 15))

    # ===================== CAMPOS =====================
    def campo(placeholder):
        e = ctk.CTkEntry(
            contenido,
            width=240,
            height=38,
            placeholder_text=placeholder
        )
        e.pack(pady=6)
        return e

    e_nadador = campo("ID del nadador")
    e_lesion = campo("ID de la lesión")
    e_tipo = campo("Tipo de terapia (Ej. Fisioterapia)")
    e_tiempo = campo("Tiempo estimado (días)")
    e_fecha_fin = campo("Fecha fin (YYYY-MM-DD)")

    # ===================== ESPECIFICACIONES =====================
    ctk.CTkLabel(
        contenido,
        text="Indicaciones del entrenador",
        text_color="#AAB8C2"
    ).pack(pady=(10, 2))

    txt_especificaciones = ctk.CTkTextbox(
        contenido,
        width=240,
        height=80
    )
    txt_especificaciones.pack(pady=5)

    # ===================== MENSAJE =====================
    lbl_estado = ctk.CTkLabel(contenido, text="", font=ctk.CTkFont(size=12))
    lbl_estado.pack(pady=6)

    # ===================== LÓGICA =====================
    def registrar():
        nadador = e_nadador.get().strip()
        lesion = e_lesion.get().strip()
        tipo = e_tipo.get().strip()
        tiempo = e_tiempo.get().strip()

        if not nadador or not lesion or not tipo or not tiempo:
            lbl_estado.configure(text="Completa los campos obligatorios", text_color="orange")
            return

        if not tiempo.isdigit():
            lbl_estado.configure(text="Tiempo debe ser numérico", text_color="red")
            return

        # 🔴 Aquí conectas BD después
        lbl_estado.configure(text="Terapia registrada correctamente", text_color="green")

        # limpiar
        e_nadador.delete(0, "end")
        e_lesion.delete(0, "end")
        e_tipo.delete(0, "end")
        e_tiempo.delete(0, "end")
        e_fecha_fin.delete(0, "end")
        txt_especificaciones.delete("0.0", "end")

    # ===================== BOTONES =====================
    ctk.CTkButton(
        contenido,
        text="Registrar terapia",
        width=240,
        height=38,
        fg_color="#0072FF",
        hover_color="#005ACC",
        command=registrar
    ).pack(pady=8)

    ctk.CTkButton(
        contenido,
        text="Cerrar",
        width=240,
        height=36,
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(pady=(0, 20))