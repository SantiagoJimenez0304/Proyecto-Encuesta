class Pregunta:
    def __init__(self, id, texto, tipo_respuesta, opciones=None):
        """
        Inicializa una pregunta.
        :param id: ID único de la pregunta.
        :param texto: Texto de la pregunta.
        :param tipo_respuesta: Tipo de respuesta esperada (texto, opción múltiple, etc.).
        :param opciones: Opciones disponibles para preguntas de opción múltiple.
        """
        self.id = id
        self.texto = texto
        self.tipo_respuesta = tipo_respuesta
        self.opciones = opciones.split(",") if opciones else []

    def actualizar(self, texto=None, tipo_respuesta=None, opciones=None):
        """Actualiza los atributos de la pregunta."""
        if texto:
            self.texto = texto
        if tipo_respuesta:
            self.tipo_respuesta = tipo_respuesta
        if opciones is not None:
            self.opciones = opciones.split(",") if opciones else []

    def __str__(self):
        return f"{self.texto} ({self.tipo_respuesta})"