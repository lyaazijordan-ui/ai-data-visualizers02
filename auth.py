import streamlit as st
from supabase import create_client

# Connect to Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def signup(email, password):
    try:
        # Create the user in Supabase Auth
        supabase.auth.sign_up({"email": email, "password": password})
        
        # Immediately ensure there is a row in 'users' table
        supabase.table("users").upsert({"email": email}).execute()
        return True
    except Exception as e:
        print(e)
        return False

def login(email, password):
    try:
        # Authenticate user
        supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # Ensure the user row exists in 'users' table
        if not supabase.table("users").select("email").eq("email", email).execute().data:
            supabase.table("users").upsert({"email": email}).execute()
        return True
    except Exception as e:
        print(e)
        return False
