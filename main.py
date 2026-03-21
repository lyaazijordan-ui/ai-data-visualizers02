import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login, signup
from db import save_user_data, load_user_data
from ai import chat_with_ai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Intellectual AI", layout="wide")

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color: white;
}
h1 {
    text-align:center;
    color:#00f5d4;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

# ---------------- LOGIN ----------------
if st.session_state.page == "Login":
    st.title("🧠 Intellectual AI")
    st.caption("Where data meets intelligence")
    st.markdown("### ⚡ Smart Analytics • AI Insights • Intelligent Decisions")

    tab1, tab2 = st.tabs(["Login","Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(email,password):
                st.session_state.user = email
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid login")

    with tab2:
        email = st.text_input("New Email")
        password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if signup(email,password):
                st.success("Account created. Login now.")
            else:
                st.error("Signup failed")

# ---------------- SIDEBAR ----------------
if "user" in st.session_state:
    st.sidebar.title("🧠 Intellectual AI")
    st.sidebar.caption(f"Logged in as {st.session_state.user}")

    st.session_state.page = st.sidebar.radio(
        "Navigation",
        ["Dashboard","AI Assistant","Reports","Settings","Logout"]
    )

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    st.title("📊 Intellectual Dashboard")

    file = st.file_uploader("Upload CSV", type="csv")

    if file:
        df = pd.read_csv(file)
        save_user_data(st.session_state.user,"data", df.to_dict())
    else:
        data = load_user_data(st.session_state.user,"data")
        df = pd.DataFrame(data) if data else None

    if df is not None:
        st.dataframe(df.head())

        chart = st.selectbox("Chart Type", ["Line","Bar","Scatter"])
        x = st.selectbox("X-axis", df.columns)
        y = st.selectbox("Y-axis", df.columns)

        fig = px.line(df,x=x,y=y) if chart=="Line" else \
              px.bar(df,x=x,y=y) if chart=="Bar" else \
              px.scatter(df,x=x,y=y)

        st.plotly_chart(fig, use_container_width=True)

        st.download_button("⬇️ Download Chart", fig.to_html(), "chart.html")

# ---------------- AI ASSISTANT ----------------
if st.session_state.page == "AI Assistant":
    st.title("🤖 Intellectual AI Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = [{"role":"system","content":"You are a smart AI data assistant."}]

    user_input = st.text_input("Ask anything about your data or general questions...")

    if st.button("Send"):
        st.session_state.chat.append({"role":"user","content":user_input})
        reply = chat_with_ai(st.session_state.chat)
        st.session_state.chat.append({"role":"assistant","content":reply})

    for msg in st.session_state.chat:
        if msg["role"] != "system":
            st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")

# ---------------- REPORTS ----------------
if st.session_state.page == "Reports":
    st.title("📄 Reports")
    st.info("Download charts from dashboard. PDF system can be extended.")

# ---------------- SETTINGS ----------------
if st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    st.write("More features coming soon...")

# ---------------- LOGOUT ----------------
if st.session_state.page == "Logout":
    st.session_state.clear()
    st.rerun()
