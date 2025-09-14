from streamlit_mic_recorder import speech_to_text
from config import llm
import streamlit as st


st.set_page_config(page_title="Asistente de Voz", layout="centered")

st.title("🗣️ Tu asistente de Voz Todo en Uno")
st.write("Aplicación de chat habilitada por voz (GPT-4o + Micrófono)")

# Capturar voz y convertirla a texto
text = speech_to_text(
    language="es",
    use_container_width=True,
    just_once=True,
    key="STT"
)

# Procesar el texto si existe
if text:
    st.write("🧑 Tú: ", text)
    response = llm.invoke(text)
    st.write("🤖 Respuesta del modelo: ", response.content)
