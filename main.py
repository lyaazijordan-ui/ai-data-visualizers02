import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login, signup
from db import save_user_data, load_user_data
from ai import analyze_data, ask_ai

st.set_page_config(page_title="ELAI AI DASHBOARD", layout="wide")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Login"

# ---------------- LOGIN ----------------
if st.session_state.page == "Login":
    st.title("🚀 ELAI AI DASHBOARD")

    tab1, tab2 = st.tabs(["Login","Sign Up"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(u,p):
                st.session_state.user = u
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid login")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")

        if st.button("Create"):
            if signup(u,p):
                st.success("Account created")
            else:
                st.error("User exists")

# ---------------- SIDEBAR ----------------
if "user" in st.session_state:
    st.sidebar.title(f"👤 {st.session_state.user}")
    st.session_state.page = st.sidebar.radio(
        "Menu",
        ["Dashboard","AI","Reports","Settings","Logout"]
    )

# ---------------- DASHBOARD ----------------
if st.session_state.page == "Dashboard":
    st.title("📊 Dashboard")

    file = st.file_uploader("Upload CSV")

    if file:
        df = pd.read_csv(file)
        save_user_data(st.session_state.user, "data", df.to_dict())
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

# ---------------- AI INSIGHTS ----------------
if st.session_state.page == "AI":
    st.title("🤖 AI Engine")

    data = load_user_data(st.session_state.user,"data")
    df = pd.DataFrame(data) if data else None

    if df is not None:
        st.subheader("Auto Insights")
        st.write(analyze_data(df))

        question = st.text_input("Ask your data")

        if st.button("Ask AI"):
            st.write(ask_ai(df, question))

    else:
        st.warning("Upload data first")

# ---------------- REPORTS ----------------
if st.session_state.page == "Reports":
    st.title("📄 Reports")

    st.info("PDF export ready (simplified)")

# ---------------- SETTINGS ----------------
if st.session_state.page == "Settings":
    st.title("⚙️ Settings")

    theme = st.selectbox("Theme",["dark","light"])

    if st.button("Save"):
        save_user_data(st.session_state.user,"theme",theme)
        st.success("Saved")

# ---------------- LOGOUT ----------------
if st.session_state.page == "Logout":
    st.session_state.clear()
    st.rerun()
