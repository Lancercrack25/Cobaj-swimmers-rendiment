#en este acrchivo se podra registrar a los nadadores, aqui se podran agregar los datos de cada nadador, como su nombre, edad, genero, etc. es como un registro de nadadores para el entrenador
import customtkinter as ctk
from tkinter import messagebox
from archivos.Asistente_voz.asistente import talk
import random
import string

#funcion para que genere un codigo aleatorio para cada nadador, este codigo sera unico para cada nadador y se utilizara para identificarlo en el sistema, este codigo se generara automaticamente al registrar un nuevo nadador, no se podra modificar ni eliminar, solo se podra generar uno nuevo si se elimina el nadador actual
def codigo_nadador(): 
    letras = string.ascii_uppercase
    numeros = string.digits
    codigo = ''.join(random.choice(letras + numeros) for _ in range(6))
    return codigo

