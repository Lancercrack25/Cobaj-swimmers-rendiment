import customtkinter as ctk
from Backend.asistente import talk

#interfaz que vera el usuario al ingresar, en este caso los nadadores
def interfaz_nadador():
    ventana = ctk.CTk()
    ventana.title("Bienvenido/a")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#212324")
    
    etiqueta_titulo = ctk.CTkLabel(ventana, text="Menu principal", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    boton_registro = ctk.CTkButton(ventana, text="Mi perfil", fg_color="#0AA5FF")
    boton_registro.pack(pady=8)

    estadisticas = ctk.CTkButton(ventana, text="consultar mis estadísticas ", fg_color="#C7A534")
    estadisticas.pack(pady=8)

    salir = ctk.CTkButton(ventana, text="Salir", fg_color="#BE1111", command=lambda: ventana.destroy())
    salir.pack(pady=8)

    ventana.mainloop()
