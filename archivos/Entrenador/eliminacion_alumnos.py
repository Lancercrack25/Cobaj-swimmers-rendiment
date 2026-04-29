#aqui el entrenador podra eliminar que alumnos ya no estan entrenando con el
import customtkinter as ctk
from archivos.Asistente_voz.asistente import talk
from PIL import Image, ImageFilter
from customtkinter import CTkImage
from Backend.funcionamiento_logica_modulos.nadadores import desvincular_nadador_entrenador, obtener_nadadores
from archivos.Entrenador.mis_alumnos import equipo_actual
#aqui el entrenador podra eliminar que alumnos ya no estan entrenando con el, se mostrara una lista de los alumnos registrados y se podra seleccionar uno para eliminarlo, ademas de que se mostrara un mensaje de confirmacion antes de eliminar al alumno
def interfaz_eliminar_nadador(entrenador, root):
    v = ctk.CTkToplevel(root)
    entrenador_id = entrenador["id"]
    entrenador_nombre = entrenador["nombre"]
    v.title("Cobaj Sports — Eliminar Nadador")
    v.geometry("520x650")
    v.configure(fg_color="#0A1628")

    # Sincroniza el arreglo con la BD al abrir
    equipo_actual.clear()
    equipo_actual.extend(obtener_nadadores(entrenador_id))

    # ================= FONDO =================
    try:
        img_fondo = Image.open("Backgrounds/fondo12.webp")
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

    # ================= AVATAR =================
    av = ctk.CTkFrame(cnt, width=72, height=72, corner_radius=36,
                      fg_color="#E74C3C", border_width=2, border_color="#FF6B6B")
    av.pack(pady=(24, 8))
    av.pack_propagate(False)
    ctk.CTkLabel(av, text="🗑️", font=("Arial", 28),
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")

    # ================= TITULO =================
    ctk.CTkLabel(cnt, text="Eliminar Nadador",
                 font=ctk.CTkFont(size=22, weight="bold"),
                 text_color="#E8F4FD").pack(pady=(0, 4))

    ctk.CTkFrame(cnt, height=2, fg_color="#E74C3C").pack(fill="x", padx=28, pady=10)

    # ================= BUSCADOR =================
    search_frame = ctk.CTkFrame(cnt, fg_color="transparent")
    search_frame.pack(fill="x", padx=28, pady=(0, 8))

    e_buscar = ctk.CTkEntry(search_frame, placeholder_text="Buscar por nombre o código...",
                            height=40, font=ctk.CTkFont(size=13))
    e_buscar.pack(side="left", fill="x", expand=True, padx=(0, 8))

    # ================= LISTA =================
    lista_frame = ctk.CTkScrollableFrame(cnt, fg_color="#0A1A2A", corner_radius=12,
                                         border_width=1, border_color="#1E4080", height=220)
    lista_frame.pack(fill="x", padx=28, pady=(0, 10))

    seleccionado = {"id": None, "nombre": None, "btn": None}

    def render(filtro=""):
        for w in lista_frame.winfo_children():
            w.destroy()
        seleccionado["id"] = None
        seleccionado["nombre"] = None
        seleccionado["btn"] = None
        lbl_confirmacion.configure(text="")

        filtro_lower = filtro.lower()
        filtrados = [
            n for n in equipo_actual
            if filtro_lower in n["nombre"].lower()
            or filtro_lower in n["codigo_acceso"].lower()
        ] if filtro else list(equipo_actual)

        if not filtrados:
            ctk.CTkLabel(lista_frame, text="No hay nadadores en tu equipo",
                         text_color="#AAB8C2", font=ctk.CTkFont(size=13)).pack(pady=20)
            return

        for n in filtrados:
            def sel(i=n["id"], nombre=n["nombre"], codigo=n["codigo_acceso"], btn_ref=[None]):
                if seleccionado["btn"]:
                    seleccionado["btn"].configure(fg_color="#132440", hover_color="#1A3255")
                seleccionado["id"] = i
                seleccionado["nombre"] = nombre
                btn_ref[0].configure(fg_color="#4A1010", hover_color="#5A1515")
                seleccionado["btn"] = btn_ref[0]
                lbl_confirmacion.configure(
                    text=f"Seleccionado: {nombre} ({codigo})",
                    text_color="#F39C12"
                )

            btn = ctk.CTkButton(lista_frame,
                                text=f"👤  {n['nombre']}   •   {n['codigo_acceso']}",
                                font=ctk.CTkFont(size=13), fg_color="#132440",
                                hover_color="#1A3255", anchor="w", height=36, corner_radius=8)
            btn.configure(command=lambda b=btn, i=n["id"], nombre=n["nombre"],
                          codigo=n["codigo_acceso"]: sel(i, nombre, codigo, btn_ref=[b]))
            btn.pack(fill="x", pady=3, padx=4)

    def on_buscar(event=None):
        render(e_buscar.get().strip())

    e_buscar.bind("<KeyRelease>", on_buscar)

    ctk.CTkButton(search_frame, text="🔍", width=40, height=40,
                  fg_color="#0072FF", hover_color="#005FCC",
                  corner_radius=8, command=on_buscar).pack(side="left")

    lbl_confirmacion = ctk.CTkLabel(cnt, text="", font=ctk.CTkFont(size=12))
    lbl_confirmacion.pack(pady=(0, 6))

    render()

    # ================= DIALOGO CONFIRMACION =================
    def confirmar_eliminar():
        if not seleccionado["id"]:
            talk("Debes de seleccionar un nadador primero")
            lbl_confirmacion.configure(text="⚠️ Selecciona un nadador primero",
                                       text_color="#F39C12")
            return

        dialogo = ctk.CTkToplevel(v)
        dialogo.title("Confirmar eliminación")
        dialogo.geometry("360x200")
        dialogo.resizable(False, False)
        dialogo.configure(fg_color="#0F2040")
        dialogo.grab_set()
        dialogo.focus()

        ctk.CTkLabel(dialogo, text="¿Eliminar nadador del equipo?",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#E8F4FD").pack(pady=(24, 8))

        ctk.CTkLabel(dialogo, text=f"{seleccionado['nombre']}",
                     font=ctk.CTkFont(size=13),
                     text_color="#FF6B6B").pack(pady=(0, 20))

        btn_row = ctk.CTkFrame(dialogo, fg_color="transparent")
        btn_row.pack()

        def confirmar():
            # ← desvincula de BD y elimina del arreglo
            desvincular_nadador_entrenador(seleccionado["id"], entrenador_id)
            equipo_actual[:] = [n for n in equipo_actual if n["id"] != seleccionado["id"]]
            dialogo.destroy()
            lbl_confirmacion.configure(text="✅ Nadador eliminado del equipo",
                                       text_color="#1ABC9C")
            talk(f"El nadador {seleccionado['nombre']} ha sido eliminado del equipo")
            render(e_buscar.get().strip())

        ctk.CTkButton(btn_row, text="Sí, eliminar", fg_color="#E74C3C",
                      hover_color="#C0392B", width=130, command=confirmar).pack(side="left", padx=8)

        ctk.CTkButton(btn_row, text="Cancelar", fg_color="#2C3E50",
                      hover_color="#1A252F", width=130,
                      command=dialogo.destroy).pack(side="left", padx=8)

    # ================= BOTONES =================
    ctk.CTkButton(cnt, text="🗑️  Eliminar seleccionado", width=360, height=42,
                  font=ctk.CTkFont(size=14, weight="bold"),
                  fg_color="#E74C3C", hover_color="#C0392B",
                  command=confirmar_eliminar).pack(pady=(4, 6))

    ctk.CTkButton(cnt, text="Cerrar", width=360, height=42,
                  fg_color="#2C3E50", hover_color="#1A252F",
                  command=v.destroy).pack(pady=(0, 20))