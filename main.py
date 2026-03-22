import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
import time

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
h1 {text-align:center; color:#00f5d4;}
h2,h3,h4 {color:#00f5d4;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if st.session_state.page == "Login":
    st.title("🧠 Intellectual AI")
    st.caption("Where data meets intelligence")

    choice = st.radio("Action", ["Login","Sign Up"], horizontal=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Continue"):
        if choice == "Login":
            if login(email, password):
                st.session_state.user = email
                st.session_state.page = "Dashboard"
                st.rerun()   # ✅ FIXED
            else:
                st.error("Login failed")

        else:
            if signup(email, password):
                st.success("Account created. Now login.")
            else:
                st.error("Signup failed")

# ---------------- SIDEBAR ----------------
if st.session_state.user:
    st.sidebar.title("🧠 Intellectual AI")
    st.sidebar.caption(f"{st.session_state.user}")

    st.session_state.page = st.sidebar.radio(
        "Navigation",
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

        chart = st.selectbox("Chart Type", ["Line","Bar","Scatter"])
        x = st.selectbox("X-axis", df.columns)
        y = st.selectbox("Y-axis", df.columns)

        # -------- ANIMATED CHART --------
        steps = 20
        for i in range(steps):
            subset = df.sample(frac=min(1,(i+1)/steps))

            if chart == "Line":
                fig = px.line(subset, x=x, y=y, template="plotly_dark")
            elif chart == "Bar":
                fig = px.bar(subset, x=x, y=y, template="plotly_dark")
            else:
                fig = px.scatter(subset, x=x, y=y, template="plotly_dark")

            fig.update_traces(marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)

        st.download_button("Download HTML", fig.to_html(), "chart.html")

# ---------------- AI ----------------
if st.session_state.page == "AI Assistant":
    st.title("🤖 AI Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = [{"role":"system","content":"You are helpful AI."}]

    user_input = st.text_input("Ask something...")

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

    data = load_user_data(st.session_state.user,"data")

    if data:
        df = pd.DataFrame(data)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        elements = [Paragraph("Data Report", styles["Title"])]
        table = [df.columns.tolist()] + df.values.tolist()
        elements.append(Table(table))

        doc.build(elements)
        buffer.seek(0)

        st.download_button("Download PDF", buffer, "report.pdf")

# ---------------- SETTINGS ----------------
if st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    st.write("More features coming soon")

# ---------------- LOGOUT ----------------
if st.session_state.page == "Logout":
    st.session_state.clear()
    st.rerun()   # ✅ FIXED
