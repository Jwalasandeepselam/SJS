"""XP leaderboard."""

from __future__ import annotations

import streamlit as st

from adaptive import level_for
from engine import list_users
from ui import hud, inject, refresh_user, require_login

inject()
user = require_login()
if not user:
    st.stop()
refresh_user()
user = st.session_state.user
hud(user)

st.title("Arena leaderboard")
players = list_users()
for i, p in enumerate(players, start=1):
    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
    you = " ← you" if p["id"] == user["id"] else ""
    st.markdown(
        f"<div class='card'>{medal} <b>{p['username']}</b> · LV {level_for(p['xp'])} · "
        f"{p['xp']} XP · 🔥 {p['streak']}{you}</div>",
        unsafe_allow_html=True,
    )
