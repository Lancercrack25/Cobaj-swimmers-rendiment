import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from archivos.Lesion.verificacion_lesionados import interfaz_validar_para_lesion
from archivos.Lesion.historial_gestionamiento import interfaz_historial_lesiones
from archivos.Terapias_reabilitacion.historial_gestion_terapia import interfaz_historial_terapias
#aqui sera un submenu en el cual el nadador podra registrar sus lesiones,ver su historial y finalizar sus lesiones asi como tambien ver el historial de sus terapias

def interfaz_gestion_salud(root, nadador):
    nadador_id = nadador["id"]
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Gestión Médica")
    ventana.geometry("520x620")
    ventana.resizable(False, False)
    ventana.configure(fg_color="#0A1628")

    # ===================== FONDO DINÁMICO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo10.webp")
        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        def actualizar(event=None):
            w, h = ventana.winfo_width(), ventana.winfo_height()
            if w < 100 or h < 100: return
            resized = img_fondo.resize((w, h))
            ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=ventana._bg_img)
            fondo_lbl.lower()
            card.lift()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)
    except Exception as e:
        print("Error fondo:", e)

    # ===================== TARJETA DE CONTROL =====================
    card = ctk.CTkFrame(ventana, width=420, height=540, corner_radius=28,
                        fg_color="#0F2040", border_width=2, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    # ===================== ENCABEZADO ICONOGRÁFICO =====================
    header_icon = ctk.CTkFrame(cnt, width=80, height=80, corner_radius=40,
                               fg_color="#1ABC9C", border_width=3, border_color="#16A085")
    header_icon.pack(pady=(40, 10))
    header_icon.pack_propagate(False)
    ctk.CTkLabel(header_icon, text="⚕️", font=("Arial", 38),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Panel de Bienestar",
                 font=ctk.CTkFont(size=24, weight="bold"),
                 text_color="#E8F4FD").pack()

    ctk.CTkLabel(cnt, text="Control de lesiones y rehabilitación",
                 font=ctk.CTkFont(size=13), text_color="#7BA7C7").pack(pady=(0, 20))

    # ===================== BOTONES DE ACCIÓN =====================
    # Tupla: (Texto, Color Base, Color Hover, Función)
    menu_items = [
        ("🩹  Registrar Lesión", "#C0392B", "#E74C3C", lambda: interfaz_validar_para_lesion(ventana)),
        ("📜  Historial de Lesiones",  "#1E4080", "#2980B9", lambda: interfaz_historial_lesiones(ventana, nadador_id)),
        ("🏥  Seguimiento de Terapias","#16A085", "#1ABC9C", lambda: interfaz_historial_terapias(ventana, nadador_id))
    ]

    for txt, col, hov, cmd in menu_items:
        ctk.CTkButton(
            cnt, text=txt, height=55, width=320, corner_radius=16,
            fg_color=col, hover_color=hov, text_color="white",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=cmd
        ).pack(pady=10)

    # ===================== PIE DE VENTANA =====================
    ctk.CTkButton(cnt, text="Volver al Menú Principal", 
                  width=320, height=45, corner_radius=16,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  font=ctk.CTkFont(size=13),
                  command=ventana.destroy).pack(pady=(35, 0))

    talk("Abriendo panel de bienestar. Tu salud es nuestra prioridad.")