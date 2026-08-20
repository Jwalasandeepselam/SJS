"""Play loop: diagnostic then adaptive questions with staged hints."""

from __future__ import annotations

import random
import time

import streamlit as st

from adaptive import (
    apply_attempt,
    finish_diagnostic,
    recommend_difficulty,
    recommend_topic,
)
from engine import TOPIC_LABELS, TOPICS_ORDER, get_skills, load_catalog
from ui import hud, inject, refresh_user, require_login

inject()
user = require_login()
if not user:
    st.stop()

refresh_user()
user = st.session_state.user
hud(user)

catalog = load_catalog()
questions = catalog["questions"]
by_id = {q["id"]: q for q in questions}


def pick_diagnostic() -> list[dict]:
    picked = []
    for topic in TOPICS_ORDER:
        pool = [q for q in questions if q["topic"] == topic]
        # one beginner-ish item per topic
        beg = [q for q in pool if q["difficulty"] == "beginner"] or pool
        picked.append(beg[0])
    return picked


def pick_adaptive(skills: dict) -> dict | None:
    topic = recommend_topic(skills)
    diff = recommend_difficulty(skills[topic]["mastery"])
    pool = [q for q in questions if q["topic"] == topic and q["difficulty"] == diff]
    if not pool:
        pool = [q for q in questions if q["topic"] == topic]
    seen = st.session_state.get("seen_ids", [])
    fresh = [q for q in pool if q["id"] not in seen]
    choice = random.choice(fresh or pool)
    return choice


def ensure_item(diagnostic: bool) -> None:
    if diagnostic:
        queue = st.session_state.setdefault("diag_queue", [q["id"] for q in pick_diagnostic()])
        idx = st.session_state.setdefault("diag_idx", 0)
        if idx >= len(queue):
            st.session_state.current_q = None
            return
        st.session_state.current_q = by_id[queue[idx]]
        return
    if not st.session_state.get("current_q"):
        skills = get_skills(user["id"])
        st.session_state.current_q = pick_adaptive(skills)


st.title("Play")

# Handle AI Chatbot Doubt Clarifier state
if "active_doubt" not in st.session_state:
    st.session_state.active_doubt = None

if st.session_state.get("last_feedback"):
    fb = st.session_state.pop("last_feedback")
    if fb["correct"]:
        st.success(
            f"Correct! +{fb['xp']} XP · mastery now {fb['mastery']:.0%} · streak {fb['streak']}"
        )
        st.session_state.active_doubt = None
    else:
        st.error(f"Not quite. +{fb['xp']} XP.")
        st.caption(f"Your pick: {fb['picked']} · Target: {fb['target']}")
        st.session_state.active_doubt = {
            "prompt": fb["prompt"],
            "picked": fb["picked"],
            "target": fb["target"],
            "explain": fb["explain"],
            "topic": fb["topic"],
            "chat_history": [
                {
                    "role": "assistant",
                    "content": (
                        f"🤖 **AI Doubt Tutor**: You selected **`{fb['picked']}`**, but the correct target is **`{fb['target']}`**.\n\n"
                        f"💡 **Concept Breakdown:** {fb['explain']}\n\n"
                        "Ask any follow-up question below if you have any doubt about this topic!"
                    ),
                }
            ],
        }

# Render AI Doubt Clarifier Chatbot if active
if st.session_state.active_doubt:
    doubt = st.session_state.active_doubt
    with st.expander("🤖 AI Doubt Clarifier Chatbot (Click to open/close)", expanded=True):
        st.markdown(f"**Topic:** {doubt['topic']}")
        for msg in doubt["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_query = st.chat_input("Ask the AI Tutor to explain your doubt...", key="doubt_chat_input")
        if user_query:
            doubt["chat_history"].append({"role": "user", "content": user_query})
            # Generate AI tutor explanation
            q_lower = user_query.lower()
            if "why" in q_lower or "explain" in q_lower or "how" in q_lower:
                ai_resp = (
                    f"In Python **{doubt['topic']}**, `{doubt['picked']}` does not satisfy the requirement. "
                    f"The correct option `{doubt['target']}` is preferred because: {doubt['explain']}. "
                    "Always double check syntax, variable scopes, and return values!"
                )
            elif "example" in q_lower or "code" in q_lower:
                ai_resp = (
                    f"Here is a code example related to **{doubt['topic']}**:\n\n"
                    f"```python\n# Target concept: {doubt['target']}\n"
                    f"# Explanation: {doubt['explain']}\n```\n"
                    "Try writing this out in your code editor to solidify the concept!"
                )
            else:
                ai_resp = (
                    f"Great question! Focusing on **{doubt['topic']}**: remember that `{doubt['target']}` is the standard choice. "
                    f"{doubt['explain']} Keep practicing to master this node!"
                )

            doubt["chat_history"].append({"role": "assistant", "content": ai_resp})
            st.rerun()

diagnostic = not bool(user["diagnostic_done"])
if diagnostic:
    st.info("Phase 1 — Diagnostic. One question per Python World node. This seeds your skill profile.")
else:
    st.success("Adaptive mode. Difficulty and topic follow your live mastery, not a fixed quiz.")

if "hints_used" not in st.session_state:
    st.session_state.hints_used = 0
if "q_started" not in st.session_state:
    st.session_state.q_started = time.time()
if "seen_ids" not in st.session_state:
    st.session_state.seen_ids = []

ensure_item(diagnostic)
q = st.session_state.get("current_q")

if diagnostic and q is None:
    finish_diagnostic(user["id"])
    refresh_user()
    st.balloons()
    st.success("Diagnostic complete. Your map is live — keep playing to adapt.")
    if st.button("Start adaptive run"):
        st.session_state.diag_queue = []
        st.session_state.diag_idx = 0
        st.rerun()
    st.stop()

if not q:
    st.warning("No question available.")
    st.stop()

st.caption(
    f"{TOPIC_LABELS[q['topic']]} · {q['difficulty'].title()} · id `{q['id']}`"
)
st.markdown(q["prompt"])

choice = st.radio("Your answer", q["choices"], index=None, key=f"ans_{q['id']}")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Need a hint"):
        st.session_state.hints_used = min(3, st.session_state.hints_used + 1)
with c2:
    submit = st.button("Lock in answer", type="primary")
with c3:
    why = st.button("Why is this hard?")

if st.session_state.hints_used:
    for i in range(st.session_state.hints_used):
        st.warning(f"Hint {i + 1}: {q['hints'][i]}")

if why:
    skills = get_skills(user["id"])
    m = skills[q["topic"]]["mastery"]
    st.info(
        f"Tutor: your {TOPIC_LABELS[q['topic']]} mastery is {m:.0%}. "
        f"This item is tagged {q['difficulty']}. "
        "Use hints before the full explanation — struggle is part of the loop."
    )

if submit:
    if choice is None:
        st.error("Pick an option first.")
    else:
        idx = q["choices"].index(choice)
        correct = idx == q["answer"]
        elapsed = time.time() - st.session_state.q_started
        result = apply_attempt(
            user["id"],
            q["topic"],
            q["id"],
            q["difficulty"],
            idx,
            correct,
            elapsed,
            st.session_state.hints_used,
            attempt_number=st.session_state.get("diag_idx", 0) + 1,
        )
        st.session_state.seen_ids = list(set(st.session_state.seen_ids + [q["id"]]))
        st.session_state.last_feedback = {
            "correct": correct,
            "xp": result["xp_gained"],
            "mastery": result["mastery"],
            "streak": result["streak"],
            "explain": q["explain"],
            "picked": choice,
            "target": q["choices"][q["answer"]],
            "prompt": q["prompt"],
            "topic": TOPIC_LABELS[q["topic"]],
        }
        refresh_user()
        st.session_state.hints_used = 0
        st.session_state.q_started = time.time()
        st.session_state.current_q = None
        if diagnostic:
            st.session_state.diag_idx = st.session_state.get("diag_idx", 0) + 1
        st.rerun()
