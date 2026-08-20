"""Python World skill map."""

from __future__ import annotations

import streamlit as st

from adaptive import topic_unlocked
from engine import MASTERY_UNLOCK, MIN_ATTEMPTS_UNLOCK, TOPIC_LABELS, TOPICS_ORDER, get_skills
from ui import hud, inject, refresh_user, require_login

inject()
user = require_login()
if not user:
    st.stop()
refresh_user()
user = st.session_state.user
hud(user)

st.title("Python World")
st.caption("A node unlocks after the previous topic reaches mastery and enough attempts.")

skills = get_skills(user["id"])
for topic in TOPICS_ORDER:
    row = skills[topic]
    open_ = topic_unlocked(skills, topic)
    klass = "map-node" if open_ else "map-node locked"
    status = "UNLOCKED" if open_ else "LOCKED"
    bar = min(1.0, row["mastery"])
    st.markdown(
        f"""
        <div class="{klass}">
          <b>{TOPIC_LABELS[topic]}</b> · {status}<br/>
          Mastery {row['mastery']:.0%} · {row['n']} attempts
          {" · unlock next at " + f"{MASTERY_UNLOCK:.0%} / {MIN_ATTEMPTS_UNLOCK} tries" if open_ else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(bar)
