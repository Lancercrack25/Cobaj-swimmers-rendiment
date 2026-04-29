#este archivo es para  la interfaz que el entrenador vera despues de iniciar sesion, aqui se podran registrar nadadores, eliminar nadadores, ver estadisticas, etc. es como el menu principal del entrenador
import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.metricas_rendimiento.interface_stadistics import interfaz_estadisticas
from archivos.rendimiento_seciones.verificacion import interfaz_validar_lesion
from archivos.Lesion.verificacion_lesionados import interfaz_validar_para_lesion
from archivos.Entrenador.mis_alumnos import interfaz_registrar_nadador
from archivos.Entrenador.visualizar import interfaz_ver_nadadores
from archivos.Entrenador.eliminacion_alumnos import interfaz_eliminar_nadador
from archivos.Asistente_voz.asistente import talk

def interfaz_general(entrenador_actual):
    ventana = ctk.CTk()
    ventana.title("Interfaz General")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#000000")

    # ================= FONDO =================
    ruta_fondo = "Backgrounds/fondo2.webp"

    fondo_label = ctk.CTkLabel(ventana, text="")
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    fondo_label.lower()

    def actualizar_fondo(event=None):
        w = ventana.winfo_width()
        h = ventana.winfo_height()
        if w < 100 or h < 100:
            return

        base = Image.open(ruta_fondo).resize((w, h)).convert("RGBA")

        # zona blur centrada
        cw, ch = 320, 380
        cx, cy = (w - cw) // 2, (h - ch) // 2
        zona = base.crop((cx, cy, cx + cw, cy + ch))
        zona_blur = zona.filter(ImageFilter.GaussianBlur(radius=8))
        overlay = Image.new("RGBA", (cw, ch), (255, 255, 255, 15))
        zona_final = Image.alpha_composite(zona_blur, overlay)
        base.paste(zona_final, (cx, cy))

        bg = CTkImage(light_image=base.convert("RGB"), size=(w, h))
        fondo_label.configure(image=bg)
        fondo_label.image = bg

        card.place(relx=0.5, rely=0.5, anchor="center")

    # ================= CARD CENTRAL =================
    card = ctk.CTkFrame(ventana, width=300, height=380, corner_radius=20,
                        fg_color="transparent", bg_color="transparent")
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    # ================= WIDGETS =================
    etiqueta_titulo = ctk.CTkLabel(card, text="Menú Principal",
                                   font=ctk.CTkFont(size=22, weight="bold"),
                                   text_color="white", bg_color="transparent",
                                   fg_color="transparent")
    etiqueta_titulo.pack(pady=(20, 15))

    botones = [
        ("Registrar nadador",                "#0A84FF",lambda: interfaz_registrar_nadador(ventana, entrenador_actual)),
        ("Mis nadadores",                    "#4D6533", lambda: interfaz_ver_nadadores(entrenador_id=entrenador_actual["id"])),
        ("Ver estadísticas del nadador",     "#34C759", lambda: interfaz_estadisticas()),
        ("Eliminar nadador",                 "#FF3B30", lambda: interfaz_eliminar_nadador(entrenador=entrenador_actual, root=ventana)),
        ("Registro de sesión",               "#AF52DE", lambda: interfaz_validar_lesion(ventana)),
        ("Registrar nadador lesionado",      "#D952DE", lambda: interfaz_validar_para_lesion(ventana)),
        ("Salir",                            "#DD8117", lambda: ventana.destroy()),
    ]

    for texto, color, comando in botones:
        ctk.CTkButton(
            card,
            text=texto,
            fg_color=color,
            bg_color="transparent",
            hover_color=color,
            width=240,
            command=comando if comando else lambda: None
        ).pack(pady=5)

    ventana.bind("<Configure>", actualizar_fondo)
    ventana.after(100, actualizar_fondo)
    ventana.mainloop()