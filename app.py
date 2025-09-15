import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# --- Carga de variables de entorno / cliente ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="SafeCore-Copiloto GenAI", page_icon="🤖", layout="centered")
st.title("🤖 Desarrollo solución de IA Generativa con Python")
st.caption("Ejemplo práctico: Chat · Resumen · Reescritura")

if not OPENAI_API_KEY:
    st.error("No se encontró OPENAI_API_KEY en el entorno. Configúrala en GitHub (Settings → Secrets/Variables).")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# --- Funciones de servicio ---

def call_chat(messages, model="gpt-4o-mini", temperature=0.3):
    """Llamada genérica al modelo de chat."""
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"Error al llamar al modelo: {e}")
        return None

def chat_con_modelo(pregunta, temperature=0.3):
    """Chat simple con historial mínimo."""
    messages = [
        {"role": "system", "content": "Eres un asistente útil y directo."},
        {"role": "user", "content": pregunta}
    ]
    return call_chat(messages, temperature=temperature)

def resumir_texto(texto, estilo="bullet", temperature=0.3):
    """Resumen en viñetas o en párrafo corto."""
    estilo_str = "viñetas" if estilo == "bullet" else "párrafo"
    prompt = f"Resume el siguiente texto en formato {estilo_str}:\n\n{texto}"
    messages = [
        {"role": "system", "content": "Eres un experto en resúmenes concisos."},
        {"role": "user", "content": prompt}
    ]
    return call_chat(messages, temperature=temperature)

def reescribir_tono(texto, tono="profesional", temperature=0.4):
    """Reescribe un texto en un tono específico."""
    prompt = f"Reescribe este texto en tono {tono}, manteniendo el significado:\n\n{texto}"
    messages = [
        {"role": "system", "content": "Eres un editor experto en adaptar estilos."},
        {"role": "user", "content": prompt}
    ]
    return call_ch_

