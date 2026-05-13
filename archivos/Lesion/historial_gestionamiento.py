import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.lesiones import obtener_historial_lesiones,finalizar_lesion
#aqui se vera el historial de la slesiones del nadador, con la opcion de finalizar cada una de ellas

def interfaz_historial_lesiones(root, nadador_id):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Cobaj Sports — Historial de Lesiones")
    ventana.geometry("600x650")
    ventana.configure(fg_color="#0A1628")

    # ===================== FONDO DINÁMICO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo10.webp")
        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        def actualizar(event=None):
            w, h = ventana.winfo_width(), ventana.winfo_height()
            if w < 100 or h < 100:
                return
            resized = img_fondo.resize((w, h))
            ventana._bg_img = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=ventana._bg_img)
            fondo_lbl.lower()
            card.lift()

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)
    except Exception as e:
        print("Error al cargar fondo:", e)

    # ===================== TARJETA CENTRAL =====================
    card = ctk.CTkFrame(ventana, width=540, height=580, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    # ===================== ENCABEZADO =====================
    av = ctk.CTkFrame(cnt, width=64, height=64, corner_radius=32,
                      fg_color="#C0392B", border_width=2, border_color="#E74C3C")
    av.pack(pady=(30, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="🩹", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Historial Médico",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#C0392B").pack(fill="x", padx=40, pady=10)

    # ===================== LISTA DE LESIONES =====================
    lista_frame = ctk.CTkScrollableFrame(cnt, fg_color="#0A1A2A", corner_radius=12,
                                         border_width=1, border_color="#1E4080", height=320)
    lista_frame.pack(fill="x", padx=30, pady=(10, 10))

    def render_historial():
        # Limpiar la lista antes de re-dibujar
        for w in lista_frame.winfo_children():
            w.destroy()

        historial = obtener_historial_lesiones(nadador_id)

        if not historial:
            ctk.CTkLabel(lista_frame, text="No hay registros de lesiones",
                         text_color="#AAB8C2", font=ctk.CTkFont(size=14)).pack(pady=40)
            return

        for les in historial:
            row = ctk.CTkFrame(lista_frame, fg_color="#132440", corner_radius=10)
            row.pack(fill="x", pady=5, padx=5)

            # Texto de información
            info_text = f"🔹 {les['tipo_lesion'].upper()} ({les['gravedad']})\n"
            info_text += f"📅 {les['fecha_inicio']} a " + (str(les['fecha_fin']) if les['fecha_fin'] else "Actualidad")
            
            estado_color = "#1ABC9C" if not les['activo'] else "#F39C12"
            estado_txt = "✅ Recuperado" if not les['activo'] else "⚠️ En tratamiento"

            txt_frame = ctk.CTkFrame(row, fg_color="transparent")
            txt_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            ctk.CTkLabel(txt_frame, text=info_text, font=ctk.CTkFont(size=13),
                         text_color="#E8F4FD", justify="left").pack(anchor="w")
            
            ctk.CTkLabel(txt_frame, text=estado_txt, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=estado_color).pack(anchor="w")

            # Botón para finalizar si está activa
            if les['activo']:
                def finalizar(lid=les['id'], tipo=les['tipo_lesion']):
                    ok, msg = finalizar_lesion(lid)
                    if ok:
                        talk(f"Lesión de {tipo} finalizada. ¡Excelente noticia!")
                        render_historial() # Refrescar la tabla
                    else:
                        print(f"Error: {msg}")

                ctk.CTkButton(row, text="Finalizar", width=100, height=32,
                              fg_color="#C0392B", hover_color="#A93226",
                              font=ctk.CTkFont(size=12, weight="bold"),
                              command=lambda lid=les['id'], t=les['tipo_lesion']: finalizar(lid, t)).pack(side="right", padx=15)

    render_historial()

    # ===================== BOTÓN CERRAR =====================
    ctk.CTkButton(cnt, text="Volver al Menú", width=340, height=42,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=ventana.destroy).pack(pady=(15, 20))
