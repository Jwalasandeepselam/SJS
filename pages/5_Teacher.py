"""Teacher / class analytics view."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from engine import (
    TOPIC_LABELS,
    TOPICS_ORDER,
    attempts_for,
    claim_student,
    get_skills,
    get_teacher_students,
)
from ui import hud, inject, refresh_user, require_login

inject()
user = require_login(role_required="teacher")
if not user:
    st.stop()

refresh_user()
user = st.session_state.user
hud(user)

st.title("Teacher Dashboard & Performance Analyzer")
st.caption("Observe student progress via Unique Student IDs, evaluate performance tiers, and intervene where support is needed.")

st.markdown("### 📌 Add Student to Observation")
col_input, col_btn = st.columns([3, 1])
with col_input:
    claim_input = st.text_input(
        "Enter Unique Student ID",
        placeholder="e.g. STU-A1B2C3",
        key="claim_id_input",
        help="Ask your student for their unique Student ID displayed on their home dashboard.",
    )
with col_btn:
    st.write("<div style='margin-top: 1.75rem;'></div>", unsafe_allow_html=True)
    claim_btn = st.button("Add Student ➔", use_container_width=True)

if claim_btn:
    if not claim_input.strip():
        st.error("Please enter a valid Student ID.")
    else:
        status, msg = claim_student(user["id"], claim_input.strip())
        if status == "success":
            st.success(msg)
            st.rerun()
        elif status == "info":
            st.info(msg)
        else:
            st.error(msg)

st.markdown("---")

claimed_students = get_teacher_students(user["id"])

if not claimed_students:
    st.info(
        "💡 **No students currently under observation.**\n\n"
        "Ask your students for their unique **Student ID (`STU-XXXXXX`)** and enter it above to start observing their learning profile."
    )
    st.stop()

# Analyze performance for claimed students
student_analyses = []
skill_rows = []

for s in claimed_students:
    skills = get_skills(s["id"])
    attempts = attempts_for(s["id"])
    avg_mastery = sum(skills[t]["mastery"] for t in TOPICS_ORDER) / len(TOPICS_ORDER)
    weakest_topic_key = min(TOPICS_ORDER, key=lambda t: skills[t]["mastery"])
    weakest_topic_name = TOPIC_LABELS[weakest_topic_key]
    weakest_mastery = skills[weakest_topic_key]["mastery"]

    if avg_mastery >= 0.65:
        category = "Performing Well"
        cat_badge = "🟢 Performing Well"
        color = "#166534"
    elif avg_mastery >= 0.40:
        category = "Moderate"
        cat_badge = "🟡 Moderate Performance"
        color = "#854D0E"
    else:
        category = "Struggling"
        cat_badge = "🔴 Needs Intervention"
        color = "#991B1B"

    uni_info = s.get("uni_id_card") or "Unverified"
    if uni_info.startswith("REG:"):
        verify_str = f"🛡️ Reg No: `{uni_info[5:]}`"
    elif uni_info.startswith("CARD:"):
        verify_str = f"🛡️ ID Card Uploaded (`{uni_info[6:]}`)"
    elif uni_info != "Unverified":
        verify_str = f"🛡️ Verified (`{uni_info}`)"
    else:
        verify_str = "⚠️ Pending Verification"

    student_analyses.append(
        {
            "student": s,
            "username": s["username"],
            "uid": s["student_uid"],
            "avg_mastery": avg_mastery,
            "category": category,
            "cat_badge": cat_badge,
            "weakest_topic": weakest_topic_name,
            "weakest_mastery": weakest_mastery,
            "total_attempts": len(attempts),
            "xp": s["xp"],
            "streak": s["streak"],
            "skills": skills,
            "verify_str": verify_str,
        }
    )
    skill_rows.append(
        {
            "Student": s["username"],
            "Student ID": s["student_uid"],
            "Verification": verify_str,
            "Category": category,
            "Overall Mastery": f"{avg_mastery:.0%}",
            **{TOPIC_LABELS[t]: f"{skills[t]['mastery']:.0%}" for t in TOPICS_ORDER},
        }
    )

well_count = sum(1 for a in student_analyses if a["category"] == "Performing Well")
mod_count = sum(1 for a in student_analyses if a["category"] == "Moderate")
struggle_count = sum(1 for a in student_analyses if a["category"] == "Struggling")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Observed Students", len(claimed_students))
c2.metric("🟢 Performing Well", well_count)
c3.metric("🟡 Moderate", mod_count)
c4.metric("🔴 Needs Intervention", struggle_count)

st.markdown("### 📊 Student Clarity & Performance Breakdown")
tab_struggle, tab_mod, tab_well, tab_all = st.tabs(
    [
        f"🔴 Needs Intervention ({struggle_count})",
        f"🟡 Moderate ({mod_count})",
        f"🟢 Performing Well ({well_count})",
        "📋 All Observed Class Data",
    ]
)

with tab_struggle:
    struggling_list = [a for a in student_analyses if a["category"] == "Struggling"]
    if not struggling_list:
        st.success("Great news! None of your observed students are currently in the struggling tier.")
    else:
        st.warning("These students are below 40% overall mastery and require targeted intervention:")
        for item in struggling_list:
            with st.expander(f"🔴 {item['username']} ({item['uid']}) — Overall Mastery: {item['avg_mastery']:.0%}"):
                st.markdown(
                    f"""
                    **Student ID:** `{item['uid']}` | {item['verify_str']} | **XP:** {item['xp']} | **Streak:** {item['streak']} | **Attempts:** {item['total_attempts']}<br/>
                    ⚠️ **Weakest Topic:** {item['weakest_topic']} ({item['weakest_mastery']:.0%} mastery)
                    """,
                    unsafe_allow_html=True,
                )
                st.write("**Topic Breakdown:**")
                cols = st.columns(len(TOPICS_ORDER))
                for idx, t in enumerate(TOPICS_ORDER):
                    cols[idx].metric(TOPIC_LABELS[t], f"{item['skills'][t]['mastery']:.0%}")

with tab_mod:
    mod_list = [a for a in student_analyses if a["category"] == "Moderate"]
    if not mod_list:
        st.info("No students currently in the moderate tier.")
    else:
        for item in mod_list:
            with st.expander(f"🟡 {item['username']} ({item['uid']}) — Overall Mastery: {item['avg_mastery']:.0%}"):
                st.markdown(
                    f"**Student ID:** `{item['uid']}` | {item['verify_str']} | **Weakest Topic:** {item['weakest_topic']} ({item['weakest_mastery']:.0%})"
                )
                cols = st.columns(len(TOPICS_ORDER))
                for idx, t in enumerate(TOPICS_ORDER):
                    cols[idx].metric(TOPIC_LABELS[t], f"{item['skills'][t]['mastery']:.0%}")

with tab_well:
    well_list = [a for a in student_analyses if a["category"] == "Performing Well"]
    if not well_list:
        st.info("No students currently in the high performing tier.")
    else:
        for item in well_list:
            with st.expander(f"🟢 {item['username']} ({item['uid']}) — Overall Mastery: {item['avg_mastery']:.0%}"):
                st.markdown(
                    f"**Student ID:** `{item['uid']}` | {item['verify_str']} | **XP:** {item['xp']} | **Streak:** {item['streak']}"
                )
                cols = st.columns(len(TOPICS_ORDER))
                for idx, t in enumerate(TOPICS_ORDER):
                    cols[idx].metric(TOPIC_LABELS[t], f"{item['skills'][t]['mastery']:.0%}")

with tab_all:
    skill_df = pd.DataFrame(skill_rows)
    st.dataframe(skill_df, use_container_width=True, hide_index=True)

# Topic Averages Chart
means = {
    TOPIC_LABELS[t]: sum(a["skills"][t]["mastery"] for a in student_analyses) / len(student_analyses)
    for t in TOPICS_ORDER
}
st.markdown("### 📈 Class Topic Mastery Overview")
fig = px.bar(
    x=list(means.keys()),
    y=list(means.values()),
    title="Observed Class Mean Mastery by Topic",
    color_discrete_sequence=["#0284C7"],
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
