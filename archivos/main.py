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
from Backend.database import inicializar_sistema, obtener_conexion
from Backend.funcionamiento_logica_modulos.entrenadores import registrar_entrenador, login_entrenador

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

def limpiar():
    user_entry.delete(0, 'end')
    pass_entry.delete(0, 'end')

def cambiar_a_nadador():
    global ruta_fondo
    limpiar()

    ruta_fondo = "Backgrounds/fondo1.webp"
    actualizar_fondo()

    titulo.configure(text="Login Nadador")
    label_user.configure(text="Código de acceso")

    label_pass.place_forget()
    pass_entry.place_forget()

    btn_login.configure(text="Ingresar Nadador", command=login_nadador)
    btn_switch.configure(text="Modo Entrenador", command=cambiar_a_entrenador)

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

def login_entrenador_ui():
    nombre = user_entry.get().strip()
    password = pass_entry.get().strip()

    if not nombre or not password:
        messagebox.showerror("Error", "Completa todos los campos")
        return

    res = login_entrenador(nombre, password)

    if res:
        SESSION["id"] = res[0]
        SESSION["rol"] = "entrenador"
        messagebox.showinfo("Acceso", f"Bienvenido entrenador {res[1]}")
        ventana.destroy()
        interfaz_general()
    else:
        messagebox.showerror("Error", "Credenciales inválidas")

def login_nadador():
    codigo = user_entry.get().strip()

    if not codigo:
        messagebox.showerror("Error", "Ingresa tu código de acceso")
        return

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre 
        FROM nadadores
        WHERE codigo_acceso = %s AND activo = TRUE
    """, (codigo,))

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        SESSION["id"] = resultado[0]
        SESSION["rol"] = "nadador"
        messagebox.showinfo("Bienvenido", f"Hola {resultado[1]}")
        ventana.destroy()
        interfaz_nadador()
    else:
        messagebox.showerror("Error", "Código inválido o nadador inactivo")

def ventana_registro():
    registro = ctk.CTkToplevel(ventana)
    registro.geometry("360x480")  # un poco más alto para que quepa el botón
    registro.title("Registro Entrenador")

    def actualizar_fondo_reg(event=None):
        w = registro.winfo_width()
        h = registro.winfo_height()

        if w < 100 or h < 100:
            return

        img = Image.open("Backgrounds/fondo 4.jpg").resize((w, h))
        bg_reg = CTkImage(light_image=img, size=(w, h))

        fondo_reg.configure(image=bg_reg)
        fondo_reg.image = bg_reg  # evitar que desaparezca

        card_reg.place(relx=0.5, rely=0.5, anchor="center")

    fondo_reg = ctk.CTkLabel(registro, text="")
    fondo_reg.place(x=0, y=0, relwidth=1, relheight=1)

    card_reg = ctk.CTkFrame(
        registro,
        width=280,
        height=440,  # aumentar alto para que quepa botón
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
botones_frame.place(relx=0.5, rely=0.68, anchor="n")  # el top del frame en 68% del card

# --- Botón Ingresar ---
btn_login = ctk.CTkButton(botones_frame, text="Ingresar", command=login_entrenador_ui)
btn_login.pack(fill="x", pady=(0, 10))  # 10 píxeles de espacio abajo

# --- Botón Modo Nadador ---
btn_switch = ctk.CTkButton(botones_frame, text="Modo Nadador", fg_color="red", command=cambiar_a_nadador)
btn_switch.pack(fill="x", pady=(0, 10))  # 10 píxeles de espacio abajo

# --- Botón Registrarse ---
btn_registrarse = ctk.CTkButton(botones_frame, text="Registrarse como entrenador", fg_color="#50a51f", command=ventana_registro)
btn_registrarse.pack(fill="x", pady=(0, 10))  # último botón, sin espacio extra

ventana.bind("<Configure>", actualizar_fondo)
talk("Bienvenido a Cobaj Sports Rendiment")

#funcion de la animacion del splash screen, se muestra al iniciar el programa y luego se oculta para mostrar la ventana principal
inicializar_sistema()
mostrar_splash(ventana)
ventana.mainloop()