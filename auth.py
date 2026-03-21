# auth.py
import streamlit as st

# In-memory user storage (demo)
users = {}

def login(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state["username"] = username
        return True
    return False

def signup(username, password):
    if username not in users:
        users[username] = {"password": password, "theme":"plotly_dark", "chart_color":"Agsunset"}
        return True
    return False

def load_user_settings(username):
    return users.get(username, {})

def save_user_settings(username, theme, chart_color):
    if username in users:
        users[username]["theme"] = theme
        users[username]["chart_color"] = chart_color
