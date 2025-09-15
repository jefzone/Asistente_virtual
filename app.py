import os
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(page_title="SafeCore-Copiloto GenAI", page_icon="🤖", layout="centered")
st.title("🤖 Desarrollo solucion de IA Generativa con Python")
st.caption("Ejemplo practico con Chat . Resumen . Reescritura")

# --- Funciones --- 

def call_chat(messages, model="gpt-4o-mini", temperature=0.3):
    """Llamada genérica al modelo de chat."""
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message.content

def chat_con_modelo(pregunta):
    """Chat simple con historial mínimo."""
    messages = [
        {"role": "system", "content": "Eres un asistente útil y directo."},
        {"role": "user", "content": pregunta}
    ]
    return call_chat(messages)

def resumir_texto(texto, estilo="bullet"):
    """Resumen en viñetas o en párrafo corto."""
    prompt = f"Resume el siguiente texto en formato {'viñetas' if estilo=='bullet' else 'párrafo'}:\n\n{texto}"
    messages = [
        {"role": "system", "content": "Eres un experto en resúmenes concisos."},
        {"role": "user", "content": prompt}
    ]
    return call_chat(messages)

def reescribir_tono(texto, tono="profesional"):
    """Reescribe un texto en un tono específico."""
    prompt = f"Reescribe este texto en tono {tono}, manteniendo el significado:\n\n{texto}"
    messages = [
        {"role": "system", "content": "Eres un editor experto en adaptar estilos."},
        {"role": "user", "content": prompt}
    ]
    return call_chat(messages, temperature=0.4)

mode = st.sidebar.selectbox(
    "Elige modo",
    ["Chat", "Resumen", "Reescritura de tono"]
)
    with st.sidebar.expander("Opciones avanzadas"):
        temp = st.sliden("Creatividad (temperature)", 0.0, 1.0, 0.3, 0.1)
        st.write("Modelo usado: gpt 4o-mini")

# -- Modo Chat-

If mode == "Chat":
    st.subheader("Chat sencillo con el modelo")
    if "history" not in st.session_state:
        st.session_state.history = [{"role":"system","content":"Eres un asistente amigable."}]
    for m in st.session_state.history[I:]:
        with st.chat_message("assistant" if m["role"] -- "assistant" else "user"):
            st.write(m["content"])

    prompt = st.chat_input("Escribe tu mensaje ... ")
    if prompt:
        st.session_state.history.append({"role":"user", "content":prompt} )
        with st.spinner("Pensando ... ");
            answer = call_chat(st.session_state.history, temperature=temp)
    st.session_state.history.append({"role":"assistant","content":answer})
    st.rerun()

# --- Modo Resomen - --
ellf mode == "Resumen":
    st.subheader(" Resumen de texto")
    text = st.text_area("Pega aqui el texto a resumir", height-200)
    style .- st.radio("Formato", ["bullet","parrafo"], horizontal=True)
    If st.button("Resumir"):
        with st.spioner("Generando resumen ... "):
            out - summarize(text, style-style)
        st.success("Resumen 1isto")
        st.write(out)

# --- Modo-Reascritora

elif mode == "Reescritura de tono":
    st.subheader(" Reescritura de texto con cambio de tono")
    text - st.text_area("Pega el texto a reescribir", height=200)
    tone: + st.selectbox("Selecciona el tono", ["profesional","cercano","ejecutivo","didáctico","enérgico"])
    if st.button("Reescribir"):
        with st.spinner("Reestribiendo ... "):
            out .= rewrite(text, tone=tone)
        st.success("Texto reescrito")
        st.write(out)

st.markdown(" --- ")
st.caption("Construido en Python + Streamlit . TEST rápida de IA Generativa")
