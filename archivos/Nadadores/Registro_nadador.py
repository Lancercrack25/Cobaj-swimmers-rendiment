#en este acrchivo se podra registrar a los nadadores, aqui se podran agregar los datos de cada nadador, como su nombre, edad, genero, etc. es como un registro de nadadores para el entrenador
import customtkinter as ctk
from tkinter import messagebox
from archivos.Asistente_voz.asistente import talk
import random
import string
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import registrar_nadador

#funcion para que genere un codigo aleatorio para cada nadador, este codigo sera unico para cada nadador y se utilizara para identificarlo en el sistema, este codigo se generara automaticamente al registrar un nuevo nadador, no se podra modificar ni eliminar, solo se podra generar uno nuevo si se elimina el nadador actual
def codigo_nadador():
    numeros = string.digits
    codigo = ''.join(random.choice(numeros) for _ in range(9))
    return codigo

def registro_swimmer():
    registro = ctk.CTkToplevel()
    registro.geometry("500x600")
    registro.title("Registro Nadador")

    # ---------------- FONDO (CARGA UNA SOLA VEZ) ----------------
    img_original = Image.open("Backgrounds/fondo2.webp")
    bg_img = None

    fondo_reg = ctk.CTkLabel(registro, text="")
    fondo_reg.place(x=0, y=0, relwidth=1, relheight=1)
    fondo_reg.lower()

    def actualizar_fondo_reg(event=None):
        nonlocal bg_img

        w = registro.winfo_width()
        h = registro.winfo_height()

        if w < 100 or h < 100:
            return

        img_resized = img_original.resize((w, h))
        bg_img = CTkImage(light_image=img_resized, size=(w, h))

        fondo_reg.configure(image=bg_img)
        fondo_reg.image = bg_img

        fondo_reg.lower()

    # ---------------- CARD PRINCIPAL ----------------
    card_reg = ctk.CTkFrame(
        registro,
        width=300,
        height=540,
        corner_radius=15,
        fg_color="#72D9EE"
    )
    card_reg.place(relx=0.5, rely=0.5, anchor="center")
    card_reg.pack_propagate(False)

    contenido_frame = ctk.CTkFrame(card_reg, fg_color="transparent")
    contenido_frame.pack(expand=True, fill="both", padx=10, pady=10)

    entries = {}

    # ---------------- CAMPOS ----------------
    campos = ["Nombre", "Edad", "Peso (kg)", "Estatura (m)"]

    for campo in campos:
        ctk.CTkLabel(
            contenido_frame,
            text=campo,
            text_color="#D3A612",
            font=("Arial", 16, "bold")
        ).pack(pady=(6, 2))

        entry = ctk.CTkEntry(
            contenido_frame,
            fg_color="#FFFFFF",
            text_color="#000000",
            width=220
        )
        entry.pack(pady=3)

        entries[campo] = entry

    # ---------------- GENERO ----------------
    ctk.CTkLabel(
        contenido_frame,
        text="Género",
        text_color="#D3A612",
        font=("Arial", 16, "bold")
    ).pack(pady=(8, 2))

    genero_var = ctk.StringVar(value="M")

    ctk.CTkOptionMenu(
        contenido_frame,
        values=["Masculino", "Femenino", "Otro"],
        bg_color= "#D3C912",
        variable=genero_var
    ).pack(pady=3)

    # ---------------- CHECKBOX ----------------
    problema_var = ctk.BooleanVar()

    ctk.CTkCheckBox(
        contenido_frame,
        text="Problema respiratorio",
        text_color= "#1B1A1A",
        variable=problema_var
    ).pack(pady=10)

    # ---------------- REGISTRAR (DEFINIDO ANTES DEL BOTÓN) ----------------
    def registrar():
        try:
            nombre = entries["Nombre"].get().strip()
            edad = int(entries["Edad"].get())
            peso = float(entries["Peso (kg)"].get())
            estatura = float(entries["Estatura (m)"].get())
            genero = genero_var.get()
            problema = problema_var.get()

            if not nombre:
                raise ValueError("Nombre vacío")

            codigo = codigo_nadador()

        except Exception:
            messagebox.showerror("Error", "Datos inválidos")
            return

        ok, msg = registrar_nadador(
            nombre,
            edad,
            codigo,
            genero,
            peso,
            estatura,
            problema
        )

        if ok:
            messagebox.showinfo(
                "Registro exitoso",
                f"{msg}\n\nTu código es: {codigo}"
            )
            talk("Nadador registrado correctamente, guarda bien tu código")
            registro.destroy()
        else:
            messagebox.showerror("Error", msg)

    # ---------------- BOTÓN ----------------
    ctk.CTkButton(
        contenido_frame,
        text="Registrar",
        command=registrar,
        fg_color="#FAD502",
        text_color="black"
    ).pack(pady=15)

    # ---------------- EVENTO RESIZE ----------------
    registro.bind("<Configure>", actualizar_fondo_reg)
    actualizar_fondo_reg()