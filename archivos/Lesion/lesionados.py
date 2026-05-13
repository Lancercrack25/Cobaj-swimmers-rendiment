import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.lesiones import registrar_lesion
from archivos.Terapias_reabilitacion.terapia import interfaz_registrar_terapia
from Backend.funcionamiento_logica_modulos.nadadores import buscar_nadador_por_codigo_global

def _aplicar_fondo(ventana, card=None):
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
            ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=ventana._bg_img)
            fondo_lbl.lower()
            if card:
                card.lift()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)

    except Exception as e:
        print("Error fondo:", e)


def interfaz_registrar_lesion(root, nadador_id=None):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Registrar Lesión")
    ventana.geometry("520x660")
    ventana.configure(fg_color="#0A1628")

    card = ctk.CTkFrame(
        ventana,
        width=440,
        height=610,
        corner_radius=24,
        fg_color="#080808"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    _aplicar_fondo(ventana, card)

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
    entries = {}

    def campo(texto, key):
        ctk.CTkLabel(cnt, text=texto, text_color="#7BA7C7").pack(fill="x")
        e = ctk.CTkEntry(cnt, placeholder_text=texto)
        e.pack(fill="x", pady=5)
        entries[key] = e

    campo("Código del nadador", "nadador_id")
    campo("Tipo de lesión", "tipo_lesion")
    campo("Fecha de inicio (YYYY-MM-DD)", "fecha_inicio")
    campo("Fecha fin (opcional)", "fecha_fin")
    campo("Observaciones", "observaciones")

    # si viene nadador_id precargado
    if nadador_id:
        entries["nadador_id"].insert(0, str(nadador_id))
        entries["nadador_id"].configure(state="disabled")

    # ================= GRAVEDAD =================
    ctk.CTkLabel(cnt, text="Gravedad", text_color="#7BA7C7").pack(fill="x", pady=(8, 2))

    gravedad = ctk.StringVar(value="leve")
    ctk.CTkSegmentedButton(
        cnt,
        values=["leve", "media", "grave"],
        variable=gravedad
    ).pack(fill="x", pady=5)

    lbl_status = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=12))
    lbl_status.pack(pady=(6, 0))

    # ================= LOGICA =================
    def registrar():
        nid = entries["nadador_id"].get().strip()
        tipo = entries["tipo_lesion"].get().strip()
        fecha_ini = entries["fecha_inicio"].get().strip()
        fecha_fin = entries["fecha_fin"].get().strip() or None
        obs = entries["observaciones"].get().strip() or None
        grav = gravedad.get()

        if not nid or not tipo or not fecha_ini:
            lbl_status.configure(
                text="⚠️ Código, tipo y fecha de inicio son obligatorios",
                text_color="#F39C12"
            )
            return

        try:
            nid_int = str(nid)
        except ValueError:
            lbl_status.configure(text="⚠️ El código debe ser un número", text_color="#F39C12")
            return

        ok, msg = registrar_lesion(
            nadador_id=nid_int,
            tipo=tipo,
            gravedad=grav,
            fecha_inicio=fecha_ini,
            fecha_fin=fecha_fin,
            observaciones=obs
        )

        if not ok:
            lbl_status.configure(text=f"❌ {msg}", text_color="#FF6B6B")
            return

        nadador = buscar_nadador_por_codigo_global(nid_int)
        id_numerico = nadador["id"] if nadador else nid_int

        lbl_status.configure(text="✅ Lesión registrada correctamente", text_color="#1ABC9C")
        talk("Lesión registrada correctamente")

        if grav in ("media", "grave"):
            ventana.after(800, lambda: _ir_a_terapia(id_numerico, grav))
        else:
            ventana.after(1200, ventana.destroy)

    def _ir_a_terapia(nid_int, grav):
        print(f">>> Mandando a terapia con nadador_id: {nid_int}")
        ventana.destroy()
        interfaz_registrar_terapia(root, nadador_id=nid_int)

    # ================= BOTONES =================
    ctk.CTkButton(
        cnt,
        text="Registrar lesión",
        fg_color="#50BE10",
        hover_color="#0DAF43",
        command=registrar
    ).pack(fill="x", pady=10)

    ctk.CTkButton(
        cnt,
        text="Cancelar",
        fg_color="#771111",
        command=ventana.destroy
    ).pack(fill="x")