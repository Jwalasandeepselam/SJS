"""AdaptiveAI — home, auth, and product landing."""

from __future__ import annotations

import streamlit as st

from engine import authenticate, create_user, get_user, init_db
from ui import hud, inject, refresh_user

init_db()

if "user" not in st.session_state:
    st.session_state.user = None

inject()

user = st.session_state.user

if not user:
    # Landing page layout before login: description on left, credentials on right
    left, right = st.columns([1.2, 0.8], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero">
              <div class="kicker">IDP · PERSONALIZED LEARNING GAME</div>
              <h1 style="margin-top: 0.3rem;">AdaptiveAI</h1>
              <p style="font-size: 1.05rem; line-height: 1.6; color: #334155;">
                An intelligent, personalized learning platform for Python programming. 
                Instead of fixed quizzes with static scores, AdaptiveAI continuously evaluates 
                student behavior, builds real-time skill estimates, dynamically tunes challenge 
                difficulty, and provides AI-guided staged hints for every learner.
              </p>
            </div>
            <div class="card">
              <h3 style="margin-top: 0;">🌐 Python World Roadmap</h3>
              <p style="color: #475569; margin-bottom: 0.75rem;">
                Progress through interconnected skill nodes as your mastery grows:
              </p>
              <div style="font-family: 'Fira Code', monospace; background: #F8FAFC; padding: 0.75rem 1rem; border-radius: 10px; border: 1px solid #E2E8F0; color: #0D9488; font-weight: 500;">
                START ➔ Variables ➔ Conditions ➔ Loops ➔ Functions ➔ OOP ➔ File Handling
              </div>
            </div>
            <div class="card">
              <h3 style="margin-top: 0;">⚡ Key Features</h3>
              <ul style="color: #334155; line-height: 1.8; margin-bottom: 0; padding-left: 1.2rem;">
                <li><b>Adaptive Topic & Difficulty:</b> Question sequence evolves based on your live skill profile.</li>
                <li><b>Staged AI Tutor Hints:</b> Hints scale with your attempt struggle before revealing answers.</li>
                <li><b>Gamified Progression:</b> Earn XP, maintain daily streaks, and unlock achievements.</li>
                <li><b>Analytics Dashboards:</b> Deep insights for both students and instructors.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("Player Credentials")
        st.caption("Sign in or create a player profile to unlock your personalized learning map.")
        tab_login, tab_join = st.tabs(["Log in", "Create player"])
        with tab_login:
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("Log in", use_container_width=True):
                logged_user = authenticate(u, p)
                if logged_user:
                    st.session_state.user = logged_user
                    st.success(f"Welcome back, {logged_user['username']}!")
                    st.rerun()
                else:
                    st.error("Unknown player or wrong password.")
        with tab_join:
            role = st.selectbox("Select Account Role", ["Student", "Teacher", "Other"], key="join_role")
            u2 = st.text_input("Pick a username", key="join_u")
            p2 = st.text_input("Pick a password", type="password", key="join_p")

            st.markdown("#### 🛡️ Identity Verification (Fraud Prevention)")
            verify_method = st.radio(
                "Select Verification Method",
                ["University Registration Number", "Upload University ID Card"],
                key="join_verify_method",
                horizontal=True,
            )

            reg_num_input = ""
            id_card_file = None

            if verify_method == "University Registration Number":
                reg_num_input = st.text_input(
                    "University Registration Number",
                    placeholder="e.g. REG-2024-99812",
                    key="join_reg_num",
                    help="Enter your official University Registration / Roll Number.",
                )
            else:
                id_card_file = st.file_uploader(
                    "Upload University ID Card Image/PDF",
                    type=["png", "jpg", "jpeg", "pdf"],
                    key="join_id_card",
                    help="Upload a clear picture or PDF of your official University ID Card.",
                )

            if st.button("Create Account", use_container_width=True):
                if not u2.strip() or not p2:
                    st.error("Username and password required.")
                elif get_user(u2.strip()):
                    st.error("That username is taken.")
                elif verify_method == "University Registration Number" and not reg_num_input.strip():
                    st.error("University Registration Number is required for verification.")
                elif verify_method == "Upload University ID Card" and not id_card_file:
                    st.error("University ID Card file upload is required for verification.")
                else:
                    if verify_method == "University Registration Number":
                        verification_data = f"REG: {reg_num_input.strip()}"
                    else:
                        from pathlib import Path
                        saved_filename = f"{u2.strip()}_{id_card_file.name}"
                        save_path = Path(__file__).resolve().parent / "data" / "id_cards" / saved_filename
                        save_path.parent.mkdir(parents=True, exist_ok=True)
                        save_path.write_bytes(id_card_file.getbuffer())
                        verification_data = f"CARD: {saved_filename}"

                    role_str = role.lower()
                    new_u = create_user(u2, p2, role=role_str, uni_id_card=verification_data)
                    st.session_state.user = new_u
                    st.success(f"Account created successfully as {role}! Identity verified via {verify_method}.")
                    st.rerun()

else:
    # Authenticated view after login: show HUD & options
    refresh_user()
    user = st.session_state.user

    role_title = user.get("role", "student").title()
    uid_str = f" · Student ID: {user['student_uid']}" if user.get("student_uid") else ""

    st.markdown(
        f"""
        <div class="hero">
          <div class="kicker">WELCOME BACK · {role_title.upper()} ACCOUNT{uid_str}</div>
          <h1 style="margin-top: 0.3rem;">Hello, {user['username']}! 👋</h1>
          <p style="color: #334155;">Your personalized Python learning arena is ready. Select an option below or use the sidebar navigation to jump into action.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hud(user)

    st.subheader("Game Options & Navigation")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="card">
                <h3 style="margin-top: 0;">🎮 Play / Diagnostic</h3>
                <p style="color: #475569;">Start adaptive problem solving or complete your initial skill diagnostic.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_Play.py", label="Go to Play Mode ➔", use_container_width=True)

        st.markdown(
            """
            <div class="card" style="margin-top: 1rem;">
                <h3 style="margin-top: 0;">📊 Student Dashboard</h3>
                <p style="color: #475569;">View your personalized progress, accuracy charts, and recommended next topics.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/3_Dashboard.py", label="View Dashboard ➔", use_container_width=True)

    with c2:
        st.markdown(
            """
            <div class="card">
                <h3 style="margin-top: 0;">🗺️ Skill Map</h3>
                <p style="color: #475569;">Explore your Python World skill tree and track unlocked topic nodes.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link("pages/2_Skill_Map.py", label="Explore Skill Map ➔", use_container_width=True)

        if user.get("role") != "student":
            st.markdown(
                """
                <div class="card" style="margin-top: 1rem;">
                    <h3 style="margin-top: 0;">👩‍🏫 Teacher View & Leaderboard</h3>
                    <p style="color: #475569;">Analyze student performance, observe student IDs, or check XP standings.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            sub1, sub2 = st.columns(2)
            with sub1:
                st.page_link("pages/4_Leaderboard.py", label="Leaderboard 🏆", use_container_width=True)
            with sub2:
                st.page_link("pages/5_Teacher.py", label="Teacher View 👩‍🏫", use_container_width=True)
        else:
            st.markdown(
                """
                <div class="card" style="margin-top: 1rem;">
                    <h3 style="margin-top: 0;">🏆 Arena Leaderboard</h3>
                    <p style="color: #475569;">Compare your XP standings and streaks on the class leaderboard.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.page_link("pages/4_Leaderboard.py", label="Leaderboard 🏆", use_container_width=True)

    st.markdown("---")
    if st.button("Log out", use_container_width=False):
        st.session_state.user = None
        st.rerun()

