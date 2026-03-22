import requests
import streamlit as st

API_KEY = st.secrets["OPENROUTER_API_KEY"]

def chat_with_ai(messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": messages
        }
    )

    return response.json()["choices"][0]["message"]["content"]
