import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.nadadores import buscar_nadador_por_codigo,registrar_nadador
#aqui el entrenador podra registrar y ver a sus alumnos, aqui podra ver a los alumnos que tiene registrados, y registrar a nuevos alumnos, ademas de eliminar a los alumnos que ya no entrenan con el

def interfaz_registrar_nadador(root, entrenador):
    ventana = ctk.CTkToplevel(root) 
    entrenador_id = entrenador["id"]
    entrenador_nombre = entrenador["nombre"]
    ventana.title("Registrar Nadador")
    ventana.geometry("520x500")

    # ===================== FONDO =====================
    try:
        img_fondo = Image.open("Backgrounds/fondo7.webp")
        bg_ref = [None]

        fondo_lbl = ctk.CTkLabel(ventana, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_lbl.lower()

        def actualizar(event=None):
            w = ventana.winfo_width()
            h = ventana.winfo_height()

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
    card = ctk.CTkFrame(
        ventana,
        width=320,
        height=400,
        corner_radius=24,
        fg_color="#080808",
        border_width=1,
        border_color="#151516"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.pack(expand=True, fill="both", padx=28, pady=24)

    ctk.CTkLabel(contenido, text=f" Entrenador: {entrenador_nombre}", size=16).pack(pady=10)

    e_nombre = ctk.CTkEntry(contenido, placeholder_text="Nombre",width=200)
    e_nombre.pack(fill="x", pady=5)

    e_codigo = ctk.CTkEntry(contenido, placeholder_text="Código",width=200)
    e_codigo.pack(fill="x", pady=5)

    lbl = ctk.CTkLabel(contenido, text="")
    lbl.pack(pady=10)

    def registrar():
        nombre = e_nombre.get().strip()
        codigo = e_codigo.get().strip()

        if not nombre or not codigo:
            lbl.configure(text="Completa los campos", text_color="orange")
            return

        if buscar_nadador_por_codigo(codigo, entrenador_id):
            lbl.configure(text="Código ya existe", text_color="red")
            return

        registrar_nadador(nombre, codigo, entrenador_id)
        lbl.configure(text="Registrado", text_color="green")

    ctk.CTkButton(contenido, text="Registrar", command=registrar).pack(pady=10)
    ctk.CTkButton(contenido, text="Cerrar", command=ventana.destroy).pack()


# ===================== MAIN =====================
if __name__ == "__main__":
    root = ctk.CTk()  # 🔥 SOLO UNA VEZ
    root.geometry("400x300")

    ctk.CTkButton(
        root,
        text="Abrir registro",
        command=lambda: interfaz_registrar_nadador(root)
    ).pack(pady=50)

    root.mainloop()