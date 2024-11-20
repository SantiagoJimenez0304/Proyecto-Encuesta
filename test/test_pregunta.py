import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.pregunta import Pregunta

def test_pregunta_inicializacion():
    """
    Prueba la inicialización de una pregunta.
    """
    pregunta = Pregunta(1, "¿Cuál es tu color favorito?", "opción múltiple", "Rojo,Azul,Verde")

    assert pregunta.id == 1
    assert pregunta.texto == "¿Cuál es tu color favorito?"
    assert pregunta.tipo_respuesta == "opción múltiple"
    assert pregunta.opciones == ["Rojo", "Azul", "Verde"]

def test_pregunta_inicializacion_sin_opciones():
    """
    Prueba la inicialización de una pregunta sin opciones.
    """
    pregunta = Pregunta(2, "Escribe tu nombre", "texto")

    assert pregunta.id == 2
    assert pregunta.texto == "Escribe tu nombre"
    assert pregunta.tipo_respuesta == "texto"
    assert pregunta.opciones == []

def test_actualizar_pregunta_texto():
    """
    Prueba la actualización del texto de la pregunta.
    """
    pregunta = Pregunta(3, "Texto original", "texto")
    pregunta.actualizar(texto="Texto actualizado")

    assert pregunta.texto == "Texto actualizado"
    assert pregunta.tipo_respuesta == "texto"  # Sin cambios
    assert pregunta.opciones == []  # Sin cambios

def test_actualizar_pregunta_tipo_respuesta():
    """
    Prueba la actualización del tipo de respuesta de la pregunta.
    """
    pregunta = Pregunta(4, "¿Cuál es tu edad?", "texto")
    pregunta.actualizar(tipo_respuesta="numérico")

    assert pregunta.texto == "¿Cuál es tu edad?"
    assert pregunta.tipo_respuesta == "numérico"
    assert pregunta.opciones == []  # Sin cambios

def test_actualizar_pregunta_opciones():
    """
    Prueba la actualización de las opciones de la pregunta.
    """
    pregunta = Pregunta(5, "¿Cuál es tu color favorito?", "opción múltiple", "Rojo,Azul,Verde")
    pregunta.actualizar(opciones="Amarillo,Naranja")

    assert pregunta.opciones == ["Amarillo", "Naranja"]

def test_actualizar_pregunta_todo():
    """
    Prueba la actualización de todos los atributos de la pregunta.
    """
    pregunta = Pregunta(6, "Texto original", "texto")
    pregunta.actualizar(texto="Texto nuevo", tipo_respuesta="opción múltiple", opciones="Opción 1,Opción 2")

    assert pregunta.texto == "Texto nuevo"
    assert pregunta.tipo_respuesta == "opción múltiple"
    assert pregunta.opciones == ["Opción 1", "Opción 2"]

def test_str():
    """
    Prueba el método __str__ de la clase Pregunta.
    """
    pregunta = Pregunta(7, "¿Te gusta programar?", "sí/no")
    assert str(pregunta) == "¿Te gusta programar? (sí/no)"
