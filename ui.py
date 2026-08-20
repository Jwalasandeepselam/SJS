"""Shared Streamlit chrome."""

from __future__ import annotations

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600;1,700&family=Fira+Code:wght@400;500;600&display=swap');

:root {
  --background-color: #FAF9F6 !important;
  --secondary-background-color: #F4F3EF !important;
  --text-color: #1E293B !important;
  --primary-color: #0D9488 !important;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"], section.main, .stApp {
  background-color: #FAF9F6 !important;
  color: #1E293B !important;
  font-family: 'Noto Sans', sans-serif !important;
}

[data-testid="stHeader"] {
  background: rgba(250, 249, 246, 0.9) !important;
  backdrop-filter: blur(8px);
}

[data-testid="stSidebar"], section[data-testid="stSidebar"] {
  background-color: #F4F3EF !important;
  border-right: 1px solid #E2E8F0 !important;
}

[data-testid="stSidebar"] * {
  color: #1E293B !important;
  font-family: 'Noto Sans', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Noto Sans', sans-serif !important;
  font-weight: 700 !important;
  color: #0F172A !important;
  letter-spacing: -0.02em;
}

p, span, label, div, button, input, textarea {
  font-family: 'Noto Sans', sans-serif;
}

.hero {
  border: 1px solid #E2E8F0;
  background: #FFFFFF;
  border-radius: 20px;
  padding: 1.75rem 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.kicker {
  color: #0D9488;
  font-family: 'Fira Code', monospace;
  font-weight: 600;
  font-size: 0.82rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.hud {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin: 1rem 0 1.5rem;
}

.hud .chip {
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-radius: 999px;
  padding: 0.4rem 1rem;
  font-family: 'Noto Sans', sans-serif;
  font-weight: 600;
  font-size: 0.88rem;
  color: #0F172A;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  color: #1E293B;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}

.badge {
  display: inline-block;
  margin: 0.2rem 0.3rem 0.2rem 0;
  background: #F0FDF4;
  border: 1px solid #86EFAC;
  color: #166534;
  border-radius: 8px;
  padding: 0.25rem 0.65rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.map-node {
  border-left: 4px solid #0D9488;
  padding: 0.75rem 1rem;
  margin: 0.5rem 0;
  background: #FFFFFF;
  border-radius: 0 12px 12px 0;
  border-top: 1px solid #E2E8F0;
  border-right: 1px solid #E2E8F0;
  border-bottom: 1px solid #E2E8F0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
}

.map-node.locked {
  border-left-color: #94A3B8;
  opacity: 0.65;
  background: #F8FAFC;
}

.stButton>button {
  background: linear-gradient(135deg, #0D9488 0%, #0284C7 100%) !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
  font-family: 'Noto Sans', sans-serif !important;
  border: 0 !important;
  border-radius: 10px !important;
  padding: 0.5rem 1rem !important;
  box-shadow: 0 2px 4px rgba(13, 148, 136, 0.2) !important;
}

.stButton>button:hover {
  filter: brightness(1.08) !important;
  box-shadow: 0 4px 8px rgba(13, 148, 136, 0.3) !important;
}

div[data-baseweb="input"] > div {
  background-color: #FFFFFF !important;
  border-color: #CBD5E1 !important;
  color: #0F172A !important;
  border-radius: 8px !important;
}

input {
  color: #0F172A !important;
  font-family: 'Noto Sans', sans-serif !important;
}

[data-testid="stMetric"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 14px !important;
  padding: 0.85rem 1.15rem !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
}

[data-testid="stMetricValue"] {
  color: #0F172A !important;
  font-family: 'Noto Sans', sans-serif !important;
  font-weight: 700 !important;
}

[data-testid="stMetricLabel"] {
  color: #475569 !important;
  font-family: 'Noto Sans', sans-serif !important;
}

div[data-testid="stNotification"], div[data-testid="stAlert"] {
  border-radius: 12px !important;
  font-family: 'Noto Sans', sans-serif !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
}

/* Progress bar styling */
div[data-testid="stProgressBar"] > div {
  background-color: #E2E8F0 !important;
  border-radius: 999px !important;
}

div[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, #0D9488, #0284C7) !important;
  border-radius: 999px !important;
}

/* Radio buttons */
div[data-testid="stRadio"] label p {
  font-family: 'Noto Sans', sans-serif !important;
  color: #0F172A !important;
  font-weight: 500 !important;
}

/* Code blocks */
pre, code, div[data-testid="stMarkdownContainer"] code {
  background-color: #F1F0EA !important;
  color: #0F172A !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 8px !important;
  font-family: 'Fira Code', monospace !important;
}

/* Dataframe styling */
[data-testid="stDataFrame"] {
  background-color: #FFFFFF !important;
  border: 1px solid #E2E8F0 !important;
  border-radius: 12px !important;
}

.stTabs [data-baseweb="tab-list"] {
  gap: 8px;
}

.stTabs [data-baseweb="tab"] {
  font-family: 'Noto Sans', sans-serif !important;
  font-weight: 600;
  color: #64748B;
}

.stTabs [aria-selected="true"] {
  color: #0D9488 !important;
}

/* Sidebar flex ordering to put custom logo at the top */
section[data-testid="stSidebar"] > div {
  display: flex !important;
  flex-direction: column !important;
}

[data-testid="stSidebarUserContent"] {
  order: -1 !important;
}
</style>
"""


def inject() -> None:
    from engine import init_db

    init_db()
    user = st.session_state.get("user")
    user_logged_in = bool(user)
    st.set_page_config(
        page_title="AdaptiveAI",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded" if user_logged_in else "collapsed",
    )
    st.markdown(CSS, unsafe_allow_html=True)
    if not user_logged_in:
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"], [data-testid="stSidebarNav"], section[data-testid="stSidebar"] {
                display: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown(
            """
            <div style="display: flex; align-items: center; gap: 0.7rem; padding: 0.5rem 0.2rem 0.8rem 0.2rem; border-bottom: 1px solid #E2E8F0; margin-bottom: 0.8rem;">
                <div style="background: linear-gradient(135deg, #0D9488, #0284C7); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.35rem; box-shadow: 0 3px 8px rgba(13, 148, 136, 0.25);">
                    🎮
                </div>
                <div>
                    <div style="font-weight: 800; font-size: 1.25rem; letter-spacing: -0.02em; color: #0F172A; line-height: 1.1;">AdaptiveAI</div>
                    <div style="font-family: 'Fira Code', monospace; font-size: 0.65rem; color: #0D9488; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Personalized Learning</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if user and user.get("role") == "student":
            st.markdown(
                """
                <style>
                [data-testid="stSidebarNav"] li:has(a[href*="5_Teacher"]), 
                [data-testid="stSidebarNav"] a[href*="5_Teacher"] {
                    display: none !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )


def require_login(role_required: str | None = None) -> dict | None:
    user = st.session_state.get("user")
    if not user:
        st.warning("Log in from **Home** to enter the game.")
        st.page_link("app.py", label="← Back to Home")
        return None
    if role_required == "teacher" and user.get("role") == "student":
        st.error("🔒 Access Denied: Teacher View is restricted to Teacher accounts.")
        st.page_link("app.py", label="← Back to Home")
        return None
    return user


def hud(user: dict) -> None:
    from adaptive import level_for

    role_label = {
        "student": "🎓 Student",
        "teacher": "👩‍🏫 Teacher",
        "other": "👤 Educator",
    }.get(user.get("role", "student"), "👤 Member")

    uid_chip = f'<div class="chip">🆔 {user["student_uid"]}</div>' if user.get("student_uid") else ""

    st.markdown(
        f"""
        <div class="hud">
          <div class="chip">{role_label}</div>
          <div class="chip">👤 {user['username']}</div>
          {uid_chip}
          <div class="chip">🏆 LV {level_for(user['xp'])}</div>
          <div class="chip">✨ {user['xp']} XP</div>
          <div class="chip">🔥 {user['streak']} streak</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def refresh_user() -> None:
    from engine import get_user_by_id

    uid = st.session_state.get("user", {}).get("id")
    if uid:
        st.session_state.user = get_user_by_id(uid)
