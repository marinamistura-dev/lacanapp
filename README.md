# Lacanapp: Diálogo Psicoanalítico

Esta es una aplicación de Streamlit diseñada para sostener un diálogo de orientación lacaniana.

## Características
- **Función del Analista:** Implementada siguiendo los principios de no-comprensión, puntuación y deseo del analista.
- **Estructura de Diálogo:** 3 packs dobles (6 prompts) seguidos de una interpretación final.
- **Lógica Retroactiva:** El analista asigna contexto a las intervenciones de forma retroactiva.
- **Disclaimer Obligatorio:** Cumple con la advertencia legal antes de comenzar.

## Instalación
1. Clonar el repositorio.
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
1. Configurar la clave de API de Groq (vía `.env`, la variable de entorno `GROQ_API_KEY` o en la barra lateral de la app).
2. Ejecutar Streamlit:
   ```bash
   streamlit run app.py
   ```

## Requisitos
- Python 3.8+
- Groq API Key
