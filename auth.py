import streamlit as st
from db import save_user_remote, load_user_remote

def login(username, password):
    data = load_user_remote(username, "account") or {}
    if data.get("password")==password:
        st.session_state["username"]=username
        st.session_state.update(load_user_remote(username, "settings") or {})
        return True
    return False

def signup(username, password):
    if load_user_remote(username, "account") is None:
        save_user_remote(username, "account", {"password":password})
        save_user_remote(username, "settings", {"theme":"plotly_dark","chart_color":"Agsunset"})
        return True
    return False

def load_user_settings(username):
    return load_user_remote(username, "settings") or {}

def save_user_settings(username, theme, chart_color):
    save_user_remote(username, "settings", {"theme":theme,"chart_color":chart_color})
