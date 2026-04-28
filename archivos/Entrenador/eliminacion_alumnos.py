#aqui el entrenador podra eliminar que alumnos ya no estan entrenando con el
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import eliminar_nadador, obtener_nadadores
#aqui el entrenador podra eliminar que alumnos ya no estan entrenando con el, se mostrara una lista de los alumnos registrados y se podra seleccionar uno para eliminarlo, ademas de que se mostrara un mensaje de confirmacion antes de eliminar al alumno
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

def interfaz_eliminar_nadador(entrenador_id):
    v = ctk.CTk()
    v.title("Eliminar")
    v.geometry("500x600")

    _aplicar_fondo(v)

    frame = ctk.CTkFrame(v)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    lista = ctk.CTkScrollableFrame(frame)
    lista.pack(fill="both", expand=True)

    seleccionado = {"id": None}

    def render():
        for w in lista.winfo_children():
            w.destroy()

        for n in obtener_nadadores(entrenador_id):
            def sel(i=n["id"]):
                seleccionado["id"] = i

            ctk.CTkButton(
                lista,
                text=f"{n['nombre']} ({n['codigo_acceso']})",
                command=sel
            ).pack(fill="x", pady=2)

    def eliminar():
        if not seleccionado["id"]:
            return

        eliminar_nadador(seleccionado["id"], entrenador_id)
        render()

    render()

    ctk.CTkButton(frame, text="Eliminar", command=eliminar).pack(pady=10)
    ctk.CTkButton(frame, text="Cerrar", command=v.destroy).pack()

    v.mainloop()