# src/ui/app.py
import os

import streamlit as st
import requests 

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("Smart Contract Analyst")

# 1. Widget d'upload
uploaded_file = st.file_uploader("Dépose ton rapport financier (PDF)", type="pdf")

if uploaded_file:
    # On envoie le fichier à l'API FastAPI
    with st.spinner("Ingestion en cours..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/ingest", files={"file": uploaded_file})
        if response.status_code == 200:
            st.success("Fichier indexé !")

# 2. Widget de chat
question = st.chat_input("Pose ta question sur le document...")

if question:
    # On affiche la question
    st.write(f"**Vous :** {question}")
    
    # On appelle l'API FastAPI
    payload = {"question": question}
    res = requests.post(f"{API_URL}/query", json=payload)
    
    if res.status_code == 200:
        data = res.json()
        st.write(f"**Assistant :** {data['answer']}")
        with st.expander("Sources"):
            st.json(data['sources'])