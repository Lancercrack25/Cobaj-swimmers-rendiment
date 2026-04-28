#en este archivo se hara la validacion de si el nadador esta lesionado o no en caso de que si mand eun alerta, en caso de que no pues porceda con la interfaz del otro archivo
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Lesion.lesionados import interfaz_registrar_lesion

def interfaz_validar_para_lesion(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Verificación de Lesión")
    ventana.geometry("520x650")
    ventana.resizable(False, False)

    ventana.configure(fg_color="#0A1628")

    # 🔥 IMPORTANTE: asegurar render inicial
    ventana.update_idletasks()

    # ================= FONDO =================
    img_fondo = Image.open("Backgrounds/fondo8.webp")

    fondo_lbl = ctk.CTkLabel(ventana, text="")
    fondo_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

    # 🔥 referencia FUERTE (no se pierde)
    ventana._bg_img = None

    def actualizar(event=None):
        w = ventana.winfo_width()
        h = ventana.winfo_height()

        if w < 10 or h < 10:
            return

        resized = img_fondo.resize((w, h))

        ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
        fondo_lbl.configure(image=ventana._bg_img)

    ventana.bind("<Configure>", actualizar)
    ventana.after(50, actualizar)

    # 🔥 FORZAR que el fondo quede atrás DESPUÉS de todo render
    ventana.after(100, fondo_lbl.lower)

    # ================= UI PRINCIPAL =================
    card = ctk.CTkFrame(
        ventana,
        width=430,
        height=600,
        corner_radius=24,
        fg_color="#0F2040DD"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    card.lift()  # 🔥 CLAVE REAL

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.pack(expand=True, fill="both", padx=28, pady=24)

    # ================= CONTENIDO =================
    ctk.CTkLabel(
        cnt,
        text="¿Ya tiene una lesión?",
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=10)

    e_codigo = ctk.CTkEntry(cnt, placeholder_text="Código del nadador")
    e_codigo.pack(fill="x", pady=10)

    lbl_resultado = ctk.CTkLabel(cnt, text="")
    lbl_resultado.pack(pady=5)

    res_card = ctk.CTkFrame(cnt, fg_color="#0A1A0A", corner_radius=12)

    lbl_res = ctk.CTkLabel(res_card, text="")
    lbl_res.pack(pady=5)

    lbl_det = ctk.CTkLabel(res_card, text="")
    lbl_det.pack(pady=5)

    def verificar():
        codigo = e_codigo.get().strip()

        if not codigo:
            lbl_resultado.configure(text="Ingresa código válido", text_color="orange")
            return

        lesionados = {"NAD-001", "NAD-002"}

        res_card.pack_forget()

        if codigo in lesionados:
            lbl_resultado.configure(text="Lesión detectada", text_color="red")
            res_card.pack(fill="x", pady=10)
            lbl_res.configure(text="⚠️ Lesión activa")
            lbl_det.configure(text="Debe registrar lesión")

            ventana.after(800, lambda: (ventana.destroy(), interfaz_registrar_lesion(root)))

        else:
            lbl_resultado.configure(text="Sin lesiones", text_color="#1ABC9C")
            res_card.pack(fill="x", pady=10)
            lbl_res.configure(text="✔ Sin lesiones")
            lbl_det.configure(text="Puede continuar")

    ctk.CTkButton(cnt, text="Verificar", command=verificar).pack(pady=10)
    ctk.CTkButton(cnt, text="Cerrar", command=ventana.destroy).pack(pady=5)

    ventana.mainloop()


