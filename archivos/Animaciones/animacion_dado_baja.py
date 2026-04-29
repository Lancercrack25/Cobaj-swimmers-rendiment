#este archivo mostrara una animacion como el splash pero cuando el nadador se de de baja de la app, es decir que cuando el nadador ya no este lleno el mismo se borre del sistema y aparezca esta animacion para mostrar que se dio de baja exitosamente
import customtkinter as ctk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk

# ================= SPLASH para animacion dado de baja =================
#ancho y alto de la ventana del splash
W, H = 480, 520

def mostrar_splash_dado_baja(ventana):
    splash = ctk.CTkToplevel()
    splash.overrideredirect(True)  # sin bordes ni barra de titulo
    splash.geometry(f"{W}x{H}+{(splash.winfo_screenwidth()-W)//2}+{(splash.winfo_screenheight()-H)//2}")

    img_splash = Image.open("Backgrounds/despedidas.png").resize((W, H))
    bg_splash = CTkImage(light_image=img_splash, size=(W, H))
    splash.bg_splash = bg_splash

    label = ctk.CTkLabel(splash, image=bg_splash, text="")
    label.place(x=0, y=0, relwidth=1, relheight=1)
    talk("Nadador dado de baja exitosamente")
    talk("Gracias por haber sido parte de Cobaj Sports, esperamos verte pronto de nuevo")
    splash.after(3000, lambda: (splash.destroy(), ventana.deiconify()))
    splash.mainloop()