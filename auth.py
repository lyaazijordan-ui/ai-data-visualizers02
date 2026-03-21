# auth.py
import streamlit as st

# Demo persistent memory for users
if "users" not in st.session_state:
    st.session_state["users"] = {}

def login(username, password):
    users = st.session_state["users"]
    if username in users and users[username]["password"] == password:
        st.session_state["username"] = username
        return True
    return False

def signup(username, password):
    users = st.session_state["users"]
    if username not in users:
        users[username] = {"password": password, "theme":"plotly_dark", "chart_color":"Agsunset"}
        return True
    return False

def load_user_settings(username):
    users = st.session_state["users"]
    return users.get(username, {})

def save_user_settings(username, theme, chart_color):
    users = st.session_state["users"]
    if username in users:
        users[username]["theme"] = theme
        users[username]["chart_color"] = chart_color
