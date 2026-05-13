import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from archivos.Asistente_voz.asistente import talk
from PIL import Image
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.metricas import obtener_estadisticas_globales

def global_statistics_interface(root):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Estadísticas globales")
    ventana.geometry("520x560")

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

    card = ctk.CTkFrame(ventana, width=460, height=500, corner_radius=24,
                        fg_color="#080808", border_width=1, border_color="#151516")
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    # ← usa pack en contenido para que los hijos también usen pack
    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.pack(expand=True, fill="both", padx=24, pady=20)

    ctk.CTkLabel(contenido, text="Estadísticas Globales",
                 font=ctk.CTkFont(size=18, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(10, 6))

    ctk.CTkLabel(contenido, text="Consulta el rendimiento general del equipo",
                 font=ctk.CTkFont(size=12), text_color="#AAB8C2").pack(pady=(0, 12))

    input_nickname = ctk.CTkEntry(contenido, width=340, height=38,
                                  placeholder_text="Nombre del entrenador")
    input_nickname.pack(pady=5)

    lbl_estado = ctk.CTkLabel(contenido, text="", font=ctk.CTkFont(size=12))
    lbl_estado.pack(pady=6)

    resultado_frame = ctk.CTkFrame(contenido, fg_color="#0A1A2A", corner_radius=12,
                                   border_width=1, border_color="#1E4080")
    lbl_resultado = ctk.CTkLabel(resultado_frame, text="", font=ctk.CTkFont(size=13),
                                 text_color="#E8F4FD", justify="left")
    lbl_resultado.pack(padx=16, pady=10)

    btn_grafica = ctk.CTkButton(contenido, text="📈 Ver Gráfica Comparativa",
                                width=340, height=38, fg_color="#1ABC9C",
                                hover_color="#16A085", command=lambda: mostrar_grafica())
    
    est_cache = [None]

    def consultar():
        nombre = input_nickname.get().strip()
        if not nombre:
            lbl_estado.configure(text="⚠️ Ingresa un nombre", text_color="orange")
            resultado_frame.pack_forget()
            btn_grafica.pack_forget()
            return

        estadisticas = obtener_estadisticas_globales(nombre)
        if not estadisticas:
            lbl_estado.configure(text=f"Sin datos para: {nombre}", text_color="#FF6B6B")
            resultado_frame.pack_forget()
            btn_grafica.pack_forget()
            return

        est_cache[0] = estadisticas
        lbl_estado.configure(text=f"✅ Estadísticas de {nombre}", text_color="#1ABC9C")

        texto = (
            f"Total sesiones: {estadisticas.get('total_sesiones', 0)}\n"
            f"Total nadadores: {estadisticas.get('total_nadadores', 0)}\n"
            f"Distancia promedio: {estadisticas.get('distancia_promedio', 0):.2f} m\n"
            f"Tiempo promedio: {estadisticas.get('tiempo_promedio', 0):.2f} seg\n"
            f"Ritmo promedio: {estadisticas.get('ritmo_promedio', 0):.4f}"
        )

        lbl_resultado.configure(text=texto)
        resultado_frame.pack(fill="x", pady=6)

        if estadisticas.get('por_nadador'):
            btn_grafica.pack(pady=5)

    def mostrar_grafica():
        est = est_cache[0]
        if not est or not est.get('por_nadador'):
            return

        v_g = ctk.CTkToplevel(ventana)
        v_g.title("Grafica Comparativa del Equipo")
        v_g.geometry("800x500")
        v_g.configure(fg_color="#080808")
        v_g.update()

        nombres = [n['nombre'] for n in est['por_nadador']]
        distancias = [n['distancia'] for n in est['por_nadador']]
        tiempos = [n['tiempo'] for n in est['por_nadador']]
        ritmos = [n['ritmo'] for n in est['por_nadador']]
        x = range(len(nombres))

        fig, axes = plt.subplots(1, 3, figsize=(13, 4))
        fig.patch.set_facecolor('#080808')

        colores = ['#0072FF', '#1ABC9C', '#F39C12', '#9333EA', '#E74C3C']

        titulos = ['Distancia promedio (m)', 'Tiempo promedio (seg)', 'Ritmo (s/m)']
        datos = [distancias, tiempos, ritmos]

        for i, ax in enumerate(axes):
            ax.set_facecolor('#0A1A2A')
            ax.tick_params(colors='white', labelsize=9)
            ax.title.set_color('white')
            ax.set_title(titulos[i])
            for spine in ax.spines.values():
                spine.set_edgecolor('#1E4080')

            # grafica de lineas con puntos
            ax.plot(list(x), datos[i], color=colores[0], linewidth=2,
                    marker='o', markersize=7, markerfacecolor=colores[1])
            ax.fill_between(list(x), datos[i], alpha=0.15, color=colores[0])
            ax.set_xticks(list(x))
            ax.set_xticklabels(nombres, rotation=15, ha='right', color='white')

        plt.tight_layout(pad=2.0)

        canvas = FigureCanvasTkAgg(fig, master=v_g)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        v_g.protocol("WM_DELETE_WINDOW", lambda: (plt.close(fig), v_g.destroy()))

    ctk.CTkButton(contenido, text="Consultar estadísticas", width=340, height=38,
                  fg_color="#0072FF", hover_color="#005ACC",
                  command=consultar).pack(pady=6)

    ctk.CTkButton(contenido, text="Cerrar", width=340, height=36,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=ventana.destroy).pack(pady=(0, 10))