#en este archivo el entrenador podra registrar los entrenamientos de cada nadador, aqui se podran agregar los tiempos de cada nadador, la fecha del entrenamiento, el tipo de entrenamiento, etc. es como un registro de entrenamientos para cada nadador
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage

def interfaz_registro_sesion():
    ventana = ctk.CTk()
    ventana.title("Cobaj Sports — Registrar Sesión")
    ventana.geometry("520x720")
    ventana.resizable(False, False)
    ventana.configure(fg_color="#0A1628")

    # ===================== FONDO FIJO =====================
    img_fondo = Image.open("Backgrounds/fondo7.webp")

    fondo_lbl = ctk.CTkLabel(ventana, text="")
    fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
    fondo_lbl.lower()

    def actualizar(event=None):
        w, h = ventana.winfo_width(), ventana.winfo_height()
        if w < 100 or h < 100:
            return

        resized = img_fondo.resize((w, h))

        # 🔥 CLAVE: guardar referencia en la ventana (OBLIGATORIO)
        ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
        fondo_lbl.configure(image=ventana._bg_img)
        fondo_lbl.lower()

    ventana.bind("<Configure>", actualizar)
    ventana.after(100, actualizar)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=450,
        height=670,
        corner_radius=24,
        fg_color="#0F2040DD"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.pack(expand=True, fill="both", padx=28, pady=22)

    # ===================== UI SIMPLE =====================
    ctk.CTkLabel(cnt, text="Registrar sesión",
                 font=ctk.CTkFont(size=20, weight="bold"),
                 text_color="#E8F4FD").pack(pady=10)

    ctk.CTkEntry(cnt, placeholder_text="Fecha (YYYY-MM-DD)").pack(fill="x", pady=5)
    ctk.CTkEntry(cnt, placeholder_text="Tipo de sesión").pack(fill="x", pady=5)
    ctk.CTkEntry(cnt, placeholder_text="Descripción").pack(fill="x", pady=5)

    ctk.CTkEntry(cnt, placeholder_text="Distancia (m)").pack(fill="x", pady=5)
    ctk.CTkEntry(cnt, placeholder_text="Tiempo (seg)").pack(fill="x", pady=5)

    ctk.CTkButton(cnt, text="Guardar sesión").pack(pady=10)
    ctk.CTkButton(cnt, text="Cancelar", command=ventana.destroy).pack()

    ventana.mainloop()