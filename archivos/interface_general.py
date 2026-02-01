import customtkinter as ctk
from Registro_manco import eliminacion, registro
from Registros_papeos import registros_rachas
from interface_stadistics import interfaz_estadisticas


def interfaz_general():
    ventana = ctk.CTk()
    ventana.title("Interfaz General")
    ventana.geometry("550x450")
    ventana.configure(fg_color="#3D4246")
    
    etiqueta_titulo = ctk.CTkLabel(ventana, text="Menu principal", font=ctk.CTkFont(size=20, weight="bold"))
    etiqueta_titulo.pack(pady=8)

    boton_registro = ctk.CTkButton(ventana, text="Registrar de Jugador", fg_color="#0A84FF", command=registro)
    boton_registro.pack(pady=10)

    estadisticas = ctk.CTkButton(ventana, text="Ver estadísticas del jugador", fg_color="#34C759", command=interfaz_estadisticas)
    estadisticas.pack(pady=12)

    eliminar = ctk.CTkButton(ventana, text="Eliminar jugador", fg_color="#FF3B30", command=lambda: eliminacion())
    eliminar.pack(pady=12)

    rachas = ctk.CTkButton(ventana, text="registro de rachas victorias/derrotas", fg_color="#AF52DE", command=registros_rachas)
    rachas.pack(pady=12)

    salir = ctk.CTkButton(ventana, text="Salir", fg_color="#8E8E93", command=lambda: ventana.destroy())
    salir.pack(pady=12)

    ventana.mainloop()