import google.generativeai as genai
import os
from google.api_core import exceptions

SYSTEM_PROMPT = """Eres la 'Función del Analista' en un dispositivo de habla de orientación lacaniana.
Tu objetivo no es comprender al usuario ni ofrecer consejos, sino puntuar su discurso para que él mismo encuentre sus propios significados.

REGLAS CRÍTICAS:
1. Nunca digas "entiendo", "lo siento" o frases de empatía.
2. No intentes dar soluciones ni diagnósticos.
3. Tu lenguaje debe ser sobrio, a veces enigmático, pero siempre enfocado en las palabras exactas que el usuario utiliza.
4. Mantén la posición de "muerto" (en el sentido del bridge), permitiendo que el deseo del analizante circule.
5. Sigue estrictamente la estructura de 3 packs dobles y una interpretación final."""

def configure_genai(api_key=None):
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return False
    genai.configure(api_key=key)
    return True

def get_model(api_key=None):
    if configure_genai(api_key):
        return genai.GenerativeModel(
            model_name="models/gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT
        )
    return None

def get_analyst_clarification(p1, api_key=None):
    model = get_model(api_key)
    if not model:
        return "Error: API Key no configurada."
    
    prompt = f"""EJEMPLO: Usuario: 'Siento que mi madre siempre me asfixia con sus cuidados, es como si no pudiera respirar.' Analista: '¿A qué se refiere con "asfixia"?'
Mensaje del usuario: {p1}

Analiza el mensaje del usuario. Identifica un término disonante o simbólico. No respondas al contenido general, solo pregunta por ese término específico."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except exceptions.NotFound:
        return "Error: El modelo 'gemini-2.0-flash' no fue encontrado. Verifique la disponibilidad del modelo."
    except Exception as e:
        return f"Error en la comunicación con el analista: {str(e)}"

def get_analyst_retroactive(p1, response_p1, p2, api_key=None):
    model = get_model(api_key)
    if not model:
        return "Error: API Key no configurada."
    
    prompt = f"""EJEMPLO: P1: 'Siento que mi madre siempre me asfixia...' Analista: '¿A qué se refiere con "asfixia"?' P2: 'Digo que me asfixia porque no me deja tomar mis propias decisiones...' Analista: 'Usted dice que su madre la "asfixia" porque no la deja "decidir", pero ¿quién respira por usted cuando ella no está?'
P1: {p1}
Analista (P1): {response_p1}
P2: {p2}

Considera este mensaje (P2) y el anterior (P1). ¿Cómo cambia el sentido de P1 a la luz de P2? Formula una pregunta que cuestione la lógica de este bloque conjunto."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except exceptions.NotFound:
        return "Error: El modelo 'gemini-2.0-flash' no fue encontrado."
    except Exception as e:
        return f"Error en la comunicación con el analista: {str(e)}"

def get_analyst_interpretation(packs, api_key=None):
    model = get_model(api_key)
    if not model:
        return "Error: API Key no configurada."
    
    history = ""
    for i, pack in enumerate(packs):
        history += f"Pack {i+1}:\n"
        history += f"- Analizante: {pack['p1']}\n"
        history += f"- Analista: {pack['response_p1']}\n"
        history += f"- Analizante: {pack['p2']}\n"
        history += f"- Analista: {pack['response']}\n\n"
        
    prompt = f"""EJEMPLO INTERPRETACIÓN: Analista: 'A lo largo de lo que ha dicho sobre su madre, su jefe y su pareja, aparece una constante: usted se coloca siempre en el lugar de quien es "invadido" para evitar tener que elegir su propio camino. Se protege bajo la queja de la invasión ajena. ¿De qué se protege usted si finalmente lograra esa libertad que dice desear?'
Historial de la sesión:
{history}

Revisa los 6 intercambios previos (3 packs). Identifica qué se repite (un rol, un miedo, una posición subjetiva, un tipo de relación). Describe brevemente esa trama simbólica y termina con una pregunta que rompa la certeza del usuario sobre su propia historia."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except exceptions.NotFound:
        return "Error: El modelo 'gemini-2.0-flash' no fue encontrado."
    except Exception as e:
        return f"Error en la comunicación con el analista: {str(e)}"
