import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login, signup
from db import save_user_data, load_user_data
from ai import chat_with_ai

st.set_page_config(page_title="ELAI AI DASHBOARD", layout="wide")

# ---------------- THEME ----------------
theme = st.selectbox("Theme", ["Neon Dark","Cyberpunk","Light","Minimal"])

if theme == "Neon Dark":
    st.markdown("<style>.stApp{background:linear-gradient(135deg,#000428,#004e92);color:white}</style>", unsafe_allow_html=True)
elif theme == "Cyberpunk":
    st.markdown("<style>.stApp{background:linear-gradient(135deg,#ff00cc,#333399);color:white}</style>", unsafe_allow_html=True)
elif theme == "Light":
    st.markdown("<style>.stApp{background:white;color:black}</style>", unsafe_allow_html=True)
elif theme == "Minimal":
    st.markdown("<style>.stApp{background:#f5f5f5;color:black}</style>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

# ---------------- LOGIN ----------------
if st.session_state.page == "Login":
    st.title("🚀 ELAI AI DASHBOARD")

    tab1, tab2 = st.tabs(["Login","Sign Up"])

    with tab1:
        u = st.text_input("Email")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(u,p):
                st.session_state.user = u
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid login")

    with tab2:
        u = st.text_input("New Email")
        p = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if signup(u,p):
                st.success("Account created")
            else:
                st.error("Signup failed")

# ---------------- SIDEBAR ----------------
if "user" in st.session_state:
    st.sidebar.title(f"👤 {st.session_state.user}")
    st.session_state.page = st.sidebar.radio(
        "Menu",
        ["Dashboard","AI Assistant","Reports","Settings","Logout"]
    )

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    st.title("📊 Dashboard")

    file = st.file_uploader("Upload CSV")

    if file:
        df = pd.read_csv(file)
        save_user_data(st.session_state.user,"data", df.to_dict())
    else:
        data = load_user_data(st.session_state.user,"data")
        df = pd.DataFrame(data) if data else None

    if df is not None:
        st.dataframe(df.head())

        chart = st.selectbox("Chart",["Line","Bar","Scatter"])
        x = st.selectbox("X",df.columns)
        y = st.selectbox("Y",df.columns)

        fig = px.line(df,x=x,y=y) if chart=="Line" else \
              px.bar(df,x=x,y=y) if chart=="Bar" else \
              px.scatter(df,x=x,y=y)

        st.plotly_chart(fig,use_container_width=True)

        st.download_button("Download Chart", fig.to_html(), "chart.html")

# ---------------- AI ASSISTANT ----------------
if st.session_state.page == "AI Assistant":
    st.title("🤖 AI Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = [{"role":"system","content":"You are a smart AI assistant."}]

    user_input = st.text_input("Ask anything...")

    if st.button("Send"):
        st.session_state.chat.append({"role":"user","content":user_input})

        reply = chat_with_ai(st.session_state.chat)

        st.session_state.chat.append({"role":"assistant","content":reply})

    for msg in st.session_state.chat:
        if msg["role"] != "system":
            st.write(f"**{msg['role']}:** {msg['content']}")

# ---------------- REPORTS ----------------
if st.session_state.page == "Reports":
    st.title("📄 Reports")
    st.info("You can export charts and summaries from dashboard")

# ---------------- SETTINGS ----------------
if st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    st.write("Theme already selectable at top")

# ---------------- LOGOUT ----------------
if st.session_state.page == "Logout":
    st.session_state.clear()
    st.rerun()
