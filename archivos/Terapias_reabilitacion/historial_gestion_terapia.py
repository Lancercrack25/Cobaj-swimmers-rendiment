import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.terapias_rehabilitacion import finalizar_rehabilitacion,obtener_historial_rehabilitaciones
#aqui se vera el historial de las terapias del nadador, con la opcion de finalizar cada una de ellas

def interfaz_historial_terapias(root, nadador_id):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Historial de Terapias de Rehabilitación")
    ventana.geometry("600x650")
    ventana.resizable(False, False)
    ventana.configure(fg_color="#0A1628")

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
    card = ctk.CTkFrame(ventana, width=540, height=580, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.place(x=0, y=0, relwidth=1, relheight=1)

    # ===================== HEADER =====================
    av = ctk.CTkFrame(contenido, width=64, height=64, corner_radius=32,
                      fg_color="#1ABC9C", border_width=2, border_color="#16A085")
    av.pack(pady=(30, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="🏥", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(contenido, text="Historial de Terapias",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 4))

    ctk.CTkFrame(contenido, height=2, fg_color="#1ABC9C").pack(fill="x", padx=40, pady=10)

    # ===================== LISTA DE TERAPIAS =====================
    lista_frame = ctk.CTkScrollableFrame(contenido, fg_color="#0A1A2A", corner_radius=12,
                                         border_width=1, border_color="#1E4080", height=320)
    lista_frame.pack(fill="x", padx=30, pady=(10, 10))

    def render_historial():
        # Limpiar la lista antes de re-dibujar
        for w in lista_frame.winfo_children():
            w.destroy()

        historial = obtener_historial_rehabilitaciones(nadador_id)

        if not historial:
            ctk.CTkLabel(lista_frame, text="No hay registros de terapias",
                         text_color="#AAB8C2", font=ctk.CTkFont(size=14)).pack(pady=40)
            return

        for t in historial:
            row = ctk.CTkFrame(lista_frame, fg_color="#132440", corner_radius=10)
            row.pack(fill="x", pady=5, padx=5)

            # Info de la terapia
            info_text = f"🔹 {t['tipo_terapia'].upper()}\n"
            info_text += f"📅 Inicio: {t['fecha_inicio']} | Estimado: {t['tiempo_estimado_dias']} días\n"
            info_text += f"📝 {t['especificaciones'] or 'Sin especificaciones extra'}"
            
            esta_activo = t['fecha_fin'] is None
            estado_color = "#1ABC9C" if not esta_activo else "#F39C12"
            estado_txt = f"✅ Finalizada ({t['fecha_fin']})" if not esta_activo else "🕒 En curso"

            txt_frame = ctk.CTkFrame(row, fg_color="transparent")
            txt_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

            ctk.CTkLabel(txt_frame, text=info_text, font=ctk.CTkFont(size=12),
                         text_color="#E8F4FD", justify="left").pack(anchor="w")
            
            ctk.CTkLabel(txt_frame, text=estado_txt, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=estado_color).pack(anchor="w")

            # Botón para finalizar si está activa
            if esta_activo:
                def finalizar(tid=t['id'], tipo=t['tipo_terapia']):
                    ok, msg = finalizar_rehabilitacion(tid)
                    if ok:
                        talk(f"Terapia de {tipo} finalizada correctamente. ¡Sigue así!")
                        render_historial() # Refrescar la tabla
                    else:
                        print(f"Error: {msg}")

                ctk.CTkButton(row, text="Finalizar", width=100, height=32,
                              fg_color="#1ABC9C", hover_color="#16A085",
                              font=ctk.CTkFont(size=12, weight="bold"),
                              command=lambda tid=t['id'], tipo=t['tipo_terapia']: finalizar(tid, tipo)).pack(side="right", padx=15)

    render_historial()

    # ===================== BOTÓN CERRAR =====================
    ctk.CTkButton(contenido, text="Volver al Menú", width=340, height=42,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=ventana.destroy).pack(pady=(15, 20))