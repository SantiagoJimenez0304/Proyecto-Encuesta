import sqlite3
import csv
from tkinter.filedialog import askopenfilename

class Database:
    def __init__(self, db_name="sistema_encuestas.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.crear_tablas()
        self.agregar_columna_token()
        self.agregar_columna_fecha_cierre()


    def agregar_columna_fecha_cierre(self):
        """Añade la columna 'fecha_cierre' a la tabla encuestas si no existe."""
        try:
            self.cursor.execute("ALTER TABLE encuestas ADD COLUMN fecha_cierre DATE")
            self.connection.commit()
        except sqlite3.OperationalError as e:
            # Ignora el error si la columna ya existe
            if "duplicate column name" in str(e).lower():
                pass
        else:
            raise
        columnas = db.obtener_columnas("encuestas")
        print(columnas)


    def listar_encuestas_cerradas(self):
        """Muestra una lista de encuestas cerradas."""
        self.cursor.execute("""
        SELECT titulo, fecha_cierre
        FROM encuestas
        WHERE fecha_cierre IS NOT NULL
          AND julianday('now') > julianday(fecha_cierre)
    """)
        return self.cursor.fetchall()

    def agregar_columna_estado(self):
        """Añade la columna 'estado' a la tabla encuestas si no existe."""
        try:
            self.cursor.execute("ALTER TABLE encuestas ADD COLUMN estado TEXT DEFAULT 'borrador'")
            self.connection.commit()
        except sqlite3.OperationalError as e:
            # Ignora el error si la columna ya existe
            if "duplicate column name" in str(e).lower():
                pass
            else:
                raise
    
    def agregar_columnas_segmentacion(self):
        """Añade columnas necesarias para segmentación si no existen."""
        try:
            self.cursor.execute("ALTER TABLE participantes ADD COLUMN edad INTEGER")
            self.cursor.execute("ALTER TABLE participantes ADD COLUMN genero TEXT")
            self.cursor.execute("ALTER TABLE participantes ADD COLUMN ciudad TEXT")
            self.connection.commit()
        except sqlite3.OperationalError:
            # Ignorar errores si las columnas ya existen
            pass


    def crear_tablas(self):
        """Crea las tablas necesarias para la aplicación."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol_id INTEGER NOT NULL,
                FOREIGN KEY (rol_id) REFERENCES roles (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                tipo_respuesta TEXT NOT NULL,
                opciones TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS encuestas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                preguntas TEXT NOT NULL,  -- IDs de preguntas asociadas, separados por comas
                version INTEGER DEFAULT 1,
                estado TEXT DEFAULT 'borrador',
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS encuesta_preguntas (
                encuesta_id INTEGER NOT NULL,
                pregunta_id INTEGER NOT NULL,
                FOREIGN KEY (encuesta_id) REFERENCES encuestas (id),
                FOREIGN KEY (pregunta_id) REFERENCES preguntas (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                celular TEXT,
                edad INTEGER,
                genero TEXT,
                direccion TEXT,
                ciudad TEXT,
                cargo TEXT,
                empresa TEXT,
                rango_salarial TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                celular TEXT,
                edad INTEGER,
                genero TEXT,
                direccion TEXT,
                ciudad TEXT,
                cargo TEXT,
                empresa TEXT,
                rango_salarial TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS respuestas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                encuesta_id INTEGER NOT NULL,
                pregunta_id INTEGER NOT NULL,
                respuesta TEXT NOT NULL,
                FOREIGN KEY (encuesta_id) REFERENCES encuestas (id),
                FOREIGN KEY (pregunta_id) REFERENCES preguntas (id)
        )
    """)
        self.connection.commit()


    def agregar_columna_fecha_cierre(self):
        """Añade la columna 'fecha_cierre' a la tabla encuestas si no existe."""
        try:
            self.cursor.execute("ALTER TABLE encuestas ADD COLUMN fecha_cierre TIMESTAMP")
            self.connection.commit()
        except sqlite3.OperationalError:
         # Ignorar el error si la columna ya existe
         pass

    

    def agregar_participante(self, nombre, correo, celular=None, edad=None, genero=None, direccion=None, ciudad=None, cargo=None, empresa=None, rango_salarial=None):
        """Agrega un participante a la base de datos."""
        try:
            self.cursor.execute("""
                INSERT INTO participantes (nombre, correo, celular, edad, genero, direccion, ciudad, cargo, empresa, rango_salarial)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nombre, correo, celular, edad, genero, direccion, ciudad, cargo, empresa, rango_salarial))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error al insertar el participante {correo}: {e}")

    def agregar_columna_version(self):
        """Añade la columna 'version' a la tabla encuestas si no existe."""
        try:
            self.cursor.execute("ALTER TABLE encuestas ADD COLUMN version INTEGER DEFAULT 1")
            self.connection.commit()
        except sqlite3.OperationalError as e:
            # Ignora el error si la columna ya existe
            if "duplicate column name" in str(e).lower():
                pass
            else:
                raise

    def agregar_columna_preguntas(self):
        """Añade la columna 'preguntas' a la tabla encuestas si no existe."""
        try:
            self.cursor.execute("ALTER TABLE encuestas ADD COLUMN preguntas TEXT")
            self.connection.commit()
        except sqlite3.OperationalError as e:
            # Ignora el error si la columna ya existe
            if "duplicate column name" in str(e).lower():
                pass
            else:
                raise

    def agregar_rol(self, nombre, descripcion):
        """Agrega un rol a la base de datos."""
        self.cursor.execute("SELECT COUNT(*) FROM roles WHERE nombre = ?", (nombre,))
        if self.cursor.fetchone()[0] > 0:
            return  # El rol ya existe
        self.cursor.execute("INSERT INTO roles (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
        self.connection.commit()

    def obtener_roles(self):
        """Obtiene todos los roles de la base de datos."""
        self.cursor.execute("SELECT id, nombre FROM roles")
        return self.cursor.fetchall()

    def agregar_usuario(self, username, password_hash, rol_id):
        """Agrega un usuario a la base de datos."""
        self.cursor.execute("INSERT INTO usuarios (username, password_hash, rol_id) VALUES (?, ?, ?)",
                            (username, password_hash, rol_id))
        self.connection.commit()

    def obtener_usuario(self, username):
        """Obtiene un usuario por nombre de usuario."""
        self.cursor.execute("""
            SELECT u.id, u.username, u.password_hash, r.nombre
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE u.username = ?
        """, (username,))
        return self.cursor.fetchone()

    def agregar_pregunta(self, texto, tipo_respuesta, opciones=None):
        """Agrega una pregunta al banco."""
        self.cursor.execute(
            "INSERT INTO preguntas (texto, tipo_respuesta, opciones) VALUES (?, ?, ?)",
            (texto, tipo_respuesta, opciones)
        )
        self.connection.commit()

    def obtener_preguntas(self):
        """Obtiene todas las preguntas del banco."""
        self.cursor.execute("SELECT id, texto, tipo_respuesta, opciones FROM preguntas")
        return self.cursor.fetchall()

    def agregar_encuesta(self, titulo, preguntas_ids, estado="borrador", fecha_cierre=None):
        """Crea una nueva encuesta y asocia las preguntas seleccionadas con un estado y fecha de cierre."""
        preguntas_str = ",".join(map(str, preguntas_ids))  # Convertir lista a string
        self.cursor.execute(
        "INSERT INTO encuestas (titulo, preguntas, estado, fecha_cierre) VALUES (?, ?, ?, ?)",
        (titulo, preguntas_str, estado, fecha_cierre)
    )
        self.connection.commit()

    def encuesta_cerrada(self, id_encuesta):
        """Verifica si una encuesta está cerrada basándose en la fecha de cierre."""
        self.cursor.execute("""
        SELECT fecha_cierre
        FROM encuestas
        WHERE id = ?
        """, (id_encuesta,))
        resultado = self.cursor.fetchone()
        if resultado and resultado[0]:
            from datetime import datetime
            fecha_cierre = datetime.strptime(resultado[0], "%Y-%m-%d %H:%M:%S")
            return datetime.now() > fecha_cierre  # True si ya está cerrada
        return False  # Si no tiene fecha de cierre, no está cerrada



    def actualizar_estado_encuesta(self, titulo, nuevo_estado):
        """Actualiza el estado de una encuesta (borrador/publicada)."""
        self.cursor.execute("""
            UPDATE encuestas
            SET estado = ?
            WHERE titulo = ?
        """, (nuevo_estado, titulo))
        self.connection.commit()

    def obtener_titulos_encuestas(self):
        """Obtiene los títulos únicos de las encuestas junto con sus estados."""
        self.cursor.execute("SELECT DISTINCT titulo, estado FROM encuestas")
        return self.cursor.fetchall()

    def obtener_encuestas_por_titulo(self, titulo):
        """Obtiene todas las versiones de una encuesta por título."""
        self.cursor.execute("SELECT * FROM encuestas WHERE titulo = ? ORDER BY version DESC", (titulo,))
        return self.cursor.fetchall()

    def obtener_ultima_version(self, titulo):
        """Obtiene la última versión de una encuesta por título."""
        self.cursor.execute("SELECT MAX(version) FROM encuestas WHERE titulo = ?", (titulo,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado and resultado[0] else 0

    def agregar_version_encuesta(self, titulo, preguntas):
        """Crea una nueva versión de la encuesta."""
        ultima_version = self.obtener_ultima_version(titulo)
        nueva_version = ultima_version + 1
        preguntas_str = ",".join(map(str, preguntas))  # Convertir lista a string
        self.cursor.execute(
            "INSERT INTO encuestas (titulo, preguntas, version) VALUES (?, ?, ?)",
            (titulo, preguntas_str, nueva_version)
        )
        self.connection.commit()

    def obtener_columnas(self, tabla):
        """Obtiene las columnas de una tabla."""
        self.cursor.execute(f"PRAGMA table_info({tabla})")
        return [columna[1] for columna in self.cursor.fetchall()]
    
    def agregar_columna_token(self):
        """Añade la columna 'token' a la tabla participantes si no existe."""
        try:
            self.cursor.execute("ALTER TABLE participantes ADD COLUMN token TEXT")
            self.connection.commit()
        except sqlite3.OperationalError:
            pass  # Ignorar si ya existe


    def actualizar_token_participante(self, id_participante, token):
        """Actualiza el token único del participante en la base de datos."""
        self.cursor.execute(
            "UPDATE participantes SET token = ? WHERE id = ?",
            (token, id_participante)
        )
        self.connection.commit()

    def obtener_participantes(self):
        """Obtiene todos los participantes registrados en la base de datos."""
        self.cursor.execute("SELECT id, nombre, correo FROM participantes")
        return self.cursor.fetchall()

    def registrar_recordatorio(self, id_participante):
        """Registra que se ha enviado un recordatorio a un participante."""
        self.cursor.execute("""
            UPDATE participantes
            SET recordatorios_enviados = recordatorios_enviados + 1
            WHERE id = ?
        """, (id_participante,))
        self.connection.commit()

    def obtener_resultados_encuesta(self, encuesta_id):
        """
        Obtiene los resultados de una encuesta con base en sus respuestas.
        """
        self.cursor.execute("""
            SELECT p.texto, r.respuesta
            FROM respuestas r
            JOIN preguntas p ON r.pregunta_id = p.id
            WHERE r.encuesta_id = ?
        """, (encuesta_id,))
        resultados = self.cursor.fetchall()

        # Procesar resultados   
        resumen = {}
        for pregunta, respuesta in resultados:
            if pregunta not in resumen:
                resumen[pregunta] = []
            resumen[pregunta].append(respuesta)

        return resumen

    def registrar_respuesta(self, encuesta_id, pregunta_id, respuesta):
        """
        Registra una respuesta para una pregunta en una encuesta.
        """
        self.cursor.execute("""
        INSERT INTO respuestas (encuesta_id, pregunta_id, respuesta)
        VALUES (?, ?, ?)
        """, (encuesta_id, pregunta_id, respuesta))
        self.connection.commit()





# Código para obtener las columnas de la tabla encuestas (si necesario)
if __name__ == "__main__":
    db = Database()
    columnas = db.obtener_columnas("encuestas")
    print(columnas)
