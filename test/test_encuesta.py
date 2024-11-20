import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.encuesta import Encuesta 

def encuesta():
    """Fixture que crea una instancia de Encuesta para las pruebas."""
    return Encuesta(id=1, titulo="Encuesta de Satisfacción", preguntas=[101, 102, 103])

def test_creacion_encuesta(encuesta):
    """Prueba que verifica la creación de una encuesta."""
    assert encuesta.id == 1
    assert encuesta.titulo == "Encuesta de Satisfacción"
    assert encuesta.preguntas == [101, 102, 103]
    assert encuesta.version == 1
    assert encuesta.creado_en is None

def test_agregar_pregunta(encuesta):
    """Prueba que verifica agregar una nueva pregunta a la encuesta."""
    nueva_pregunta = 104
    encuesta.agregar_pregunta(nueva_pregunta)
    assert nueva_pregunta in encuesta.preguntas
    assert len(encuesta.preguntas) == 4

def test_listar_preguntas(encuesta):
    """Prueba que verifica listar preguntas devuelve las preguntas en formato de string."""
    preguntas_listadas = encuesta.listar_preguntas()
    assert preguntas_listadas == ["101", "102", "103"]
    encuesta.agregar_pregunta(104)
    preguntas_listadas = encuesta.listar_preguntas()
    assert preguntas_listadas == ["101", "102", "103", "104"]
