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

# ================= VALIDACIONES =================
def validar_campos(nombre, edad_str, peso_str, estatura_str):
    """
    Valida que los campos ingresados sean correctos.
    Retorna (True, datos_convertidos) o (False, mensaje_error).
    """
    if not nombre:
        return False, "El nombre no puede estar vacío."
 
    try:
        edad = int(edad_str)
        if edad <= 0 or edad > 120:
            return False, "La edad debe ser un número válido entre 1 y 120."
    except ValueError:
        return False, "La edad debe ser un número entero."
 
    try:
        peso = float(peso_str)
        if peso <= 0 or peso > 300:
            return False, "El peso debe ser un número válido en kg."
    except ValueError:
        return False, "El peso debe ser un número decimal (ej. 65.5)."
 
    try:
        estatura = float(estatura_str)
        if estatura <= 0 or estatura > 3:
            return False, "La estatura debe ser un número válido en metros (ej. 1.75)."
    except ValueError:
        return False, "La estatura debe ser un número decimal (ej. 1.75)."
 
    return True, (nombre, edad, peso, estatura)
 
# ================= VENTANA PRINCIPAL =================
def registro_swimmer():
    registro = ctk.CTkToplevel()
    registro.geometry("500x620")
    registro.title("Registro de Nadador")
    registro.resizable(False, False)
 
    # ---------------- FONDO ----------------
    try:
        img_original = Image.open("Backgrounds/fondo2.webp")
        bg_img_ref = [None]
 
        fondo_reg = ctk.CTkLabel(registro, text="")
        fondo_reg.place(x=0, y=0, relwidth=1, relheight=1)
        fondo_reg.lower()
 
        def actualizar_fondo(event=None):
            w = registro.winfo_width()
            h = registro.winfo_height()
            if w < 100 or h < 100:
                return
            img_resized = img_original.resize((w, h))
            bg_img_ref[0] = CTkImage(light_image=img_resized, size=(w, h))
            fondo_reg.configure(image=bg_img_ref[0])
            fondo_reg.lower()
 
        registro.bind("<Configure>", actualizar_fondo)
        registro.after(100, actualizar_fondo)
 
    except Exception:
        registro.configure(fg_color="#1a1a2e")
 
    # ---------------- CARD ----------------
    card = ctk.CTkFrame(
        registro,
        width=320,
        height=570,
        corner_radius=15,
        fg_color="#72D9EE"
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)
 
    contenido = ctk.CTkFrame(card, fg_color="transparent")
    contenido.pack(expand=True, fill="both", padx=15, pady=15)
 
    # ---------------- TÍTULO ----------------
    ctk.CTkLabel(
        contenido,
        text="Registro de Nadador",
        text_color="#1B1A1A",
        font=("Arial", 18, "bold")
    ).pack(pady=(0, 10))
 
    # ---------------- CAMPOS DE TEXTO ----------------
    campos = ["Nombre", "Edad", "Peso (kg)", "Estatura (m)"]
    entries = {}
 
    for campo in campos:
        ctk.CTkLabel(
            contenido,
            text=campo,
            text_color="#D3A612",
            font=("Arial", 14, "bold")
        ).pack(pady=(6, 2))
 
        entry = ctk.CTkEntry(
            contenido,
            fg_color="#FFFFFF",
            text_color="#000000",
            width=230,
            placeholder_text=f"Ingresa {campo.lower()}"
        )
        entry.pack(pady=3)
        entries[campo] = entry
 
    # ---------------- GÉNERO ----------------
    ctk.CTkLabel(
        contenido,
        text="Género",
        text_color="#D3A612",
        font=("Arial", 14, "bold")
    ).pack(pady=(8, 2))
 
    genero_var = ctk.StringVar(value="Masculino")
 
    ctk.CTkOptionMenu(
        contenido,
        values=["Masculino", "Femenino", "Otro"],
        variable=genero_var,
        width=230,
        fg_color="#FAD502",
        text_color="#000000",
        button_color="#D3A612"
    ).pack(pady=3)

    # ---------------- CHECKBOX ----------------
    problema_var = ctk.BooleanVar(value=False)
 
    ctk.CTkCheckBox(
        contenido,
        text="Problema respiratorio",
        text_color="#1B1A1A",
        variable=problema_var,
        checkmark_color="#1B1A1A",
        fg_color="#FAD502",
        hover_color="#D3A612"
    ).pack(pady=12)
 
    # ---------------- FUNCIÓN REGISTRAR ----------------
    def registrar():
        nombre    = entries["Nombre"].get().strip()
        edad_str  = entries["Edad"].get().strip()
        peso_str  = entries["Peso (kg)"].get().strip()
        est_str   = entries["Estatura (m)"].get().strip()
        genero    = genero_var.get()
        problema  = problema_var.get()  # BooleanVar: True o False directamente
 
        # Validar campos
        valido, resultado = validar_campos(nombre, edad_str, peso_str, est_str)
        if not valido:
            messagebox.showerror("Error de validación", resultado)
            return
 
        nombre, edad, peso, estatura = resultado
        codigo = codigo_nadador()

        genero_map = {"Masculino": "M", "Femenino": "F", "Otro": "O"}
        genero = genero_map.get(genero, "M")
 
        # Registrar en la base de datos
        ok, msg = registrar_nadador(nombre, edad, codigo, genero, peso, estatura, problema)
        if ok:
            talk("Nadador registrado correctamente, guarda bien tu código")
            messagebox.showinfo(
                "Registro exitoso",
                f"{msg}\n\nGuarda tu código de acceso:\n\n{codigo}"
            )
            registro.destroy()
        else:
            messagebox.showerror("Error al registrar", msg)
 
    # ---------------- BOTÓN REGISTRAR ----------------
    ctk.CTkButton(
        contenido,
        text="Registrar",
        command=registrar,
        fg_color="#FAD502",
        text_color="#000000",
        hover_color="#D3A612",
        width=230,
        height=40,
        font=("Arial", 14, "bold")
    ).pack(pady=15)