import customtkinter as ctk
from tkinter import messagebox
from Backend.asistente import talk
#aqui van las interfaces de perfil tanto del nadador como del entrenandor
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def profile_swimmer():

    ventana = ctk.CTkToplevel()
    ventana.title("Perfil del Nadador")
    ventana.geometry("450x550")

    titulo = ctk.CTkLabel(ventana, text="Perfil del Nadador", font=("Arial",20,"bold"))
    titulo.pack(pady=10)

    nombre = ctk.CTkEntry(ventana, placeholder_text="Nombre")
    nombre.pack(pady=5)

    edad = ctk.CTkEntry(ventana, placeholder_text="Edad")
    edad.pack(pady=5)

    codigo = ctk.CTkEntry(ventana, placeholder_text="Código de acceso")
    codigo.pack(pady=5)

    genero = ctk.CTkOptionMenu(ventana, values=["Masculino","Femenino","Otro"])
    genero.pack(pady=5)

    peso = ctk.CTkEntry(ventana, placeholder_text="Peso (kg)")
    peso.pack(pady=5)

    estatura = ctk.CTkEntry(ventana, placeholder_text="Estatura (m)")
    estatura.pack(pady=5)

    respiratorio = ctk.CTkCheckBox(ventana, text="Problema respiratorio")
    respiratorio.pack(pady=5)

    entrenador = ctk.CTkEntry(ventana, placeholder_text="ID del entrenador")
    entrenador.pack(pady=5)


    def guarda():
        messagebox.showinfo("Info", "Nadador guardado (conectar a BD aquí)")


    def elimina():
        messagebox.showwarning("Info", "Nadador eliminado (conectar a BD aquí)")


    btn_guardar = ctk.CTkButton(ventana, text="Guardar", command=guarda)
    btn_guardar.pack(pady=10)

    btn_eliminar = ctk.CTkButton(ventana, text="Eliminar", fg_color="red", command=elimina)
    btn_eliminar.pack(pady=5)
