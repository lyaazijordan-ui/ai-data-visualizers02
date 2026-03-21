import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def save_user_data(user,key,value):
    supabase.table("users").upsert({
        "email": user,
        key: str(value)
    }).execute()

def load_user_data(user,key):
    res = supabase.table("users").select(key).eq("email",user).execute()
    if res.data:
        return eval(res.data[0][key])
    return None
