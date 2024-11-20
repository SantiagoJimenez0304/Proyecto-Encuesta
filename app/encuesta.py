class Encuesta:
    def __init__(self, id, titulo, preguntas, version=1, creado_en=None):
        self.id = id
        self.titulo = titulo
        self.preguntas = preguntas  # Lista de IDs de preguntas asociadas
        self.version = version
        self.creado_en = creado_en

    def agregar_pregunta(self, pregunta):
        """Agrega una pregunta a la encuesta."""
        self.preguntas.append(pregunta)

    def listar_preguntas(self):
        """Devuelve las preguntas de la encuesta."""
        return [str(pregunta) for pregunta in self.preguntas]
