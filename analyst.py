from openai import OpenAI
import os

SYSTEM_PROMPT = """Eres la 'Función del Analista' en un dispositivo de habla de orientación lacaniana. 
Tu objetivo no es comprender al usuario ni ofrecer consejos, sino puntuar su discurso para que él mismo encuentre sus propios significados.

REGLAS CRÍTICAS:
1. Nunca digas "entiendo", "lo siento" o frases de empatía.
2. No intentes dar soluciones ni diagnósticos.
3. Tu lenguaje debe ser sobrio, a veces enigmático, pero siempre enfocado en las palabras exactas que el usuario utiliza.
4. Mantén la posición de "muerto" (en el sentido del bridge), permitiendo que el deseo del analizante circule.
5. Sigue estrictamente la estructura de 3 packs dobles y una interpretación final."""

def get_client(api_key=None):
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key)

def get_analyst_clarification(p1, api_key=None):
    client = get_client(api_key)
    if not client:
        return "Error: API Key no configurada."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": "EJEMPLO: Usuario: 'Siento que mi madre siempre me asfixia con sus cuidados, es como si no pudiera respirar.' Analista: '¿A qué se refiere con \"asfixia\"?'"},
            {"role": "user", "content": p1},
            {"role": "system", "content": "Analiza el mensaje del usuario. Identifica un término disonante o simbólico. No respondas al contenido general, solo pregunta por ese término específico."}
        ]
    )
    return response.choices[0].message.content

def get_analyst_retroactive(p1, response_p1, p2, api_key=None):
    client = get_client(api_key)
    if not client:
        return "Error: API Key no configurada."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": "EJEMPLO: P1: 'Siento que mi madre siempre me asfixia...' Analista: '¿A qué se refiere con \"asfixia\"?' P2: 'Digo que me asfixia porque no me deja tomar mis propias decisiones...' Analista: 'Usted dice que su madre la \"asfixia\" porque no la deja \"decidir\", pero ¿quién respira por usted cuando ella no está?'"},
            {"role": "user", "content": p1},
            {"role": "assistant", "content": response_p1},
            {"role": "user", "content": p2},
            {"role": "system", "content": "Considera este mensaje (P2) y el anterior (P1). ¿Cómo cambia el sentido de P1 a la luz de P2? Formula una pregunta que cuestione la lógica de este bloque conjunto."}
        ]
    )
    return response.choices[0].message.content

def get_analyst_interpretation(packs, api_key=None):
    client = get_client(api_key)
    if not client:
        return "Error: API Key no configurada."
    
    history = ""
    for i, pack in enumerate(packs):
        history += f"Pack {i+1}:\n"
        history += f"- Analizante: {pack['p1']}\n"
        history += f"- Analista: {pack['response_p1']}\n"
        history += f"- Analizante: {pack['p2']}\n"
        history += f"- Analista: {pack['response']}\n\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": "EJEMPLO INTERPRETACIÓN: Analista: 'A lo largo de lo que ha dicho sobre su madre, su jefe y su pareja, aparece una constante: usted se coloca siempre en el lugar de quien es \"invadido\" para evitar tener que elegir su propio camino. Se protege bajo la queja de la invasión ajena. ¿De qué se protege usted si finalmente lograra esa libertad que dice desear?'"},
            {"role": "user", "content": history},
            {"role": "system", "content": "Revisa los 6 intercambios previos (3 packs). Identifica qué se repite (un rol, un miedo, una posición subjetiva, un tipo de relación). Describe brevemente esa trama simbólica y termina con una pregunta que rompa la certeza del usuario sobre su propia historia."}
        ]
    )
    return response.choices[0].message.content
