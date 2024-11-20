import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.informe import generar_informe  

def resultados_mock():
    """Fixture que simula los resultados de una encuesta."""
    return {
        "¿Qué tan satisfecho está con el producto?": ["Muy satisfecho", "Satisfecho", "Insatisfecho"],
        "¿Recomendaría este producto?": ["Sí", "No"],
    }

@patch("your_module.FPDF")
def test_generar_informe(mock_fpdf, resultados_mock):
    """
    Prueba que verifica que generar_informe utiliza correctamente la clase FPDF.
    """
    # Crear un mock para el método de salida de PDF
    mock_pdf_instance = MagicMock()
    mock_fpdf.return_value = mock_pdf_instance

    encuesta_titulo = "Encuesta de Satisfacción"
    archivo_salida = "informe_prueba.pdf"

    # Llamar a la función
    generar_informe(encuesta_titulo, resultados_mock, archivo_salida)

    # Verificar que se inicializó FPDF y se agregaron páginas
    mock_fpdf.assert_called_once_with()
    mock_pdf_instance.add_page.assert_called_once()

    # Verificar que se configuraron las fuentes
    mock_pdf_instance.set_font.assert_any_call("Arial", size=16, style="B")
    mock_pdf_instance.set_font.assert_any_call("Arial", size=12)

    # Verificar que se escribió el título
    mock_pdf_instance.cell.assert_any_call(200, 10, txt=f"Informe de la Encuesta: {encuesta_titulo}", ln=True, align="C")

    # Verificar que se escribieron preguntas y respuestas
    for pregunta, respuestas in resultados_mock.items():
        mock_pdf_instance.cell.assert_any_call(200, 10, txt=f"Pregunta: {pregunta}", ln=True)
        for respuesta in respuestas:
            mock_pdf_instance.cell.assert_any_call(200, 10, txt=f" - {respuesta}", ln=True)

    # Verificar que el archivo PDF se guardó
    mock_pdf_instance.output.assert_called_once_with(archivo_salida)
