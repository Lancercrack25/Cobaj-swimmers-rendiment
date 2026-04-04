import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk

# ================= SPLASH SCREEN =================
#ancho y alto de la ventana del splash
W, H = 480, 520

def mostrar_splash(ventana):
    splash = ctk.CTkToplevel()
    splash.overrideredirect(True)  # sin bordes ni barra de titulo
    splash.geometry(f"{W}x{H}+{(splash.winfo_screenwidth()-W)//2}+{(splash.winfo_screenheight()-H)//2}")

    img_splash = Image.open("Backgrounds/cobaj.png").resize((W, H))  # cambia por tu archivo de logo
    bg_splash = CTkImage(light_image=img_splash, size=(W, H))
    splash.bg_splash = bg_splash

    label = ctk.CTkLabel(splash, image=bg_splash, text="")
    label.place(x=0, y=0, relwidth=1, relheight=1)
    talk("Inicializando aplicación")
    splash.after(3000, lambda: (splash.destroy(), ventana.deiconify()))
    splash.mainloop()