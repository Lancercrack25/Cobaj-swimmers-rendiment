import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.nadadores import buscar_nadador_por_codigo_global, vincular_nadador_entrenador,obtener_nadadores
#aqui ,el entrenador podra registrar y ver a sus alumnos, aqui podra ver a los alumnos que tiene registrados, y registrar a nuevos alumnos, ademas de eliminar a los alumnos que ya no entrenan con el
# Arreglo compartido en memoria — persiste mientras la app esté abierta
equipo_actual = []

def interfaz_registrar_nadador(root, entrenador):
    ventana = ctk.CTkToplevel(root)
    entrenador_id = entrenador["id"]
    entrenador_nombre = entrenador["nombre"]
    ventana.title("Agregar Nadador al Equipo")
    ventana.geometry("520x500")

    # Carga nadadores que ya tenía este entrenador
    equipo_actual.clear()
    equipo_actual.extend(obtener_nadadores(entrenador_id))

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

        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)
    except Exception as e:
        print("Error fondo:", e)

    # ===================== CARD =====================
    card = ctk.CTkFrame(ventana, width=320, height=340,
                        corner_radius=24, fg_color="#080808",
                        border_width=1, border_color="#151516")
    card.place(relx=0.5, rely=0.5, anchor="center")

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.place(x=0, y=0, relwidth=1, relheight=1)

    ctk.CTkLabel(contenido, text=f"Entrenador: {entrenador_nombre}",
                 font=ctk.CTkFont(size=13), text_color="#AAB8C2").pack(pady=(24, 4))

    ctk.CTkLabel(contenido, text="Ingresa el código del nadador",
                 font=ctk.CTkFont(size=15, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 16))

    e_codigo = ctk.CTkEntry(contenido, placeholder_text="Código de acceso", width=220, height=38)
    e_codigo.pack(pady=5)

    lbl = ctk.CTkLabel(contenido, text="", font=ctk.CTkFont(size=12))
    lbl.pack(pady=8)

    def agregar():
        codigo = e_codigo.get().strip()
        if not codigo:
            lbl.configure(text="Ingresa un código", text_color="orange")
            return

        if any(n["codigo_acceso"] == codigo for n in equipo_actual):
            talk(f"El nadador {entrenador_nombre} ya está en tu equipo, no puedes agregarlo dos veces")
            lbl.configure(text="Ya está en tu equipo", text_color="orange")
            return

        nadador = buscar_nadador_por_codigo_global(codigo)
        if not nadador:
            talk("El codigo que ingresaste no corresponde a ningún nadador registrado, intente de nuevo")
            lbl.configure(text="Código no encontrado", text_color="red")
            return

        # Vincular en BD y agregar al arreglo
        ok = vincular_nadador_entrenador(nadador["id"], entrenador_id)
        if not ok:
            lbl.configure(text="Error al vincular, intenta de nuevo", text_color="red")
            return

        equipo_actual.append(nadador)
        e_codigo.delete(0, "end")
        talk(f"Nadador {nadador['nombre']}  ha sido agregado a tu equipo {entrenador_nombre}")
        lbl.configure(text=f"✅ {nadador['nombre']} agregado", text_color="green")

    ctk.CTkButton(contenido, text="Agregar al equipo", width=220, height=38,
                  fg_color="#0072FF", hover_color="#005ACC",
                  command=agregar).pack(pady=6)

    ctk.CTkButton(contenido, text="Cerrar", width=220, height=36,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=ventana.destroy).pack(pady=(0, 20))