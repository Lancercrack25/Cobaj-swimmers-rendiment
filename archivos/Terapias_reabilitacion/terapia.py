import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.terapias_rehabilitacion import registrar_rehabilitacion
#esta interfaz se manda a llamar cuando la lesion es media o grave, para registrar la terapia de rehabilitacion que se le asigna al nadador, con el tipo de terapia, tiempo estimado, fecha fin y especificaciones del entrenador
def interfaz_registrar_terapia(root, nadador_id=None):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Registrar Terapia de Rehabilitación")
    ventana.geometry("520x580")
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
            fondo_lbl.lower()
            card.lift()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=420,
        height=520,
        corner_radius=24,
        fg_color="#080808",
        border_width=1,
        border_color="#151516"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.pack(expand=True, fill="both", padx=28, pady=20)

    # ===================== HEADER =====================
    ctk.CTkLabel(
        contenido,
        text="Nueva Terapia",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(10, 4))

    ctk.CTkLabel(
        contenido,
        text="Registro de rehabilitacion del nadador",
        font=ctk.CTkFont(size=12),
        text_color="#AAB8C2"
    ).pack(pady=(0, 12))

    ctk.CTkFrame(contenido, height=2, fg_color="#0072FF").pack(fill="x", pady=(0, 12))

    # ===================== CAMPOS =====================
    def campo(placeholder, precargar=None, disabled=False):
        e = ctk.CTkEntry(contenido, width=340, height=38, placeholder_text=placeholder)
        e.pack(pady=5)
        if precargar:
            e.insert(0, str(precargar))
        if disabled:
            e.configure(state="disabled")
        return e

    e_nadador   = campo("ID del nadador", precargar=nadador_id, disabled=bool(nadador_id))
    e_tipo      = campo("Tipo de terapia (Ej. Fisioterapia)")
    e_tiempo    = campo("Tiempo estimado (dias)")
    e_fecha_fin = campo("Fecha fin (YYYY-MM-DD, opcional)")

    ctk.CTkLabel(
        contenido,
        text="Indicaciones del entrenador",
        text_color="#AAB8C2",
        font=ctk.CTkFont(size=12)
    ).pack(pady=(8, 2))

    txt_especificaciones = ctk.CTkTextbox(contenido, width=340, height=70)
    txt_especificaciones.pack(pady=4)

    lbl_estado = ctk.CTkLabel(contenido, text="", font=ctk.CTkFont(size=12))
    lbl_estado.pack(pady=4)

    # ===================== LOGICA =====================
    def registrar():
        nadador = e_nadador.get().strip()
        tipo    = e_tipo.get().strip()
        tiempo  = e_tiempo.get().strip()
        fecha_fin = e_fecha_fin.get().strip() or None
        especificaciones = txt_especificaciones.get("0.0", "end").strip() or None
        print(f">>> nadador_id en terapia: '{nadador}'")

        if not nadador or not tipo or not tiempo:
            lbl_estado.configure(
                text="⚠️ Completa los campos obligatorios",
                text_color="#F39C12"
            )
            return

        if not tiempo.isdigit():
            lbl_estado.configure(
                text="⚠️ El tiempo debe ser un numero entero",
                text_color="#FF6B6B"
            )
            return

        try:
            ok, msg = registrar_rehabilitacion(
                nadador_id=int(nadador),
                tipo_terapia=tipo,
                tiempo_estimado_dias=int(tiempo),
                especificaciones_entrenador=especificaciones,
                fecha_fin=fecha_fin
            )
        except Exception as e:
            lbl_estado.configure(text=f"❌ Error: {e}", text_color="#FF6B6B")
            return

        if not ok:
            lbl_estado.configure(text=f"❌ {msg}", text_color="#FF6B6B")
            return

        lbl_estado.configure(text="✅ Terapia registrada correctamente", text_color="#1ABC9C")
        talk("Terapia de rehabilitacion registrada correctamente")

        e_tipo.delete(0, "end")
        e_tiempo.delete(0, "end")
        e_fecha_fin.delete(0, "end")
        txt_especificaciones.delete("0.0", "end")

        ventana.after(1500, ventana.destroy)

    # ===================== BOTONES =====================
    ctk.CTkButton(
        contenido,
        text="Registrar terapia",
        width=340,
        height=38,
        fg_color="#0072FF",
        hover_color="#005ACC",
        command=registrar
    ).pack(pady=8)

    ctk.CTkButton(
        contenido,
        text="Cerrar",
        width=340,
        height=36,
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(pady=(0, 10))