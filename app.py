import streamlit as st
import os
from dotenv import load_dotenv
from analyst import get_analyst_clarification, get_analyst_retroactive, get_analyst_interpretation

load_dotenv()

# State initialization
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "packs" not in st.session_state:
    st.session_state.packs = []

if "current_step" not in st.session_state:
    st.session_state.current_step = "P1" 

if "last_p1" not in st.session_state:
    st.session_state.last_p1 = None

if "last_response_p1" not in st.session_state:
    st.session_state.last_response_p1 = None

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")

def show_disclaimer():
    st.title("Lacanapp")
    st.warning("""
    "La presente conversación no reemplaza ni complementa ninguna terapia de ningún tipo. Se trata de un test de ensayo conversacional que no debe ser tomado como sustituto de un profesional."
    """)
    if st.button("Acepto y deseo continuar"):
        st.session_state.disclaimer_accepted = True
        st.rerun()

def process_input(prompt):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    current_step = st.session_state.current_step
    api_key = st.session_state.api_key
    
    if not api_key:
        st.error("Por favor, configure su API Key de Google Gemini en la barra lateral.")
        return

    with st.spinner("El analista está puntuando su discurso..."):
        if current_step == "P1":
            response = get_analyst_clarification(prompt, api_key=api_key)
            st.session_state.current_step = "P2"
            st.session_state.last_p1 = prompt
            st.session_state.last_response_p1 = response
        elif current_step == "P2":
            p1 = st.session_state.last_p1
            response_p1 = st.session_state.last_response_p1
            p2 = prompt
            response = get_analyst_retroactive(p1, response_p1, p2, api_key=api_key)
            
            st.session_state.packs.append({
                "p1": p1, 
                "response_p1": response_p1,
                "p2": p2, 
                "response": response
            })
            
            if len(st.session_state.packs) == 3:
                interpretation = get_analyst_interpretation(st.session_state.packs, api_key=api_key)
                response += "\n\n---\n\n**Interpretación Final:**\n\n" + interpretation
                st.session_state.current_step = "FINISHED"
            else:
                st.session_state.current_step = "P1"
                
        st.session_state.chat_history.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(page_title="Lacanapp", page_icon="🧠")

    if not st.session_state.disclaimer_accepted:
        show_disclaimer()
        return

    st.title("Lacanapp: Diálogo Psicoanalítico")
    
    with st.sidebar:
        st.title("Configuración")
        st.session_state.api_key = st.text_input("Gemini API Key", value=st.session_state.api_key, type="password")
        st.info(f"Packs completados: {len(st.session_state.packs)}/3")
        if st.session_state.current_step != "FINISHED":
            st.write(f"Esperando: {'Respuesta inicial' if st.session_state.current_step == 'P1' else 'Aclaración'}")
        
        if st.button("Reiniciar sesión"):
            for key in ["chat_history", "packs", "current_step", "last_p1"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input
    if st.session_state.current_step != "FINISHED":
        if prompt := st.chat_input("Diga lo que piensa..."):
            process_input(prompt)
            st.rerun()
    else:
        st.success("El ciclo de diálogo ha concluido.")

if __name__ == "__main__":
    main()
