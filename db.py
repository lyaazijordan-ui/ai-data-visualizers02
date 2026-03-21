import streamlit as st
import pandas as pd

def save_data(key, df):
    st.session_state[key] = df

def load_data(key):
    return st.session_state.get(key)

# -----------------------------
# Supabase-like persistent user storage
# -----------------------------
def save_user_remote(username, key, value):
    if "remote_users" not in st.session_state:
        st.session_state["remote_users"] = {}
    if username not in st.session_state["remote_users"]:
        st.session_state["remote_users"][username]={}
    st.session_state["remote_users"][username][key] = value

def load_user_remote(username, key=None):
    if "remote_users" not in st.session_state:
        return None
    user = st.session_state["remote_users"].get(username)
    if not user:
        return None
    if key:
        return user.get(key)
    return user
