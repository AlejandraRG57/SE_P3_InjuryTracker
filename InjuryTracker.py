import tkinter as tk
from tkinter import PhotoImage, messagebox, simpledialog
import sqlite3
from PIL import Image, ImageTk
import os

# Inicializar la base de datos SQLite
def inicializar_base_datos():
    conn = sqlite3.connect("sintomas.db")
    cursor = conn.cursor()

    # Crear tabla de preguntas con parte_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parte_id INTEGER,
            texto TEXT NOT NULL,
            respuesta_si INTEGER,
            respuesta_no INTEGER,
            diagnostico_id INTEGER,
            FOREIGN KEY(parte_id) REFERENCES partes_cuerpo(id),
            FOREIGN KEY(diagnostico_id) REFERENCES diagnosticos(id)
        )
    """)

    # Crear tabla de partes del cuerpo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partes_cuerpo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)

    # Crear tabla de diagnósticos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            causas TEXT NOT NULL,
            tratamiento TEXT NOT NULL
        )
    """)

    # Insertar partes del cuerpo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM partes_cuerpo")
    if cursor.fetchone()[0] == 0:
        partes = ["Cabeza", "Hombro", "Columna", "Codo", "Cadera", "Muñeca", "Mano", 
                  "Rodilla", "Pierna", "Tobillo", "Pie"]
        cursor.executemany("INSERT INTO partes_cuerpo (nombre) VALUES (?)", [(parte,) for parte in partes])

    conn.commit()
    conn.close()

# Clase principal para el inicio de sesión
class InjuryTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("InjuryTracker - Inicio de Sesión")
        self.root.geometry("276x700")
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="InjuryTracker", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="Bienvenido!").pack(pady=5)

        tk.Label(frame, text="Usuario:").pack()
        self.usuario_entry = tk.Entry(frame)
        self.usuario_entry.pack()

        tk.Label(frame, text="Contraseña:").pack()
        self.contrasena_entry = tk.Entry(frame, show="*")
        self.contrasena_entry.pack()

        tk.Button(frame, text="Iniciar sesión", command=self.iniciar_sesion).pack(pady=10)

        self.root.mainloop()

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        if usuario == "admin" and contrasena == "admin123":
            messagebox.showinfo("Inicio de sesión", "Bienvenido, Administrador")
            self.root.destroy()
        elif usuario == "1" and contrasena == "1":
            messagebox.showinfo("Inicio de sesión", "Bienvenido, Usuario")
            self.root.destroy()
            ModoUsuario()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Clase para el modo usuario
class ModoUsuario:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Selecciona la parte del cuerpo")
        self.root.geometry("276x700")
        self.root.configure(bg="blue")

        self.canvas = tk.Canvas(self.root, width=276, height=700)
        self.canvas.pack(fill="both", expand=True)

        self.label_texto = tk.Label(self.root, text="¿Dónde sientes el malestar?", font=("Helvetica", 12, "bold"), fg="black")
        self.label_texto.place(x=27, y=10)

        try:
            self.bg_image = PhotoImage(file="cuerpo_humano.png")
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

        self.crear_boton("Cabeza", 30, 50)
        self.crear_boton("Hombro", 90, 150)
        self.crear_boton("Columna", 25, 200)
        self.crear_boton("Codo", 140, 240)
        self.crear_boton("Cadera", 60, 320)
        self.crear_boton("Muñeca", 170, 320)
        self.crear_boton("Mano", 170, 360)
        self.crear_boton("Rodilla", 70, 480)
        self.crear_boton("Pierna", 90, 560)
        self.crear_boton("Tobillo", 85, 630)
        self.crear_boton("Pie", 100, 660)

        cerrar_sesion_btn = tk.Button(self.root, text="Cerrar sesión", command=self.cerrar_sesion, bg="white")
        cerrar_sesion_btn.place(x=190, y=650)

        self.root.mainloop()

    def crear_boton(self, parte, x, y):
        boton = tk.Button(self.root, text=parte, command=lambda: self.iniciar_cuestionario(parte))
        boton.place(x=x, y=y)

    def iniciar_cuestionario(self, parte):
        self.root.destroy()
        Cuestionario(parte)

    def cerrar_sesion(self):
        self.root.destroy()
        InjuryTracker()

# Clase para manejar el cuestionario
class Cuestionario:
    def __init__(self, parte):
        self.parte = parte
        self.root = tk.Tk()
        self.root.title(f"Cuestionario - {parte}")
        self.root.geometry("276x700")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        try:
            self.imagenes_partes = {
                "Cabeza": "cabeza.png",
                "Hombro": "hombro.png",
                "Columna": "columna.png",
                "Codo": "codo.png",
                "Cadera": "cadera.png",
                "Muñeca": "muneca.png",
                "Mano": "mano.png",
                "Rodilla": "rodilla.png",
                "Pierna": "pierna.png",
                "Tobillo": "tobillo.png",
                "Pie": "pie.png"
            }
            image_file = self.imagenes_partes.get(parte, "default.png")
            if not os.path.exists(image_file):
                image_file = "default.png"
            original_image = Image.open(image_file)
            resized_image = original_image.resize((120, 120), Image.Resampling.LANCZOS)
            self.part_image = ImageTk.PhotoImage(resized_image)
            tk.Label(self.top_frame, image=self.part_image).pack()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

        tk.Label(self.top_frame, text=parte, font=("Helvetica", 16, "bold")).pack()

        self.conn = sqlite3.connect("sintomas.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT id FROM partes_cuerpo WHERE nombre=?", (parte,))
        parte_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT * FROM preguntas 
            WHERE parte_id=? AND id NOT IN (
                SELECT respuesta_si FROM preguntas WHERE respuesta_si IS NOT NULL 
                UNION 
                SELECT respuesta_no FROM preguntas WHERE respuesta_no IS NOT NULL)
        """, (parte_id,))
        self.nodo_actual = self.cursor.fetchone()

        self.pregunta_label = tk.Label(self.root, text="", font=("Helvetica", 14), wraplength=260, justify="center")
        self.pregunta_label.pack(pady=20)

        self.botones_frame = tk.Frame(self.root)
        self.botones_frame.pack(pady=20)
        self.si_button = tk.Button(self.botones_frame, text="Sí", command=self.responder_si, width=10)
        self.no_button = tk.Button(self.botones_frame, text="No", command=self.responder_no, width=10)
        self.si_button.pack(side=tk.LEFT, padx=10)
        self.no_button.pack(side=tk.RIGHT, padx=10)

        self.mostrar_pregunta()
        self.root.mainloop()

    def mostrar_pregunta(self):
        if self.nodo_actual is None:
            messagebox.showinfo("Error", "No hay preguntas registradas para esta parte del cuerpo.")
            self.root.destroy()
            InjuryTracker()
            return

        if self.nodo_actual[5]:  # Si tiene un diagnóstico
            self.root.destroy()
            VentanaDiagnostico(self.nodo_actual[5])
        else:
            self.pregunta_label.config(text=self.nodo_actual[2])

    def responder_si(self):
        if self.nodo_actual[3]:  # Si hay una pregunta ligada al "Sí"
            self.cursor.execute("SELECT * FROM preguntas WHERE id=?", (self.nodo_actual[3],))
            self.nodo_actual = self.cursor.fetchone()
            self.mostrar_pregunta()
        else:  # Si no hay una pregunta ligada al "Sí"
            self.manejar_pregunta_faltante(es_si=True)

    def responder_no(self):
        if self.nodo_actual[4]:  # Si hay una pregunta ligada al "No"
            self.cursor.execute("SELECT * FROM preguntas WHERE id=?", (self.nodo_actual[4],))
            self.nodo_actual = self.cursor.fetchone()
            self.mostrar_pregunta()
        else:  # Si no hay una pregunta ligada al "No"
            self.manejar_pregunta_faltante(es_si=False)

    def manejar_pregunta_faltante(self, es_si):
        # Preguntar al administrador si desea agregar un diagnóstico o una nueva pregunta
        contrasena = simpledialog.askstring("Autenticación", "Ingrese la contraseña de administrador para continuar:", show="*")
        if contrasena != "admin123":
            messagebox.showinfo("Acceso Denegado", "No hay más preguntas disponibles y no se puede agregar una nueva.")
            self.root.destroy()
            InjuryTracker()
            return

        opcion = messagebox.askquestion("Agregar contenido", "¿Desea agregar un diagnóstico en lugar de una nueva pregunta?")
        if opcion == "yes":
            # Agregar diagnóstico
            self.agregar_diagnostico(es_si)
        else:
            # Agregar nueva pregunta
            self.agregar_pregunta(es_si)

    def agregar_diagnostico(self, es_si):
        nuevo_diagnostico = simpledialog.askstring("Nuevo Diagnóstico", "Ingrese el texto del diagnóstico relacionado:")
        causas = simpledialog.askstring("Causas", "Ingrese las causas del diagnóstico:")
        tratamiento = simpledialog.askstring("Tratamiento", "Ingrese el tratamiento del diagnóstico:")
        if not nuevo_diagnostico or not causas or not tratamiento:
            messagebox.showerror("Error", "Debe ingresar todos los datos del diagnóstico.")
            return

        # Crear el diagnóstico en la tabla de diagnósticos
        self.cursor.execute("INSERT INTO diagnosticos (nombre, causas, tratamiento) VALUES (?, ?, ?)",
                            (nuevo_diagnostico, causas, tratamiento))
        diagnostico_id = self.cursor.lastrowid

        # Crear un nuevo nodo para este diagnóstico en la tabla de preguntas
        self.cursor.execute("INSERT INTO preguntas (parte_id, texto, diagnostico_id) VALUES (?, ?, ?)",
                            (self.nodo_actual[1], f"Diagnóstico: {nuevo_diagnostico}", diagnostico_id))
        id_nuevo_diagnostico = self.cursor.lastrowid

        # Enlazar el nodo de diagnóstico con la pregunta previa
        if es_si:
            self.cursor.execute("UPDATE preguntas SET respuesta_si=? WHERE id=?", (id_nuevo_diagnostico, self.nodo_actual[0]))
        else:
            self.cursor.execute("UPDATE preguntas SET respuesta_no=? WHERE id=?", (id_nuevo_diagnostico, self.nodo_actual[0]))

        self.conn.commit()
        messagebox.showinfo("Éxito", "Diagnóstico agregado correctamente.")
        self.root.destroy()
        InjuryTracker()


    def agregar_pregunta(self, es_si):
        nueva_pregunta = simpledialog.askstring("Nueva Pregunta", "Ingrese el texto de la nueva pregunta:")
        if not nueva_pregunta:
            messagebox.showerror("Error", "Debe ingresar una pregunta válida.")
            return

        # Insertar nueva pregunta
        self.cursor.execute("INSERT INTO preguntas (parte_id, texto) VALUES (?, ?)", (self.nodo_actual[1], nueva_pregunta))
        id_nueva_pregunta = self.cursor.lastrowid

        # Enlazar la nueva pregunta con la respuesta actual
        if es_si:
            self.cursor.execute("UPDATE preguntas SET respuesta_si=? WHERE id=?", (id_nueva_pregunta, self.nodo_actual[0]))
        else:
            self.cursor.execute("UPDATE preguntas SET respuesta_no=? WHERE id=?", (id_nueva_pregunta, self.nodo_actual[0]))

        self.conn.commit()
        messagebox.showinfo("Éxito", "Pregunta agregada correctamente.")
        self.root.destroy()
        InjuryTracker()

# Clase para mostrar el diagnóstico
class VentanaDiagnostico:
    def __init__(self, diagnostico_id):
        self.root = tk.Tk()
        self.root.title("Resultados")
        self.root.geometry("276x700")

        self.conn = sqlite3.connect("sintomas.db")
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.nombre, d.causas, d.tratamiento
            FROM diagnosticos d WHERE d.id = ?
        """, (diagnostico_id,))
        diagnostico = cursor.fetchone()
        self.conn.close()

        if diagnostico:
            self.top_frame = tk.Frame(self.root)
            self.top_frame.pack(pady=10)

            try:
                self.imagenes_partes = {
                    "Cabeza": "cabeza.png",
                    "Hombro": "hombro.png",
                    "Columna": "columna.png",
                    "Codo": "codo.png",
                    "Cadera": "cadera.png",
                    "Muñeca": "muneca.png",
                    "Mano": "mano.png",
                    "Rodilla": "rodilla.png",
                    "Pierna": "pierna.png",
                    "Tobillo": "tobillo.png",
                    "Pie": "pie.png"
                }
                image_file = "default.png"
                original_image = Image.open(image_file)
                resized_image = original_image.resize((120, 120), Image.Resampling.LANCZOS)
                self.part_image = ImageTk.PhotoImage(resized_image)
                tk.Label(self.top_frame, image=self.part_image).pack()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

            # Texto ajustado con wraplength proporcional al ancho de la ventana
            tk.Label(self.root, text="En base a sus resultados usted puede padecer:", 
                     font=("Helvetica", 12, "bold"), 
                     justify="center", 
                     wraplength=250).pack(pady=5)
            
            tk.Label(self.root, text=diagnostico[0], 
                     font=("Helvetica", 14, "bold"), 
                     fg="blue", 
                     wraplength=250, 
                     justify="center").pack(pady=5)

            tk.Label(self.root, text="Le recomendamos consultar a un médico", 
                     font=("Helvetica", 10), 
                     justify="center", 
                     wraplength=250).pack(pady=5)

            causas_label = tk.Label(self.root, text="Causas:", font=("Helvetica", 12, "bold"), anchor="w")
            causas_label.pack(fill="x", pady=5)
            causas_frame = tk.Frame(self.root)
            causas_frame.pack(fill="both", expand=True, pady=5)
            causas_text = tk.Text(causas_frame, wrap="word", height=6, font=("Helvetica", 10), bg="white")
            causas_scroll = tk.Scrollbar(causas_frame, command=causas_text.yview)
            causas_text.insert("1.0", diagnostico[1])
            causas_text.configure(state="disabled", yscrollcommand=causas_scroll.set)
            causas_text.pack(side="left", fill="both", expand=True)
            causas_scroll.pack(side="right", fill="y")

            tratamiento_label = tk.Label(self.root, text="Tratamiento:", font=("Helvetica", 12, "bold"), anchor="w")
            tratamiento_label.pack(fill="x", pady=5)
            tratamiento_frame = tk.Frame(self.root)
            tratamiento_frame.pack(fill="both", expand=True, pady=5)
            tratamiento_text = tk.Text(tratamiento_frame, wrap="word", height=6, font=("Helvetica", 10), bg="white")
            tratamiento_scroll = tk.Scrollbar(tratamiento_frame, command=tratamiento_text.yview)
            tratamiento_text.insert("1.0", diagnostico[2])
            tratamiento_text.configure(state="disabled", yscrollcommand=tratamiento_scroll.set)
            tratamiento_text.pack(side="left", fill="both", expand=True)
            tratamiento_scroll.pack(side="right", fill="y")

            tk.Button(self.root, text="Página Principal", command=self.volver_principal, bg="lightblue").pack(pady=20)
        else:
            messagebox.showerror("Error", "Diagnóstico no encontrado.")
            self.volver_principal()

        self.root.mainloop()

    def volver_principal(self):
        self.root.destroy()
        InjuryTracker()


# Inicializar base de datos y ejecutar la aplicación
inicializar_base_datos()
InjuryTracker()