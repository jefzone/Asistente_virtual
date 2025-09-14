import streamlit as st
import os
from langchain_openai import ChatOpenAI

# Carga la clave desde Streamlit Secrets o variable de entorno
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# Configuración del modelo LLM
llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=OPENAI_API_KEY
)
