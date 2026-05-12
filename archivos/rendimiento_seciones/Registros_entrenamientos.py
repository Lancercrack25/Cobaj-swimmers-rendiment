#en este archivo el entrenador podra registrar los entrenamientos de cada nadador, aqui se podran agregar los tiempos de cada nadador, la fecha del entrenamiento, el tipo de entrenamiento, etc. es como un registro de entrenamientos para cada nadador
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import buscar_nadador_por_codigo_global
from Backend.funcionamiento_logica_modulos.sesiones import crear_sesion
from Backend.funcionamiento_logica_modulos.metricas import registrar_rendimiento
#aqui ya se registra la secion para que se mande a la tabla de rendimiento, la cual se encargara de realizar las metricas de cada nadador o de todos.
def interfaz_registro_sesion(root, codigo_nadador, entrenador):
    ventana = ctk.CTkToplevel(root)
    entrenador_id = entrenador["id"]

    ventana.title("Cobaj Sports — Registrar Sesión")
    ventana.geometry("520x720")
    ventana.configure(fg_color="#0A1628")
    ventana.update()

    # ===================== FONDO =====================
    img_fondo = Image.open("Backgrounds/fondo7.webp")

    fondo_lbl = ctk.CTkLabel(ventana, text="")
    fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    # ===================== CARD =====================
    card = ctk.CTkFrame(
        ventana,
        width=450,
        height=670,
        corner_radius=24,
        fg_color="#0F2040"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.pack(expand=True, fill="both", padx=28, pady=22)

    # ===================== ACTUALIZAR FONDO =====================
    def actualizar(event=None):
        ventana.update_idletasks()
        w, h = ventana.winfo_width(), ventana.winfo_height()
        if w < 100 or h < 100:
            ventana.after(100, actualizar)
            return
        resized = img_fondo.resize((w, h))
        ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
        fondo_lbl.configure(image=ventana._bg_img)
        fondo_lbl.lower()
        card.lift()

    ventana.bind("<Configure>", actualizar)
    ventana.after(300, actualizar)

    # ===================== UI =====================
    ctk.CTkLabel(
        cnt,
        text="Registrar Sesión",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#E8F4FD"
    ).pack(pady=(0, 5))

    ctk.CTkLabel(
        cnt,
        text=f"Nadador: {codigo_nadador}",
        font=ctk.CTkFont(size=13),
        text_color="#94a3b8"
    ).pack(pady=(0, 15))

    e_fecha = ctk.CTkEntry(cnt, placeholder_text="Fecha (YYYY-MM-DD)")
    e_fecha.pack(fill="x", pady=5)

    e_tipo = ctk.CTkEntry(cnt, placeholder_text="Tipo de sesión")
    e_tipo.pack(fill="x", pady=5)

    e_desc = ctk.CTkEntry(cnt, placeholder_text="Descripción")
    e_desc.pack(fill="x", pady=5)

    e_dist = ctk.CTkEntry(cnt, placeholder_text="Distancia (m)")
    e_dist.pack(fill="x", pady=5)

    e_tiempo = ctk.CTkEntry(cnt, placeholder_text="Tiempo (seg)")
    e_tiempo.pack(fill="x", pady=5)

    lbl_status = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=12))
    lbl_status.pack(pady=5)

    def guardar():
        fecha = e_fecha.get().strip()
        tipo = e_tipo.get().strip()
        desc = e_desc.get().strip()
        dist = e_dist.get().strip()
        tiempo = e_tiempo.get().strip()

        if not all([fecha, tipo, desc, dist, tiempo]):
            lbl_status.configure(text="⚠️ Llena todos los campos", text_color="#F39C12")
            return

        nadador = buscar_nadador_por_codigo_global(codigo_nadador)
        if not nadador:
            lbl_status.configure(text="❌ Nadador no encontrado", text_color="#FF6B6B")
            return

        try:
            # 1. Intentar crear la sesión general
            ok_s, res_s = crear_sesion(entrenador_id, fecha, tipo, desc)
            if not ok_s:
                lbl_status.configure(text=f"❌ {res_s}", text_color="#FF6B6B")
                return
            
            sesion_id = res_s # Ahora devuelve el ID numérico

            # 2. Registrar el rendimiento específico del nadador
            ok_r, msg_r = registrar_rendimiento(nadador["id"], sesion_id, float(dist), float(tiempo))
            if ok_r:
                lbl_status.configure(text="✅ Registrado correctamente", text_color="#1ABC9C")
                talk("Entrenamiento guardado con éxito")
                ventana.after(1500, ventana.destroy)
            else:
                lbl_status.configure(text=f"❌ {msg_r}", text_color="#FF6B6B")
        except ValueError:
            lbl_status.configure(text="❌ Distancia y tiempo deben ser números", text_color="#FF6B6B")

    ctk.CTkButton(
        cnt,
        text="Guardar sesión",
        fg_color="#0072FF",
        hover_color="#005FCC",
        command=guardar
    ).pack(pady=15, fill="x")

    ctk.CTkButton(
        cnt,
        text="Cancelar",
        fg_color="#2C3E50",
        hover_color="#1A252F",
        command=ventana.destroy
    ).pack(fill="x")