import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.nadadores import obtener_nadadores
#aqui el entrenador podra registrar y ver a sus alumnos, aqui podra ver a los alumnos que tiene registrados, y registrar a nuevos alumnos, ademas de eliminar a los alumnos que ya no entrenan con el
def _aplicar_fondo(ventana):
    try:
        img_fondo = Image.open("Backgrounds/fondo 6.png")
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
        ventana.bind("<Configure>", actualizar)
        ventana.after(100, actualizar)
    except Exception:
        pass

def interfaz_ver_nadadores(entrenador_id):
    v = ctk.CTk()
    v.title("Nadadores")
    v.geometry("500x600")

    _aplicar_fondo(v)

    frame = ctk.CTkFrame(v)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    buscador = ctk.CTkEntry(frame, placeholder_text="Buscar")
    buscador.pack(pady=5, fill="x")

    lista = ctk.CTkScrollableFrame(frame)
    lista.pack(fill="both", expand=True)

    cache = []

    def render(data):
        for w in lista.winfo_children():
            w.destroy()

        for n in data:
            ctk.CTkLabel(lista,
                text=f"{n['nombre']} | {n['codigo_acceso']}").pack(anchor="w")

    def cargar():
        nonlocal cache
        cache = obtener_nadadores(entrenador_id)
        render(cache)

    def filtrar(event=None):
        txt = buscador.get().lower()
        render([n for n in cache if txt in n["nombre"].lower() or txt in n["codigo_acceso"].lower()])

    buscador.bind("<KeyRelease>", filtrar)

    cargar()

    ctk.CTkButton(frame, text="Cerrar", command=v.destroy).pack(pady=5)

    v.mainloop()
