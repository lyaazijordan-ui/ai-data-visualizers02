import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def signup(email, password):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        print("SIGNUP RESPONSE:", res)

        return True
    except Exception as e:
        st.error(f"Signup error: {e}")
        return False


def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        print("LOGIN RESPONSE:", res)

        return True
    except Exception as e:
        st.error(f"Login error: {e}")
        return False
