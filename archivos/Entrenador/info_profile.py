import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
#aqui van las interfaces de perfil tanto del nadador como del entrenandor
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# ===============================
# PERFIL ENTRENADOR
# ===============================
def profile_trainer():

    ventana = ctk.CTkToplevel()
    ventana.title("Perfil del Entrenador")
    ventana.geometry("400x450")

    titulo = ctk.CTkLabel(ventana, text="Perfil del Entrenador", font=("Arial",20,"bold"))
    titulo.pack(pady=10)

    nombre = ctk.CTkEntry(ventana, placeholder_text="Nombre")
    nombre.pack(pady=5)

    edad = ctk.CTkEntry(ventana, placeholder_text="Edad")
    edad.pack(pady=5)

    experiencia = ctk.CTkEntry(ventana, placeholder_text="Años de experiencia")
    experiencia.pack(pady=5)

    especialidad = ctk.CTkEntry(ventana, placeholder_text="Especialidad")
    especialidad.pack(pady=5)

    password = ctk.CTkEntry(ventana, placeholder_text="Contraseña", show="*")
    password.pack(pady=5)


    def guardar():
        messagebox.showinfo("Info", "Entrenador guardado (conectar a BD aquí)")


    def eliminar():
        messagebox.showwarning("Info", "Entrenador eliminado (conectar a BD aquí)")


    btn_guardar = ctk.CTkButton(ventana, text="Guardar", command=guardar)
    btn_guardar.pack(pady=10)

    btn_eliminar = ctk.CTkButton(ventana, text="Eliminar", fg_color="red", command=eliminar)
    btn_eliminar.pack(pady=5)
