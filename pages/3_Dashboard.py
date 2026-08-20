"""Student dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from adaptive import level_for, next_learn
from engine import TOPIC_LABELS, TOPICS_ORDER, attempts_for, badges_of, get_skills
from ui import hud, inject, refresh_user, require_login

inject()
user = require_login()
if not user:
    st.stop()
refresh_user()
user = st.session_state.user
hud(user)

st.title(f"Welcome {user['username']}")
skills = get_skills(user["id"])
rows = attempts_for(user["id"])
overall = sum(skills[t]["mastery"] for t in TOPICS_ORDER) / len(TOPICS_ORDER)
weakest = min(TOPICS_ORDER, key=lambda t: skills[t]["mastery"])
learn, why = next_learn(skills)

a, b, c, d = st.columns(4)
a.metric("Level", level_for(user["xp"]))
b.metric("XP", user["xp"])
c.metric("Streak", user["streak"])
d.metric("Overall skill", f"{overall:.0%}")

st.markdown("#### What should I learn next?")
st.info(f"**{learn}** — {why}")
st.markdown(f"**Today's mission:** complete 5 challenges in **{TOPIC_LABELS[weakest]}**.")

st.markdown("#### Skill bars")
for t in TOPICS_ORDER:
    st.write(f"{TOPIC_LABELS[t]} — {skills[t]['mastery']:.0%}")
    st.progress(min(1.0, skills[t]["mastery"]))

badges = badges_of(user)
st.markdown("#### Badges")
if badges:
    st.markdown("".join(f'<span class="badge">🏅 {b}</span>' for b in badges), unsafe_allow_html=True)
else:
    st.caption("Earn XP and streaks to unlock badges.")

if rows:
    df = pd.DataFrame(rows)
    df["topic_name"] = df["topic"].map(TOPIC_LABELS)
    fig = px.bar(
        df.groupby("topic_name")["correct"].mean().reset_index(),
        x="topic_name",
        y="correct",
        title="Accuracy by topic",
        color_discrete_sequence=["#0D9488"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#0F172A",
        font_family="Noto Sans, sans-serif",
        yaxis_tickformat=".0%",
        yaxis_range=[0, 1],
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(
        df[["timestamp", "topic", "difficulty", "correct", "hints_used", "response_time"]],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.caption("Play a few questions to populate analytics.")
