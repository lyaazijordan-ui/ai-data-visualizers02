# db.py
import streamlit as st

def save_data(key, df):
    st.session_state[key] = df

def load_data(key):
    return st.session_state.get(key)
