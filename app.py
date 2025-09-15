import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# --- Carga de variables de entorno / cliente ---
    
load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY", None) if hasattr(st, "secrets") else None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="SafeCore-Copiloto GenAI", page_icon="🤖", layout="centered")
st.title("🤖 SafeCore solución de IA Generativa con Python")
st.caption("Habilidades aprendidas: Chat · Resumen · Reescritura")

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
    return call_chat(messages, temperature=temperature)
# --- Sidebar ---
st.sidebar.header("Ajustes")
mode = st.sidebar.selectbox("Elige modo", ["Chat", "Resumen", "Reescritura de tono"], key="mode")
with st.sidebar.expander("Opciones avanzadas", expanded=False):
    temp = st.slider("Creatividad (temperature)", 0.0, 1.0, 0.3, 0.1, key="temperature")
    st.write("Modelo usado: **gpt-4o-mini**")

# --- Modo: Chat ---
if mode == "Chat":
    st.subheader("Chat sencillo con el modelo")

    if "history" not in st.session_state:
        st.session_state.history = [{"role": "system", "content": "Eres un asistente amigable."}]

    for m in st.session_state.history[1:]:
        with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
            st.write(m["content"])

    prompt = st.chat_input("Escribe tu mensaje...")
    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.spinner("Pensando..."):
            answer = call_chat(st.session_state.history, temperature=temp)
        if answer:
            st.session_state.history.append({"role": "assistant", "content": answer})
            st.rerun()

# --- Modo: Resumen ---
elif mode == "Resumen":
    st.subheader("Resumen de texto")
    text = st.text_area("Pega aquí el texto a resumir", height=200)
    style = st.radio("Formato", ["bullet", "parrafo"], horizontal=True, index=0)
    estilo = "bullet" if style == "bullet" else "parrafo"

    if st.button("Resumir"):
        if not text.strip():
            st.warning("Por favor, pega un texto.")
        else:
            with st.spinner("Generando resumen..."):
                out = resumir_texto(text, estilo=("bullet" if estilo == "bullet" else "parrafo"), temperature=temp)
            if out:
                st.success("Resumen listo")
                st.write(out)

# --- Modo: Reescritura ---
elif mode == "Reescritura de tono":
    st.subheader("Reescritura de texto con cambio de tono")
    text = st.text_area("Pega el texto a reescribir", height=200)
    tone = st.selectbox("Selecciona el tono", ["profesional", "cercano", "ejecutivo", "didáctico", "enérgico"])

    if st.button("Reescribir"):
        if not text.strip():
            st.warning("Por favor, pega un texto.")
        else:
            with st.spinner("Reescribiendo..."):
                out = reescribir_tono(text, tono=tone, temperature=temp)
            if out:
                st.success("Texto reescrito")
                st.write(out)

st.markdown("---")
st.caption("Construido con Python + Streamlit por Jeffry Antonio IA Generativa")
