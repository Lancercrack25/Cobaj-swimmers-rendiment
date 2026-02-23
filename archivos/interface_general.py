import customtkinter as ctk
from archivos.Registro_Entrenador import eliminacion, registro
from archivos.Registros_entrenamientos import registros_rachas
from interface_stadistics import interfaz_estadisticas
from Backend.asistente import talk


def interfaz_general():
    ventana = ctk.CTk()
    ventana.title("Interfaz General")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#3D4246")
    
    etiqueta_titulo = ctk.CTkLabel(ventana, text="Menu principal", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    boton_registro = ctk.CTkButton(ventana, text="Registrar de nadador", fg_color="#0A84FF", command=registro)
    boton_registro.pack(pady=10)

    estadisticas = ctk.CTkButton(ventana, text="Ver estadísticas del nadador", fg_color="#34C759", command=interfaz_estadisticas)
    estadisticas.pack(pady=12)

    eliminar = ctk.CTkButton(ventana, text="Eliminar nadador", fg_color="#FF3B30", command=lambda: eliminacion())
    eliminar.pack(pady=12)

    rachas = ctk.CTkButton(ventana, text="registro de rendimiento de nadador", fg_color="#AF52DE", command=registros_rachas)
    rachas.pack(pady=12)

    salir = ctk.CTkButton(ventana, text="Salir", fg_color="#8E8E93", command=lambda: ventana.destroy())
    salir.pack(pady=12)

    ventana.mainloop()