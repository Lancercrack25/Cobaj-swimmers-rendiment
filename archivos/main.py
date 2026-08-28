#librerias necesarias para la interfaz gráfica y el funcionamiento del programa
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
#librerias para las imagenes de fondo
from PIL import Image, ImageFilter
from customtkinter import CTkImage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#con esta línea evitamos que se creen los archivos pycache al ejecutar el programa
sys.dont_write_bytecode = True
#importaciones de funciones de los módulos del programa
from archivos.Animaciones.splash import mostrar_splash
from archivos.Asistente_voz.asistente import talk
from archivos.Entrenador.interface_general import interfaz_general
from archivos.Nadadores.interface_swimmers import interfaz_nadador
from archivos.Nadadores.Registro_nadador import registro_swimmer
from Backend.database import inicializar_sistema, obtener_conexion
from Backend.funcionamiento_logica_modulos.entrenadores import registrar_entrenador, login_entrenador, obtener_entrenador_por_id
from Backend.funcionamiento_logica_modulos.nadadores import login_nadador

# Configuración general CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ajuste para evitar problemas de escalado DPI en distintas pantallas
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

SESSION = {"id": None, "rol": None}
#ancho y alto de la ventana
W, H = 480, 520
#ancho y alto del card central donde se encuentran los campos de login y botones, se usa para calcular la zona borrosa del fondo
CW, CH = 260, 300

ruta_fondo = "Backgrounds/fondo3.webp"

def actualizar_fondo(event=None):
    global bg, ruta_fondo
    w = ventana.winfo_width()
    h = ventana.winfo_height()
    if w < 100 or h < 100:
        return

    base = Image.open(ruta_fondo).resize((w, h)).convert("RGBA")
    cx = (w - CW) // 2
    cy = (h - CH) // 2

    zona = base.crop((cx, cy, cx + CW, cy + CH))
    zona_blur = zona.filter(ImageFilter.GaussianBlur(radius=8))

    overlay = Image.new("RGBA", (CW, CH), (255, 255, 255, 15))
    zona_final = Image.alpha_composite(zona_blur, overlay)

    base.paste(zona_final, (cx, cy))

    bg = CTkImage(light_image=base.convert("RGB"), size=(w, h))
    fondo.configure(image=bg)

    card.place(relx=0.5, rely=0.5, anchor="center")
#limpia los campos de texto para evitar que al cambiar de modo queden los datos escritos en los campos
def limpiar():
    user_entry.delete(0, 'end')
    pass_entry.delete(0, 'end')
#esta funcion cambia la interfaz de login de entrenador a nadador, cambia el fondo, los textos y los botones, ademas de agregar un nuevo boton para registrar nadadores
def cambiar_a_nadador():
    global ruta_fondo
    limpiar()

    ruta_fondo = "Backgrounds/fondo1.webp"
    actualizar_fondo()

    titulo.configure(text="Login Nadador")
    label_user.configure(text="Código de acceso")
    label_pass.configure(text="Contraseña")
   
    btn_login.configure(text="Ingresar Nadador", command=login_nadador_ui)
    btn_switch.configure(text="Modo Entrenador", command=cambiar_a_entrenador)

    # 🔹 CAMBIO AGREGADO
    btn_registrarse.configure(
        text="Registrar Nadador",
        command=registro_swimmer
    )

def cambiar_a_entrenador():
    global ruta_fondo
    limpiar()

    ruta_fondo = "Backgrounds/fondo3.webp"
    actualizar_fondo()

    titulo.configure(text="Login Entrenador")
    label_user.configure(text="Usuario")

    label_pass.place(relx=0.5, rely=0.35, anchor="center")
    pass_entry.place(relx=0.5, rely=0.45, anchor="center")

    btn_login.configure(text="Ingresar", command=login_entrenador_ui)
    btn_switch.configure(text="Modo Nadador", command=cambiar_a_nadador)

    # 🔹 CAMBIO AGREGADO
    btn_registrarse.configure(
        text="Registrarse como entrenador",
        command=ventana_registro
    )
#aqui se define la función para el login del entrenador, se obtiene el nombre y la contraseña de los campos de texto, se verifica que no estén vacíos y luego se llama a la función de login del backend, si el login es exitoso se guarda la información del entrenador en una variable global y se muestra un mensaje de bienvenida, luego se cierra la ventana de login y se abre la interfaz general del entrenador
def login_entrenador_ui():
    nombre = user_entry.get().strip()
    password = pass_entry.get().strip()

    if not nombre or not password:
        messagebox.showerror("Error", "Completa todos los campos")
        return

    res = login_entrenador(nombre, password)

    if not res:
        messagebox.showerror("Error", "Credenciales inválidas")
        return

    # 🔥 CREAS EL OBJETO GLOBAL CORRECTO
    entrenador_actual = {
        "id": res[0],
        "nombre": res[1]
    }

    SESSION["id"] = res[0]
    SESSION["rol"] = "entrenador"
    
    talk(f"Bienvenido entrenador {res[1]} en unos momento  podras acceder a tu menú principal")
    messagebox.showinfo("Acceso", f"Bienvenido {res[1]}")
    ventana.destroy()
    interfaz_general(entrenador_actual)
    
def login_nadador_ui():
    codigo = user_entry.get().strip()
    password = pass_entry.get().strip()

    if not codigo or not password:
        messagebox.showerror("Error", "Completa todos los campos")
        return
    res = login_nadador(codigo, password)
    if not res:
        messagebox.showerror("Error", "Credenciales inválidas")
        return

    # ✅ Se define ANTES de usarlo
    nadador_actual = {
        "id": res[0],
        "nombre": res[1]
    }

    SESSION["id"] = res[0]
    SESSION["rol"] = "nadador"

    talk(f"Bienvenido{res[1]} en unos momentos accederas a la sección de nadadores")
    messagebox.showinfo("Acceso", f"Bienvenido {res[1]}")
    ventana.destroy()
    interfaz_nadador(nadador_actual)

def ventana_registro():
    registro = ctk.CTkToplevel(ventana)
    registro.geometry("500x500")
    registro.title("Registro Entrenador")

    def actualizar_fondo_reg(event=None):
        w = registro.winfo_width()
        h = registro.winfo_height()

        if w < 100 or h < 100:
            return

        img = Image.open("Backgrounds/fondo 4.jpg").resize((w, h))
        bg_reg = CTkImage(light_image=img, size=(w, h))

        fondo_reg.configure(image=bg_reg)
        fondo_reg.image = bg_reg

        card_reg.place(relx=0.5, rely=0.5, anchor="center")

    fondo_reg = ctk.CTkLabel(registro, text="")
    fondo_reg.place(x=0, y=0, relwidth=1, relheight=1)

    card_reg = ctk.CTkFrame(
        registro,
        width=280,
        height=440,
        corner_radius=15,
        fg_color="#72EEE8"
    )
    card_reg.place(relx=0.5, rely=0.5, anchor="center")
    card_reg.pack_propagate(False)

    contenido_frame = ctk.CTkFrame(card_reg, fg_color="transparent")
    contenido_frame.pack(expand=True, fill="both", padx=10, pady=10)

    entries = {}
    for campo in ["Nombre", "Edad", "Experiencia (años)", "Especialidad", "Contraseña"]:
        label = ctk.CTkLabel(contenido_frame, text=campo, text_color="#D3A612", font=("Arial", 18, "bold"))
        label.pack(pady=(8, 2))
        entry = ctk.CTkEntry(
            contenido_frame,
            show="*" if campo == "Contraseña" else "",
            fg_color="#FFFFFF",
            text_color="#000000",
            width=220
        )
        entry.pack(pady=4)
        entries[campo] = entry

    def registrar():
        try:
            nombre = entries["Nombre"].get()
            edad = int(entries["Edad"].get())
            exp = int(entries["Experiencia (años)"].get())
            esp = entries["Especialidad"].get()
            pwd = entries["Contraseña"].get()

            if not all([nombre, esp, pwd]):
                raise ValueError
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return

        ok, msg = registrar_entrenador(nombre, edad, exp, esp, pwd)

        if ok:
            talk(f"Entrenador registrado exitosamente, ya puedes iniciar sesión")
            messagebox.showinfo("Registro exitoso", msg)
            registro.destroy()
        else:
            messagebox.showerror("Error", msg)

    btn_reg = ctk.CTkButton(contenido_frame, text="Registrar", command=registrar, fg_color="#FAD502")
    btn_reg.pack(pady=15)

    registro.bind("<Configure>", actualizar_fondo_reg)
    actualizar_fondo_reg()

# --- Ventana principal ---
ventana = ctk.CTk()
ventana.withdraw() 
ventana.geometry(f"{W}x{H}")
ventana.title("Sistema")
ventana.configure(fg_color="#000000")

bg = CTkImage(light_image=Image.open(ruta_fondo), size=(W, H))
fondo = ctk.CTkLabel(ventana, image=bg, text="")
fondo.place(x=0, y=0, relwidth=1, relheight=1)
fondo.lower()

card = ctk.CTkLabel(ventana, text="", width=CW, height=338, fg_color="transparent")
card.place(relx=0.5, rely=0.5, anchor="center")

titulo = ctk.CTkLabel(card, text="Login Entrenador", font=("Arial", 20, "bold"), text_color="white")
titulo.place(relx=0.5, rely=0.1, anchor="center")

label_user = ctk.CTkLabel(card, text="Usuario", text_color="white")
label_user.place(relx=0.5, rely=0.25, anchor="center")

user_entry = ctk.CTkEntry(card, width=200, fg_color="#555", text_color="white")
user_entry.place(relx=0.5, rely=0.35, anchor="center")

label_pass = ctk.CTkLabel(card, text="Contraseña", text_color="white")
label_pass.place(relx=0.5, rely=0.5, anchor="center")

pass_entry = ctk.CTkEntry(card, show="*", width=200, fg_color="#555", text_color="white")
pass_entry.place(relx=0.5, rely=0.6, anchor="center")

botones_frame = ctk.CTkFrame(card, fg_color="transparent")
botones_frame.place(relx=0.5, rely=0.68, anchor="n")

btn_login = ctk.CTkButton(botones_frame, text="Ingresar", command=login_entrenador_ui)
btn_login.pack(fill="x", pady=(0, 10))

btn_switch = ctk.CTkButton(botones_frame, text="Modo Nadador", fg_color="red", command=cambiar_a_nadador)
btn_switch.pack(fill="x", pady=(0, 10))

btn_registrarse = ctk.CTkButton(
    botones_frame,
    text="Registrarse como entrenador",
    fg_color="#50a51f",
    command=ventana_registro
)
btn_registrarse.pack(fill="x", pady=(0, 10))

ventana.bind("<Configure>", actualizar_fondo)
talk("Bienvenido a Cobaj Sports Rendiment")
#inicia el backend
inicializar_sistema()
#muestra el splash de la animacion para la app
mostrar_splash(ventana)
#muestra la ventana principal de la app 
ventana.mainloop()