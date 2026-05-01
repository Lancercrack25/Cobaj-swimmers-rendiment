#esta interfaz se registraran los lesionados, aqui el entrenador podra registrar a un nadador como lesionado
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage

def _aplicar_fondo(ventana):
    try:
        img_fondo = Image.open("Backgrounds/fondo11.webp")

        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_lbl.lower()

        def actualizar(event=None):
            w, h = ventana.winfo_width(), ventana.winfo_height()
            if w < 100 or h < 100:
                return

            resized = img_fondo.resize((w, h))

            # 🔥 CLAVE: guardar referencia en la ventana
            ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=ventana._bg_img)
            fondo_lbl.lower()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)


def interfaz_registrar_lesion(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Registrar Lesión")
    ventana.geometry("520x660")
    ventana.resizable(False, False)
    ventana.configure(fg_color="#0A1628")

    _aplicar_fondo(ventana)

    # ================= CARD =================
    card = ctk.CTkFrame(
        ventana,
        width=440,
        height=610,
        corner_radius=24,
        fg_color="#0F2040DD"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.pack(expand=True, fill="both", padx=28, pady=22)

    # ================= HEADER =================
    ctk.CTkLabel(
        cnt,
        text="Registrar nueva lesión",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(10, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#C0392B").pack(fill="x", pady=(4, 14))

    # ================= CAMPOS =================
    def campo(texto):
        ctk.CTkLabel(cnt, text=texto,
                     text_color="#7BA7C7").pack(fill="x")
        e = ctk.CTkEntry(cnt, placeholder_text=texto)
        e.pack(fill="x", pady=5)
        return e

    campo("Tipo de lesión")
    campo("Fecha de inicio")
    campo("Fecha fin (opcional)")
    campo("Observaciones")

    # ================= GRAVEDAD =================
    ctk.CTkLabel(cnt, text="Gravedad", text_color="#7BA7C7").pack(fill="x", pady=(8, 2))

    gravedad = ctk.StringVar(value="leve")
    ctk.CTkSegmentedButton(
        cnt,
        values=["leve", "media", "grave"],
        variable=gravedad
    ).pack(fill="x", pady=5)

    # ================= BOTONES =================
    ctk.CTkButton(
        cnt,
        text="Registrar lesión",
        fg_color="#50BE10",
        hover_color="#0DAF43"
    ).pack(fill="x", pady=10)

    ctk.CTkButton(
        cnt,
        text="Cancelar",
        fg_color="#771111",
        command=ventana.destroy
    ).pack(fill="x")