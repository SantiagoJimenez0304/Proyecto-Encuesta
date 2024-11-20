from fpdf import FPDF

def generar_informe(encuesta_titulo, resultados, archivo_salida="informe.pdf"):
    """
    Genera un informe en PDF con los resultados de la encuesta.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del informe
    pdf.set_font("Arial", size=16, style="B")
    pdf.cell(200, 10, txt=f"Informe de la Encuesta: {encuesta_titulo}", ln=True, align="C")
    pdf.ln(10)

    # Agregar resultados
    pdf.set_font("Arial", size=12)
    for pregunta, respuestas in resultados.items():
        pdf.cell(200, 10, txt=f"Pregunta: {pregunta}", ln=True)
        for respuesta in respuestas:
            pdf.cell(200, 10, txt=f" - {respuesta}", ln=True)
        pdf.ln(5)

    # Guardar el archivo
    pdf.output(archivo_salida)
    print(f"Informe generado: {archivo_salida}")
