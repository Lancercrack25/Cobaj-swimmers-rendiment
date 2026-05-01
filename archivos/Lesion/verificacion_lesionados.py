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
    ventana.configure(fg_color="#000000")
    ventana.update_idletasks()

    try:
        img_fondo = Image.open("Backgrounds/fondo8.webp")
        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

        def actualizar(event=None):
            w = ventana.winfo_width()
            h = ventana.winfo_height()
            if w < 10 or h < 10:
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

    card = ctk.CTkFrame(
        ventana,
        width=430,
        height=500,
        corner_radius=24,
        fg_color="#000000",
        border_width=1,
        border_color="#1E4080"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36, fg_color="#0072FF", border_width=2, border_color="#00C6FF")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="🏊", font=("Arial", 32), fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Verificación de Lesión", font=ctk.CTkFont(size=22, weight="bold"), text_color="#E8F4FD").pack(pady=(0, 4))
    ctk.CTkFrame(cnt, height=2, fg_color="#0072FF").pack(fill="x", padx=28, pady=10)

    e_codigo = ctk.CTkEntry(cnt, placeholder_text="Código del nadador", width=340, height=42, font=ctk.CTkFont(size=14))
    e_codigo.pack(pady=(10, 6))

    lbl_resultado = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=13))
    lbl_resultado.pack(pady=6)

    res_card = ctk.CTkFrame(cnt, fg_color="#0A1A2A", corner_radius=12, border_width=1, border_color="#1E4080")
    lbl_res = ctk.CTkLabel(res_card, text="", font=ctk.CTkFont(size=14, weight="bold"))
    lbl_res.pack(pady=(10, 2))
    lbl_det = ctk.CTkLabel(res_card, text="", font=ctk.CTkFont(size=12), text_color="#AAB8C2")
    lbl_det.pack(pady=(2, 10))

    def verificar():
        codigo = e_codigo.get().strip()

        if not codigo:
            lbl_resultado.configure(text="⚠️ Ingresa un código válido", text_color="#F39C12")
            res_card.pack_forget()
            return

        lbl_resultado.configure(text="📋 Redirigiendo al registro de lesión...", text_color="#22d3ee")
        res_card.pack(fill="x", padx=28, pady=6)
        lbl_res.configure(text=f"Nadador: {codigo}", text_color="#E8F4FD")
        lbl_det.configure(text="¡Es momento de registrar una nueva lesión!")

        # ← solo pasa root, no ventana ni codigo
        ventana.after(800, lambda: interfaz_registrar_lesion(root))

    e_codigo.bind("<Return>", lambda e: verificar())

    ctk.CTkButton(
        cnt,
        text="Verificar y Registrar Lesión",
        width=340,
        height=42,
        font=ctk.CTkFont(size=15, weight="bold"),
        fg_color="#0072FF",
        hover_color="#005FCC",
        command=verificar
    ).pack(pady=(8, 5))

    ctk.CTkButton(
        cnt,
        text="Cerrar",
        width=340,
        height=42,
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(pady=(0, 20))