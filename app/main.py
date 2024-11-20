import tkinter as tk
from tkinter import ttk, messagebox
from usuario import Usuario
from database import Database
import csv
from tkinter.filedialog import askopenfilename
import time  
from threading import Timer  
from tkcalendar import Calendar
from informe import generar_informe


# Inicialización de la base de datos
db = Database()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Encuestas")
        self.geometry("500x400")
        self.usuario_activo = None  # Usuario autenticado
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        """Muestra el menú principal con opciones para iniciar sesión o registrarse."""
        self.clear_window()
        ttk.Label(self, text="Bienvenido al Sistema de Encuestas", font=("Helvetica", 16)).pack(pady=20)

        # Botón para iniciar sesión
        self.login_button = ttk.Button(self, text="Iniciar Sesión", command=self.mostrar_login_screen)
        self.login_button.pack(pady=10)

        # Botón para registrarse
        self.register_button = ttk.Button(self, text="Registrarse", command=self.mostrar_registro_usuario)
        self.register_button.pack(pady=10)

    def clear_window(self):
        """Limpia todos los widgets de la ventana actual."""
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login_screen(self):
        """Muestra la pantalla de inicio de sesión."""
        LoginScreen(self)

    def mostrar_registro_usuario(self):
        """Muestra la pantalla de registro de usuario."""
        RegisterScreen(self)

    def mostrar_pantalla_principal(self):
        """Muestra la pantalla principal después del inicio de sesión."""
        self.clear_window()
        self.title(f"Bienvenido, {self.usuario_activo.username}")
        ttk.Label(self, text=f"Hola, {self.usuario_activo.username} ({self.usuario_activo.rol})",
                  font=("Helvetica", 16)).pack(pady=20)

        # Botón para gestionar encuestas
        self.encuesta_button = ttk.Button(self, text="Gestión de Encuestas", command=self.mostrar_encuesta_screen)
        self.encuesta_button.pack(pady=10)

         # Botón para cargar participantes
        self.cargar_participantes_button = ttk.Button(self, text="Cargar Participantes", command=self.mostrar_cargar_participantes_screen)
        self.cargar_participantes_button.pack(pady=10)

        # Botón para editar preguntas
        self.editar_preguntas_button = ttk.Button(self, text="Editar Preguntas", command=self.mostrar_editar_preguntas)
        self.editar_preguntas_button.pack(pady=10)

        # Botón para consultar encuestas
        self.consultar_encuestas_button = ttk.Button(self, text="Consultar Encuestas", command=self.mostrar_consulta_encuestas)
        self.consultar_encuestas_button.pack(pady=10)

        # Botón para cerrar sesión
        self.logout_button = ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion)
        self.logout_button.pack(pady=10)

        self.segmentacion_button = ttk.Button(self, text="Segmentar Participantes", command=self.mostrar_segmentacion)
        self.segmentacion_button.pack(pady=10)

        self.cargar_desde_crm_button = ttk.Button(
        self, text="Cargar Participantes desde CRM", command=self.mostrar_cargar_participantes_desde_crm
)
        self.cargar_desde_crm_button.pack(pady=10)

        ttk.Button(self, text="Ver Encuestas Cerradas", command=self.mostrar_encuestas_cerradas).pack(pady=10)


    
    def mostrar_cargar_participantes_desde_crm(self):
        """Muestra la pantalla para cargar participantes desde un archivo CSV del CRM."""
        CargarParticipantesDesdeCRM(self)

    def mostrar_segmentacion(self):
        """Muestra la pantalla para segmentar participantes."""
        SegmentacionScreen(self)


    def mostrar_cargar_participantes_screen(self):
       """Muestra la pantalla para cargar participantes desde un CSV."""
       CargarParticipantesScreen(self)

    def mostrar_consulta_encuestas(self):
        """Muestra la pantalla para consultar encuestas."""
        ConsultaEncuestasScreen(self)

    def mostrar_encuesta_screen(self):
        """Muestra la pantalla de gestión de encuestas."""
        EncuestaScreen(self)  # Asegúrate de que EncuestaScreen esté definida o importada.

    def mostrar_editar_preguntas(self):
        """Muestra la pantalla para editar preguntas."""
        EditPreguntaScreen(self)

    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al menú principal."""
        self.usuario_activo = None
        self.mostrar_menu_principal()
    
    def mostrar_encuestas_cerradas(self):
        """Muestra las encuestas cerradas en un cuadro de diálogo."""
        encuestas_cerradas = db.listar_encuestas_cerradas()
        if encuestas_cerradas:
            lista = "\n".join([f"{titulo} (Cerrada el: {fecha})" for titulo, fecha in encuestas_cerradas])
            messagebox.showinfo("Encuestas Cerradas", lista)
        else:
            messagebox.showinfo("Encuestas Cerradas", "No hay encuestas cerradas.")



class EditPreguntaScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Editar Preguntas")
        self.geometry("600x400")
        self.parent = parent
        self.preguntas = []
        self.init_ui()

    def init_ui(self):
        """Interfaz para editar preguntas."""
        ttk.Label(self, text="Lista de Preguntas").pack(pady=5)

        # Listbox para mostrar preguntas existentes
        self.listbox_preguntas = tk.Listbox(self, width=50, height=10)
        self.listbox_preguntas.pack(pady=5)
        self.cargar_preguntas()

        self.btn_editar = ttk.Button(self, text="Editar Pregunta", command=self.editar_pregunta)
        self.btn_editar.pack(pady=5)

    def cargar_preguntas(self):
        """Carga las preguntas del banco y las muestra en el Listbox."""
        self.preguntas = db.obtener_preguntas()
        for pregunta in self.preguntas:
            self.listbox_preguntas.insert(tk.END, f"{pregunta[1]} ({pregunta[2]})")

    def editar_pregunta(self):
        """Abre la ventana para editar la pregunta seleccionada."""
        seleccion = self.listbox_preguntas.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una pregunta para editar.")
            return

        index = seleccion[0]
        pregunta = self.preguntas[index]
        EditarPreguntaDetalles(self, pregunta)


class EditarPreguntaDetalles(tk.Toplevel):
    def __init__(self, parent, pregunta):
        super().__init__(parent)
        self.title("Editar Detalles de la Pregunta")
        self.geometry("400x300")
        self.parent = parent
        self.pregunta = pregunta
        self.init_ui()

    def init_ui(self):
        """Interfaz para editar detalles de una pregunta."""
        ttk.Label(self, text="Texto de la Pregunta:").pack(pady=5)
        self.texto_entry = ttk.Entry(self, width=50)
        self.texto_entry.insert(0, self.pregunta[1])  # Texto de la pregunta
        self.texto_entry.pack(pady=5)

        ttk.Label(self, text="Tipo de Respuesta:").pack(pady=5)
        self.tipo_entry = ttk.Entry(self, width=50)
        self.tipo_entry.insert(0, self.pregunta[2])  # Tipo de respuesta
        self.tipo_entry.pack(pady=5)

        ttk.Label(self, text="Opciones (separadas por comas):").pack(pady=5)
        self.opciones_entry = ttk.Entry(self, width=50)
        self.opciones_entry.insert(0, self.pregunta[3] if self.pregunta[3] else "")  # Opciones
        self.opciones_entry.pack(pady=5)

        self.btn_guardar = ttk.Button(self, text="Guardar Cambios", command=self.guardar_cambios)
        self.btn_guardar.pack(pady=10)

    def guardar_cambios(self):
        """Guarda los cambios realizados en la pregunta."""
        nuevo_texto = self.texto_entry.get()
        nuevo_tipo = self.tipo_entry.get()
        nuevas_opciones = self.opciones_entry.get()

        if not nuevo_texto or not nuevo_tipo:
            messagebox.showwarning("Advertencia", "El texto y el tipo de respuesta son obligatorios.")
            return

        # Actualizar la pregunta en la base de datos
        db.actualizar_pregunta(self.pregunta[0], nuevo_texto, nuevo_tipo, nuevas_opciones)
        messagebox.showinfo("Éxito", "Pregunta actualizada correctamente.")
        self.destroy()
        self.parent.cargar_preguntas()  # Actualizar la lista de preguntas

class LoginScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Iniciar Sesión")
        self.geometry("400x300")
        self.parent = parent

        ttk.Label(self, text="Nombre de Usuario:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.btn_iniciar = ttk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.btn_iniciar.pack(pady=10)

    def iniciar_sesion(self):
        """Valida las credenciales del usuario."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        usuario_data = db.obtener_usuario(username)
        if usuario_data:
            _, _, password_hash, rol_nombre = usuario_data
            if Usuario.verificar_password(password, password_hash):
                self.parent.usuario_activo = Usuario(username, password_hash, rol_nombre)
                messagebox.showinfo("Éxito", f"Bienvenido, {username}.\nRol: {rol_nombre}")
                self.destroy()
                self.parent.mostrar_pantalla_principal()
                return

        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


class RegisterScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Usuario")
        self.geometry("400x300")
        self.parent = parent

        ttk.Label(self, text="Nombre de Usuario:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        ttk.Label(self, text="Rol:").pack(pady=5)
        roles = db.obtener_roles()
        self.roles_combobox = ttk.Combobox(self, values=[rol[1] for rol in roles])
        self.roles_combobox.pack(pady=5)

        self.btn_guardar = ttk.Button(self, text="Guardar Usuario", command=self.guardar_usuario)
        self.btn_guardar.pack(pady=10)

    def guardar_usuario(self):
        """Guarda un nuevo usuario en la base de datos."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        rol_nombre = self.roles_combobox.get()

        if not username or not password or not rol_nombre:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        rol_id = next((rol[0] for rol in db.obtener_roles() if rol[1] == rol_nombre), None)
        if not rol_id:
            messagebox.showerror("Error", "Rol seleccionado no válido.")
            return

        password_hash = Usuario.hash_password(password)
        try:
            db.agregar_usuario(username, password_hash, rol_id)
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {str(e)}")
class VersionesEncuestaScreen(tk.Toplevel):
    def __init__(self, parent, titulo):
        super().__init__(parent)
        self.title(f"Versiones de Encuesta: {titulo}")
        self.geometry("600x300")
        self.titulo = titulo
        self.init_ui()

    def init_ui(self):
        """Interfaz para mostrar versiones de una encuesta."""
        ttk.Label(self, text=f"Versiones de '{self.titulo}'", font=("Helvetica", 14)).pack(pady=10)

        # Listbox para mostrar las versiones
        self.listbox_versiones = tk.Listbox(self, height=10, width=50)
        self.listbox_versiones.pack(pady=10)
        self.cargar_versiones()

    def cargar_versiones(self):
        """Carga todas las versiones de la encuesta seleccionada."""
        versiones = db.obtener_encuestas_por_titulo(self.titulo)
        for version in versiones:
            self.listbox_versiones.insert(
                tk.END, f"Versión {version[3]} - Creado en: {version[4]}"
            )


class ConsultaEncuestasScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Consulta de Encuestas")
        self.geometry("600x500")
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Interfaz para listar encuestas y consultar versiones."""
        ttk.Label(self, text="Consulta de Encuestas", font=("Helvetica", 16)).pack(pady=10)

        # Listbox para mostrar los títulos y estados de las encuestas
        self.listbox_titulos = tk.Listbox(self, height=15, width=70)
        self.listbox_titulos.pack(pady=10)
        self.cargar_titulos_encuestas()

        # Botón para ver versiones de una encuesta seleccionada
        self.btn_ver_versiones = ttk.Button(self, text="Ver Versiones", command=self.ver_versiones)
        self.btn_ver_versiones.pack(pady=5)

        # Botón para cambiar el estado de una encuesta seleccionada
        self.btn_cambiar_estado = ttk.Button(self, text="Cambiar Estado", command=self.cambiar_estado)
        self.btn_cambiar_estado.pack(pady=5)

        # Botón para cerrar la ventana
        self.btn_cerrar = ttk.Button(self, text="Cerrar", command=self.destroy)
        self.btn_cerrar.pack(pady=5)

    def cargar_titulos_encuestas(self):
        """Carga los títulos únicos de las encuestas en el Listbox, mostrando su estado."""
        self.listbox_titulos.delete(0, tk.END)  # Limpia el Listbox
        titulos = db.obtener_titulos_encuestas()  # Método actualizado en la base de datos
        for titulo, estado in titulos:
            self.listbox_titulos.insert(tk.END, f"{titulo} ({estado})")


        if not titulos:
            self.listbox_titulos.insert(tk.END, "No hay encuestas disponibles.")
            return

        for titulo, estado in titulos:
            self.listbox_titulos.insert(tk.END, f"{titulo} - Estado: {estado}")

    def ver_versiones(self):
        """Muestra las versiones de la encuesta seleccionada."""
        seleccion = self.listbox_titulos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un título de encuesta.")
            return

        titulo = self.listbox_titulos.get(seleccion).split(" - ")[0]  # Extrae solo el título
        VersionesEncuestaScreen(self, titulo)

    def cambiar_estado(self):
        """Cambia el estado de la encuesta seleccionada entre 'borrador' y 'publicada'."""
        seleccion = self.listbox_titulos.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una encuesta para cambiar su estado.")
            return

        titulo = self.listbox_titulos.get(seleccion).split(" - ")[0]  # Extrae solo el título
        estado_actual = "borrador" if "borrador" in self.listbox_titulos.get(seleccion) else "publicada"
        nuevo_estado = "publicada" if estado_actual == "borrador" else "borrador"

        # Actualizar el estado en la base de datos
        db.actualizar_estado_encuesta(titulo, nuevo_estado)
        messagebox.showinfo("Éxito", f"El estado de la encuesta '{titulo}' ha sido cambiado a '{nuevo_estado}'.")

        # Recargar los títulos con los nuevos estados
        self.cargar_titulos_encuestas()



class EncuestaScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Encuestas")
        self.geometry("500x500")
        self.parent = parent
        self.preguntas_seleccionadas = []
        self.init_ui()

    def init_ui(self):
        """Interfaz para crear encuestas."""
        ttk.Label(self, text="Título de la Encuesta:").pack(pady=5)
        self.titulo_entry = ttk.Entry(self)
        self.titulo_entry.pack(pady=5)

        ttk.Label(self, text="Banco de Preguntas:").pack(pady=5)

        # Banco de preguntas (Listbox)
        self.banco_preguntas = tk.Listbox(self, selectmode="multiple", height=10)
        self.banco_preguntas.pack(pady=5, fill="x")
        self.cargar_preguntas()

        # Botón para seleccionar preguntas
        self.btn_agregar_pregunta = ttk.Button(self, text="Agregar Preguntas Seleccionadas",
                                               command=self.seleccionar_preguntas)
        self.btn_agregar_pregunta.pack(pady=5)

        # Selector de estado
        ttk.Label(self, text="Estado de la Encuesta:").pack(pady=5)
        self.estado_combobox = ttk.Combobox(self, values=["borrador", "publicada"])
        self.estado_combobox.set("borrador")  # Estado por defecto
        self.estado_combobox.pack(pady=5)

        # Selector de fecha de cierre
        ttk.Label(self, text="Fecha de Cierre:").pack(pady=5)
        self.fecha_cierre_calendar = Calendar(self, date_pattern="y-mm-dd")
        self.fecha_cierre_calendar.pack(pady=5)

        # Botón para guardar encuesta
        self.btn_guardar_encuesta = ttk.Button(self, text="Guardar Encuesta", command=self.guardar_encuesta)
        self.btn_guardar_encuesta.pack(pady=10)

    def cargar_preguntas(self):
        """Carga las preguntas predefinidas en el Listbox."""
        preguntas = db.obtener_preguntas()
        for pregunta in preguntas:
            self.banco_preguntas.insert(tk.END, f"{pregunta[1]} ({pregunta[2]})")

    def seleccionar_preguntas(self):
        """Selecciona preguntas del banco."""
        seleccion = self.banco_preguntas.curselection()
        preguntas = db.obtener_preguntas()
        self.preguntas_seleccionadas = [preguntas[i] for i in seleccion]
        messagebox.showinfo("Éxito", "Preguntas seleccionadas correctamente.")

    def guardar_encuesta(self):
        """Guarda la encuesta como borrador o publicada."""
        titulo = self.titulo_entry.get()
        estado = self.estado_combobox.get()
        fecha_cierre = self.fecha_cierre_calendar.get_date()

        if not titulo:
            messagebox.showwarning("Advertencia", "El título es obligatorio.")
            return

        if not self.preguntas_seleccionadas:
            messagebox.showwarning("Advertencia", "Seleccione al menos una pregunta.")
            return

        # Crear una nueva encuesta con el estado seleccionado y la fecha de cierre
        preguntas_ids = [pregunta[0] for pregunta in self.preguntas_seleccionadas]
        db.agregar_encuesta(titulo, preguntas_ids, estado, fecha_cierre)
        messagebox.showinfo("Éxito", f"Encuesta '{titulo}' guardada como '{estado}' con cierre en {fecha_cierre}.")
        self.destroy()


class CargarParticipantesScreen(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cargar Participantes desde CSV")
        self.geometry("500x300")
        self.init_ui()

    def init_ui(self):
        """Interfaz para cargar un archivo CSV."""
        ttk.Label(self, text="Cargar Participantes desde un archivo CSV", font=("Helvetica", 16)).pack(pady=10)

        # Botón para seleccionar archivo CSV
        self.btn_seleccionar_archivo = ttk.Button(self, text="Seleccionar Archivo CSV", command=self.cargar_archivo)
        self.btn_seleccionar_archivo.pack(pady=20)

        # Área de texto para mostrar el estado de la carga
        self.text_area = tk.Text(self, wrap=tk.WORD, height=10, width=60)
        self.text_area.pack(pady=10)

    def cargar_archivo(self):
        """Abre un diálogo para seleccionar un archivo CSV y procesa el contenido."""
        archivo = askopenfilename(
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los Archivos", "*.*")]
        )
        if not archivo:
            return

        try:
            with open(archivo, newline='', encoding="ISO-8859-1", errors="replace") as csvfile:
                reader = csv.reader(csvfile)
                encabezados = next(reader, None)  # Saltar encabezado, si existe

                for row in reader:
                    # Validar que la fila tenga exactamente 10 columnas
                    if len(row) < 10:
                        self.text_area.insert(tk.END, f"Fila inválida: {row}\n")
                        continue

                    try:
                        # Desempaquetar valores de la fila
                        nombre, correo, celular, edad, genero, direccion, ciudad, cargo, empresa, rango_salarial = row

                        # Validación adicional (ejemplo: omitir filas con campos obligatorios vacíos)
                        if not nombre or not correo:
                            self.text_area.insert(tk.END, f"Fila inválida (campos obligatorios vacíos): {row}\n")
                            continue

                        # Insertar en la base de datos
                        db.agregar_participante(
                            nombre.strip(), correo.strip(), celular.strip(), edad.strip(),
                            genero.strip(), direccion.strip(), ciudad.strip(),
                            cargo.strip(), empresa.strip(), rango_salarial.strip()
                    )
                        self.text_area.insert(tk.END, f"Participante agregado: {nombre} ({correo})\n")
                    except ValueError:
                        self.text_area.insert(tk.END, f"Error al procesar la fila: {row}\n")

        except Exception as e:
            self.text_area.insert(tk.END, f"Error al leer el archivo: {str(e)}\n")

class SegmentacionScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Segmentación de Participantes")
        self.geometry("600x400")
        self.init_ui()

    def init_ui(self):
        """Interfaz para seleccionar criterios de segmentación."""
        ttk.Label(self, text="Segmentación de Participantes", font=("Helvetica", 16)).pack(pady=10)

        # Campos para criterios de segmentación
        ttk.Label(self, text="Edad mínima:").pack(pady=5)
        self.edad_min_entry = ttk.Entry(self)
        self.edad_min_entry.pack(pady=5)

        ttk.Label(self, text="Edad máxima:").pack(pady=5)
        self.edad_max_entry = ttk.Entry(self)
        self.edad_max_entry.pack(pady=5)

        ttk.Label(self, text="Género:").pack(pady=5)
        self.genero_combobox = ttk.Combobox(self, values=["", "Masculino", "Femenino", "Otro"])
        self.genero_combobox.pack(pady=5)

        ttk.Label(self, text="Ciudad:").pack(pady=5)
        self.ciudad_entry = ttk.Entry(self)
        self.ciudad_entry.pack(pady=5)

        # Botón para aplicar filtros
        self.btn_filtrar = ttk.Button(self, text="Aplicar Filtros", command=self.filtrar_participantes)
        self.btn_filtrar.pack(pady=10)

        # Listbox para mostrar resultados
        self.resultados_listbox = tk.Listbox(self, height=10, width=80)
        self.resultados_listbox.pack(pady=10)

    def filtrar_participantes(self):
        """Filtra participantes según los criterios especificados."""
        edad_min = self.edad_min_entry.get()
        edad_max = self.edad_max_entry.get()
        genero = self.genero_combobox.get()
        ciudad = self.ciudad_entry.get()

        # Construcción dinámica de la consulta
        query = "SELECT nombre, correo, edad, genero, ciudad FROM participantes WHERE 1=1"
        params = []

        if edad_min:
            query += " AND edad >= ?"
            params.append(edad_min)
        if edad_max:
            query += " AND edad <= ?"
            params.append(edad_max)
        if genero:
            query += " AND genero = ?"
            params.append(genero)
        if ciudad:
            query += " AND ciudad LIKE ?"
            params.append(f"%{ciudad}%")

        # Ejecutar la consulta
        self.resultados_listbox.delete(0, tk.END)
        try:
            resultados = db.cursor.execute(query, params).fetchall()
            if resultados:
                for row in resultados:
                    self.resultados_listbox.insert(tk.END, f"Nombre: {row[0]}, Correo: {row[1]}, Edad: {row[2]}, Género: {row[3]}, Ciudad: {row[4]}")
            else:
                self.resultados_listbox.insert(tk.END, "No se encontraron participantes que coincidan con los criterios.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar la consulta: {str(e)}")


class CargarParticipantesDesdeCRM(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cargar Participantes desde el CRM")
        self.geometry("500x400")
        self.init_ui()

    def init_ui(self):
        """Interfaz para cargar un archivo CSV desde el CRM."""
        ttk.Label(self, text="Cargar Participantes desde un archivo CSV del CRM", font=("Helvetica", 16)).pack(pady=10)

        # Botón para seleccionar archivo CSV
        self.btn_seleccionar_archivo = ttk.Button(self, text="Seleccionar Archivo CSV", command=self.cargar_archivo_crm)
        self.btn_seleccionar_archivo.pack(pady=20)

        # Área de texto para mostrar el estado de la carga
        self.text_area = tk.Text(self, wrap=tk.WORD, height=15, width=60)
        self.text_area.pack(pady=10)
        
    def detectar_codificacion(archivo):
        """Detecta la codificación de un archivo."""
        with open(archivo, "rb") as f:
            resultado = chardet.detect(f.read())
        return resultado['encoding']


    def cargar_archivo_crm(self):
        """Abre un diálogo para seleccionar un archivo CSV y procesa el contenido."""
        archivo = askopenfilename(
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los Archivos", "*.*")]
        )
        if not archivo:
            return

        try:
            # Detectar codificación
            codificacion = detectar_codificacion(archivo)
            print(f"Codificación detectada: {codificacion}")

            with open(archivo, newline='', encoding=codificacion) as csvfile:
                reader = csv.reader(csvfile)
                encabezados = next(reader)
            print(f"Encabezados: {encabezados}")

            for row in reader:
                print(f"Procesando fila: {row}")

            with open(archivo, newline='', encoding=codificacion) as csvfile:
                reader = csv.DictReader(csvfile)

                # Verificar encabezados esperados
                campos_requeridos = ["nombre", "correo", "celular", "edad", "genero", "direccion", "ciudad", "cargo", "empresa", "rango_salarial"]
                if not all(campo in reader.fieldnames for campo in campos_requeridos):
                    self.text_area.insert(tk.END, "Error: El archivo no contiene los campos requeridos.\n")
                    return

                for row in reader:
                    # Validar si todos los campos están presentes
                    if not all(row[campo] for campo in campos_requeridos):
                        self.text_area.insert(tk.END, f"Fila inválida: {row}\n")
                        continue

                    # Insertar participante en la base de datos
                    db.agregar_participante(
                        row["nombre"].strip(),
                        row["correo"].strip(),
                        row["celular"].strip(),
                        int(row["edad"].strip()),
                        row["genero"].strip(),
                        row["direccion"].strip(),
                        row["ciudad"].strip(),
                        row["cargo"].strip(),
                        row["empresa"].strip(),
                        row["rango_salarial"].strip(),
                    )
                    self.text_area.insert(tk.END, f"Participante agregado: {row['nombre']} ({row['correo']})\n")

        except Exception as e:
            self.text_area.insert(tk.END, f"Error al leer el archivo: {str(e)}\n")


if __name__ == "__main__":
    # Inicializar la base de datos y agregar roles/preguntas de prueba
    db.agregar_rol("Administrador", "Acceso completo al sistema")
    db.agregar_rol("Analista", "Acceso limitado a reportes")
    db.agregar_pregunta("¿Qué tan satisfecho está?", "Escala", "1,2,3,4,5")
    db.agregar_pregunta("¿Recomendaría nuestro producto?", "Sí/No")
    db.agregar_pregunta("Escriba su comentario", "Texto")
    db = Database()
    db.agregar_columna_version()  # Verifica o agrega la columna 'version'
    db.agregar_columna_estado()
    db.agregar_columna_token()
    
class EncuestaScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Encuestas")
        self.geometry("500x500")
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Interfaz para gestionar encuestas."""
        ttk.Label(self, text="Gestión de Encuestas", font=("Helvetica", 16)).pack(pady=10)

        # Listbox para mostrar encuestas
        self.listbox_encuestas = tk.Listbox(self, height=15, width=50)
        self.listbox_encuestas.pack(pady=10)
        self.cargar_encuestas()

        # Botón para generar informe
        self.btn_generar_informe = ttk.Button(self, text="Generar Informe", command=self.generar_informe_encuesta)
        self.btn_generar_informe.pack(pady=10)

    def cargar_encuestas(self):
        """Carga las encuestas disponibles en el Listbox."""
        encuestas = db.obtener_titulos_encuestas()
        for encuesta in encuestas:
            self.listbox_encuestas.insert(tk.END, encuesta[0])

    def generar_informe_encuesta(self):
        """Genera un informe de la encuesta seleccionada."""
        seleccion = self.listbox_encuestas.curselection()
        if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione una encuesta.")
                return  # Asegúrate de salir de la función si no hay selección

    # Obtener el título de la encuesta seleccionada
        encuesta_titulo = self.listbox_encuestas.get(seleccion)
    
    # Obtener el ID de la encuesta
        encuesta_id = db.obtener_id_encuesta(encuesta_titulo)  # Necesitas implementar esta función en la base de datos

    # Obtener los resultados de la encuesta
        resultados = db.obtener_resultados_encuesta(encuesta_id)  # Necesitas implementar esta función en la base de datos

    # Generar informe en PDF
        archivo_salida = f"{encuesta_titulo}_informe.pdf"
        generar_informe(encuesta_titulo, resultados, archivo_salida)  # Asegúrate de tener la función generar_informe implementada
        messagebox.showinfo("Éxito", f"Informe generado: {archivo_salida}")

    
    class LlenarEncuestaScreen(tk.Toplevel):
        def __init__(self, parent, encuesta_id):
            super().__init__(parent)
            self.title("Llenar Encuesta")
            self.geometry("600x500")
            self.parent = parent
            self.encuesta_id = encuesta_id
            self.preguntas = []
            self.respuestas = {}
            self.init_ui()

        def init_ui(self):
            """Interfaz para responder preguntas."""
            encuesta = db.obtener_encuesta(self.encuesta_id)
            ttk.Label(self, text=f"Encuesta: {encuesta['titulo']}", font=("Helvetica", 16)).pack(pady=10)

            # Cargar preguntas
            self.preguntas = db.obtener_preguntas_de_encuesta(self.encuesta_id)

            for pregunta in self.preguntas:
                ttk.Label(self, text=pregunta['texto'], font=("Helvetica", 12)).pack(anchor="w", pady=5)
                respuesta_entry = ttk.Entry(self, width=50)
                respuesta_entry.pack(pady=5)
                self.respuestas[pregunta['id']] = respuesta_entry

            # Botón para enviar respuestas
            self.btn_enviar = ttk.Button(self, text="Enviar Respuestas", command=self.enviar_respuestas)
            self.btn_enviar.pack(pady=20)

        def enviar_respuestas(self):
            """Enviar respuestas del participante."""
            participante_id = self.parent.usuario_activo.id
            for pregunta_id, respuesta_entry in self.respuestas.items():
                respuesta = respuesta_entry.get()
            db.guardar_respuesta(participante_id, self.encuesta_id, pregunta_id, respuesta)

            messagebox.showinfo("Gracias", "Tus respuestas han sido enviadas.")
            self.destroy()

class EncuestaScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Encuestas")
        self.geometry("500x500")
        self.parent = parent
        self.preguntas_seleccionadas = []
        self.init_ui()

    def init_ui(self):
        """Interfaz para crear encuestas."""
        ttk.Label(self, text="Título de la Encuesta:").pack(pady=5)
        self.titulo_entry = ttk.Entry(self)
        self.titulo_entry.pack(pady=5)

        ttk.Label(self, text="Banco de Preguntas:").pack(pady=5)

        # Banco de preguntas (Listbox)
        self.banco_preguntas = tk.Listbox(self, selectmode="multiple", height=10)
        self.banco_preguntas.pack(pady=5, fill="x")
        self.cargar_preguntas()

        # Botón para seleccionar preguntas
        self.btn_agregar_pregunta = ttk.Button(self, text="Agregar Preguntas Seleccionadas",
                                               command=self.seleccionar_preguntas)
        self.btn_agregar_pregunta.pack(pady=5)

        # Selector de estado
        ttk.Label(self, text="Estado de la Encuesta:").pack(pady=5)
        self.estado_combobox = ttk.Combobox(self, values=["borrador", "publicada"])
        self.estado_combobox.set("borrador")  # Estado por defecto
        self.estado_combobox.pack(pady=5)

        # Selector de fecha de cierre
        ttk.Label(self, text="Fecha de Cierre:").pack(pady=5)
        self.fecha_cierre_calendar = Calendar(self, date_pattern="y-mm-dd")
        self.fecha_cierre_calendar.pack(pady=5)

        # Botón para guardar encuesta
        self.btn_guardar_encuesta = ttk.Button(self, text="Guardar Encuesta", command=self.guardar_encuesta)
        self.btn_guardar_encuesta.pack(pady=10)

    def cargar_preguntas(self):
        """Carga las preguntas predefinidas en el Listbox."""
        preguntas = db.obtener_preguntas()
        for pregunta in preguntas:
            self.banco_preguntas.insert(tk.END, f"{pregunta[1]} ({pregunta[2]})")

    def seleccionar_preguntas(self):
        """Selecciona preguntas del banco."""
        seleccion = self.banco_preguntas.curselection()
        preguntas = db.obtener_preguntas()
        self.preguntas_seleccionadas = [preguntas[i] for i in seleccion]
        messagebox.showinfo("Éxito", "Preguntas seleccionadas correctamente.")

    def guardar_encuesta(self):
        """Guarda la encuesta como borrador o publicada."""
        titulo = self.titulo_entry.get()
        estado = self.estado_combobox.get()
        fecha_cierre = self.fecha_cierre_calendar.get_date()

        if not titulo:
            messagebox.showwarning("Advertencia", "El título es obligatorio.")
            return

        if not self.preguntas_seleccionadas:
            messagebox.showwarning("Advertencia", "Seleccione al menos una pregunta.")
            return

        # Crear una nueva encuesta con el estado seleccionado y la fecha de cierre
        preguntas_ids = [pregunta[0] for pregunta in self.preguntas_seleccionadas]
        db.agregar_encuesta(titulo, preguntas_ids, estado, fecha_cierre)
        messagebox.showinfo("Éxito", f"Encuesta '{titulo}' guardada como '{estado}' con cierre en {fecha_cierre}.")
        self.destroy()
        
if __name__ == "__main__":
    # Inicializar la base de datos y agregar roles/preguntas de prueba
    db.agregar_rol("Administrador", "Acceso completo al sistema")
    db.agregar_rol("Analista", "Acceso limitado a reportes")
    db.agregar_pregunta("¿Qué tan satisfecho está?", "Escala", "1,2,3,4,5")
    db.agregar_pregunta("¿Recomendaría nuestro producto?", "Sí/No")
    db.agregar_pregunta("Escriba su comentario", "Texto")
    db = Database()
    db.agregar_columna_version()  # Verifica o agrega la columna 'version'
    db.agregar_columna_estado()
    db.agregar_columna_preguntas()

    

    app = App()
    app.mainloop()

    

  