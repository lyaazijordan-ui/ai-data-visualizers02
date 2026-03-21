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
h1 {
    text-align:center;
    color:#00f5d4;
}
h2,h3,h4 {
    color:#00f5d4;
}
.stCaption {
    text-align: center;
    font-size:16px;
    color:#b0bec5;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN / SIGNUP ----------------
if st.session_state.page == "Login":
    st.title("🧠 Intellectual AI")
    st.caption("Where data meets intelligence")
    st.markdown("### ⚡ Smart Analytics • AI Insights • Intelligent Decisions")

    choice = st.radio("Choose action", ["Login", "Sign Up"], horizontal=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Proceed"):
        if choice == "Login":
            if login(email,password):
                st.session_state.user = email
                st.session_state.page = "Dashboard"
                st.experimental_rerun()
            else:
                st.error("Invalid login")
        else:
            if signup(email,password):
                st.success("Account created! You can now log in.")
            else:
                st.error("Signup failed")

# ---------------- AUTHORIZED NAVIGATION ----------------
if st.session_state.user and st.session_state.page != "Login":
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

        chart_type = st.selectbox("Chart Type", ["Line","Bar","Scatter"])
        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis", df.columns)

        # ---------------- Animated chart ----------------
        steps = 25
        for i in range(steps):
            subset = df.sample(frac=min(1,(i+1)/steps))
            if chart_type=="Line":
                fig = px.line(subset, x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Agsunset)
            elif chart_type=="Bar":
                fig = px.bar(subset, x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Agsunset)
            else:
                fig = px.scatter(subset, x=x_col, y=y_col, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Agsunset)
            fig.update_traces(marker=dict(size=10, line=dict(width=1, color='white')), selector=dict(mode='markers+lines'))
            fig.update_layout(hovermode="x unified", plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)

        st.download_button("⬇️ Download Chart HTML", fig.to_html(), "chart.html", mime="text/html")

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
    df = load_user_data(st.session_state.user,"data")
    if df:
        df = pd.DataFrame(df)
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        elements = [Paragraph("User Data Report", styles['Title'])]
        data_table = [df.columns.tolist()] + df.values.tolist()
        elements.append(Table(data_table))
        doc.build(elements)
        buffer.seek(0)
        st.download_button("Download PDF Report", buffer, file_name="report.pdf")
    else:
        st.info("No data available")

# ---------------- SETTINGS ----------------
if st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    theme = st.selectbox("Theme", ["plotly_dark","plotly_white"], index=0)
    chart_color = st.text_input("Default Chart Gradient", st.session_state.get("chart_color","Agsunset"))
    if st.button("Save Settings"):
        st.session_state["theme"] = theme
        st.session_state["chart_color"] = chart_color
        st.success("Settings saved!")

# ---------------- LOGOUT ----------------
if st.session_state.page == "Logout":
    st.session_state.clear()
    st.experimental_rerun()
