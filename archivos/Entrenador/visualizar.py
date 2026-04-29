import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from archivos.Asistente_voz.asistente import talk
from Backend.funcionamiento_logica_modulos.nadadores import obtener_nadadores,desvincular_nadador_entrenador
from archivos.Entrenador.mis_alumnos import equipo_actual
#aqui el entrenador podra registrar y ver a sus alumnos, aqui podra ver a los alumnos que tiene registrados, y registrar a nuevos alumnos, ademas de eliminar a los alumnos que ya no entrenan con el

def interfaz_ver_nadadores(entrenador, root):
    v = ctk.CTkToplevel(root)
    entrenador_id = entrenador["id"]
    entrenador_nombre = entrenador["nombre"]
    v.title("Cobaj Sports — Mi Equipo")
    v.geometry("520x650")
    v.configure(fg_color="#0A1628")

    # Sincroniza el arreglo con la BD al abrir
    equipo_actual.clear()
    equipo_actual.extend(obtener_nadadores(entrenador_id))

    # ================= FONDO =================
    try:
        img_fondo = Image.open("Backgrounds/fondo 6.png")
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
    card = ctk.CTkFrame(v, width=450, height=580, corner_radius=24,
                        fg_color="#0F2040", border_width=1, border_color="#1E4080")
    card.place(relx=0.5, rely=0.5, anchor="center")

    cnt = ctk.CTkFrame(card, fg_color="transparent")
    cnt.place(x=0, y=0, relwidth=1, relheight=1)

    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36,
                      fg_color="#0072FF", border_width=2, border_color="#00C6FF")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="🏊", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(cnt, text="Mi Equipo",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#0072FF").pack(fill="x", padx=28, pady=10)

    e_buscar = ctk.CTkEntry(cnt, placeholder_text="🔍  Buscar por nombre o código...",
                            height=40, font=ctk.CTkFont(size=13), width=360)
    e_buscar.pack(pady=(0, 10))

    lbl_contador = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=12), text_color="#AAB8C2")
    lbl_contador.pack(pady=(0, 6))

    lista_frame = ctk.CTkScrollableFrame(cnt, fg_color="#0A1A2A", corner_radius=12,
                                         border_width=1, border_color="#1E4080", height=280)
    lista_frame.pack(fill="x", padx=28, pady=(0, 10))

    def render(data):
        for w in lista_frame.winfo_children():
            w.destroy()

        lbl_contador.configure(
            text=f"{len(data)} nadador{'es' if len(data) != 1 else ''} en tu equipo")

        if not data:
            ctk.CTkLabel(lista_frame, text="No hay nadadores en tu equipo",
                         text_color="#AAB8C2", font=ctk.CTkFont(size=13)).pack(pady=20)
            return

        for i, n in enumerate(data):
            row = ctk.CTkFrame(lista_frame,
                               fg_color="#132440" if i % 2 == 0 else "#0F1E38",
                               corner_radius=8, height=44)
            row.pack(fill="x", pady=2, padx=4)
            row.pack_propagate(False)

            ctk.CTkLabel(row, text=f"{i+1:02d}", font=ctk.CTkFont(size=11),
                         text_color="#4A7AB5", width=30).pack(side="left", padx=(10, 4))

            ctk.CTkLabel(row, text="👤", font=("Arial", 14),
                         fg_color="transparent").pack(side="left", padx=(0, 8))

            ctk.CTkLabel(row, text=n["nombre"], font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#E8F4FD", anchor="w").pack(side="left", fill="x", expand=True)

            ctk.CTkButton(
                row, text="✕", width=28, height=28,
                fg_color="#8B0000", hover_color="#CC0000",
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda nid=n["id"]: eliminar(nid)
            ).pack(side="right", padx=(0, 6))

            badge = ctk.CTkFrame(row, fg_color="#0072FF", corner_radius=6)
            badge.pack(side="right", padx=4)
            ctk.CTkLabel(badge, text=n["codigo_acceso"],
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="white", padx=8, pady=2).pack()

    def eliminar(nadador_id):
        desvincular_nadador_entrenador(nadador_id, entrenador_id)  # ← limpia BD
        equipo_actual[:] = [n for n in equipo_actual if n["id"] != nadador_id]
        filtrar()

    def filtrar(event=None):
        txt = e_buscar.get().strip().lower()
        if txt:
            render([n for n in equipo_actual
                    if txt in n["nombre"].lower() or txt in n["codigo_acceso"].lower()])
        else:
            render(equipo_actual)

    e_buscar.bind("<KeyRelease>", filtrar)
    render(equipo_actual)

    ctk.CTkButton(cnt, text="Cerrar", width=360, height=42,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=v.destroy).pack(pady=(0, 20))