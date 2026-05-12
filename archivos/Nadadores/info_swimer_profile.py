import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import obtener_nadador_por_id, eliminar_nadador
from archivos.Animaciones.animacion_dado_baja import mostrar_splash_dado_baja
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.lesiones import puede_entrenar

def profile_swimmer(nadador, root):
    v = ctk.CTkToplevel(root)
    nadador_id = nadador["id"]
    nadador_nombre = nadador["nombre"]
    datos_completos = {} # Inicializar datos_completos aquí
    v.title("Cobaj Sports — Perfil")
    v.geometry("620x650")
    v.configure(fg_color="#0A1628")

    # ================= FONDO =================
    try:
        img_fondo = Image.open("Backgrounds/epic_background.png")
        fondo_lbl = ctk.CTkLabel(v, text="")
        fondo_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        def actualizar(event=None):
            w, h = v.winfo_width(), v.winfo_height()
            if w < 100 or h < 100:
                return
            resized = img_fondo.resize((w, h))
            v._bg_img = CTkImage(light_image=resized, size=(w, h))
            fondo_lbl.configure(image=v._bg_img)
            fondo_lbl.lower()
            card.lift()

        v.bind("<Configure>", actualizar)
        v.after(100, actualizar)
    except Exception as e:
        print("Error fondo:", e)

    # ================= CARD =================
    card = ctk.CTkFrame(v, width=450, height=616, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    # ================= AVATAR =================
    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36,
                      fg_color="#0072FF", border_width=2, border_color="#00C6FF")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="🏊", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    # ================= TITULO =================
    ctk.CTkLabel(cnt, text=f"{nadador_nombre}",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 2))

    ctk.CTkLabel(cnt, text="Perfil del Nadador",
                 font=ctk.CTkFont(size=13),
                 text_color="#AAB8C2").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#0072FF").pack(fill="x", padx=28, pady=8)

    # ================= CAMPOS =================
    campos_frame = ctk.CTkFrame(cnt, fg_color="transparent")
    campos_frame.pack(fill="x", padx=28, pady=(0, 8))

    def campo(placeholder, ancho=360):
        e = ctk.CTkEntry(campos_frame, placeholder_text=placeholder,
                         height=38, width=ancho, font=ctk.CTkFont(size=13))
        e.pack(pady=4)
        return e

    e_nombre   = campo("Nombre")
    e_edad     = campo("Edad")
    e_codigo   = campo("Código de acceso")

    genero_var = ctk.StringVar(value="Masculino")
    ctk.CTkOptionMenu(campos_frame, values=["Masculino", "Femenino", "Otro"],
                      variable=genero_var, width=360, height=38,
                      font=ctk.CTkFont(size=13)).pack(pady=4)

    e_peso     = campo("Peso (kg)")
    e_estatura = campo("Estatura (m)")

    prob_var   = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(campos_frame, text="Problema respiratorio",
                    variable=prob_var, font=ctk.CTkFont(size=13),
                    text_color="#AAB8C2").pack(pady=4, anchor="w")

    # Estatus Médico
    lbl_status_medico = ctk.CTkLabel(cnt, text="Estatus: Verificando...", font=ctk.CTkFont(size=14, weight="bold"))
    lbl_status_medico.pack(pady=(5, 5))

    # ================= CARGA DATOS =================
    def cargar_datos():
        data = obtener_nadador_por_id(nadador_id)
        if not data:
            return
        datos_completos["entrenador_id"] = data.get("entrenador_id")
        e_nombre.insert(0, data.get("nombre", ""))
        e_edad.insert(0, str(data.get("edad", "")))
        e_codigo.insert(0, data.get("codigo_acceso", ""))
        genero_var.set(data.get("genero", "Masculino"))
        e_peso.insert(0, str(data.get("peso", "")))
        e_estatura.insert(0, str(data.get("estatura", "")))
        prob_var.set(data.get("problema_respiratorio", False))

        # Consultar si el nadador tiene lesiones activas
        if puede_entrenar(nadador_id):
            lbl_status_medico.configure(text="Estatus: ✅ Apto para entrenar", text_color="#1ABC9C")
        else:
            lbl_status_medico.configure(text="Estatus: ❌ En recuperación / Lesionado", text_color="#E74C3C")

    cargar_datos()

    # ================= MENSAJE =================
    lbl = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=12))
    lbl.pack(pady=(0, 4))

    # ================= ELIMINAR =================
    def confirmar_eliminar():
        dialogo = ctk.CTkToplevel(v)
        dialogo.title("Confirmar")
        dialogo.geometry("360x180")
        dialogo.resizable(False, False)
        dialogo.configure(fg_color="#0F2040")
        dialogo.grab_set()
        dialogo.focus()

        ctk.CTkLabel(dialogo, text="¿Eliminar este nadador?",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#E8F4FD").pack(pady=(24, 8))

        ctk.CTkLabel(dialogo, text=nadador_nombre,
                     font=ctk.CTkFont(size=13),
                     text_color="#FF6B6B").pack(pady=(0, 20))

        btn_row = ctk.CTkFrame(dialogo, fg_color="transparent")
        btn_row.pack()

        def eliminar():
            ok = eliminar_nadador(nadador_id, datos_completos["entrenador_id"])
            dialogo.destroy()
            if ok:
                lbl.configure(text="✅ Nadador eliminado", text_color="#1ABC9C")
                mostrar_splash_dado_baja(v)
                v.after(1000, v.destroy)  # cierra el perfil después de 1.5s
            else:
                talk("Error al eliminar el nadador")
                lbl.configure(text="❌ Error al eliminar", text_color="red")

        ctk.CTkButton(btn_row, text="Sí, eliminar", fg_color="#E74C3C",
                      hover_color="#C0392B", width=130,
                      command=eliminar).pack(side="left", padx=8)

        ctk.CTkButton(btn_row, text="Cancelar", fg_color="#2C3E50",
                      hover_color="#1A252F", width=130,
                      command=dialogo.destroy).pack(side="left", padx=8)

    # ================= BOTONES =================
    btns = ctk.CTkFrame(cnt, fg_color="transparent")
    btns.pack(pady=(0, 20))

    ctk.CTkButton(btns, text="🗑️  Eliminar nadador", width=360, height=38,
                  fg_color="#E74C3C", hover_color="#C0392B",
                  font=ctk.CTkFont(size=13, weight="bold"),
                  command=confirmar_eliminar).pack(pady=(0, 6))

    ctk.CTkButton(btns, text="Cerrar", width=360, height=38,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=v.destroy).pack()