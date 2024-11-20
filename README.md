
# Sistema de Gestión de Encuestas

Este proyecto es un **Sistema de Gestión de Encuestas** diseñado para gestionar encuestas, participantes y resultados. Incluye funcionalidades para crear y editar encuestas, administrar participantes, enviar invitaciones, generar informes y realizar análisis básicos.

# Realizado por: Santiago Jimenez y Enzo Gonzalez
## Características

- **Gestión de Usuarios**: Registro e inicio de sesión con roles específicos como Administrador o Analista.
- **Gestión de Encuestas**:
  - Crear, editar y eliminar encuestas.
  - Configurar preguntas con diferentes tipos de respuestas.
  - Establecer fecha de cierre de encuestas.
- **Gestión de Participantes**:
  - Cargar participantes desde un archivo CSV.
  - Segmentar participantes por criterios como edad, género y ubicación.
- **Invitaciones**:
  - Generar enlaces únicos para cada participante.
  - Enviar correos electrónicos simulados con invitaciones.
- **Resultados e Informes**:
  - Visualizar tasas de respuesta y distribución de respuestas.
  - Generar informes automáticos en PDF.
  - Exportar datos crudos en formato CSV.

## Requisitos

- Python 3.8 o superior.
- Dependencias adicionales enumeradas en `requirements.txt`.

## Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/SantiagoJimenez0304/Proyecto-Encuesta.git
   
   pip install -r requirements.txt
   ```
2. **Ejecución del programa**
```bash
python main.py

