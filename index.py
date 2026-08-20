"""AdaptiveAI — Vercel Serverless Web Application Entry Point."""

from __future__ import annotations

import os
import random
import sys
import time
from pathlib import Path
from flask import Flask, jsonify, render_template, request, session

# Add root project folder to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import adaptive
import engine

app = Flask(
    __name__,
    template_folder=str(ROOT_DIR / "templates"),
    static_folder=str(ROOT_DIR / "static"),
    static_url_path="/static",
)
app.secret_key = os.environ.get("SECRET_KEY", "adaptiveai-vercel-secret-key-2026")

# Export for Vercel WSGI / Serverless handler
handler = app
application = app

engine.init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/me", methods=["GET"])
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"user": None})
    user = engine.get_user_by_id(uid)
    if not user:
        session.clear()
        return jsonify({"user": None})
    return jsonify({
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user.get("role", "student"),
            "student_uid": user.get("student_uid"),
            "uni_id_card": user.get("uni_id_card"),
            "xp": user["xp"],
            "streak": user["streak"],
            "diagnostic_done": bool(user["diagnostic_done"]),
            "badges": engine.badges_of(user),
            "level": adaptive.level_for(user["xp"]),
        }
    })


@app.route("/api/auth/register", methods=["POST"])
def register():
    role = request.form.get("role", "student").lower()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    verify_method = request.form.get("verify_method", "reg_num")
    reg_num = request.form.get("reg_num", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if engine.get_user(username):
        return jsonify({"error": "That username is already taken."}), 400

    uni_data = None
    if verify_method == "reg_num":
        if not reg_num:
            return jsonify({"error": "University Registration Number is required for verification."}), 400
        uni_data = f"REG: {reg_num}"
    else:
        file = request.files.get("id_card_file")
        if not file or file.filename == "":
            return jsonify({"error": "University ID Card file is required for verification."}), 400
        saved_name = f"{username}_{file.filename}"
        save_path = engine.ID_CARDS_DIR / saved_name
        save_path.parent.mkdir(parents=True, exist_ok=True)
        file.save(save_path)
        uni_data = f"CARD: {saved_name}"

    user = engine.create_user(username, password, role=role, uni_id_card=uni_data)
    session["user_id"] = user["id"]
    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "student_uid": user["student_uid"],
            "xp": user["xp"],
            "streak": user["streak"],
            "diagnostic_done": bool(user["diagnostic_done"]),
            "badges": engine.badges_of(user),
            "level": adaptive.level_for(user["xp"]),
        }
    })


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form
    username = data.get("username", "").strip()
    password = data.get("password", "")
    user = engine.authenticate(username, password)
    if not user:
        return jsonify({"error": "Invalid username or wrong password."}), 401
    session["user_id"] = user["id"]
    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user.get("role", "student"),
            "student_uid": user.get("student_uid"),
            "xp": user["xp"],
            "streak": user["streak"],
            "diagnostic_done": bool(user["diagnostic_done"]),
            "badges": engine.badges_of(user),
            "level": adaptive.level_for(user["xp"]),
        }
    })


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})


@app.route("/api/play/next", methods=["GET"])
def play_next():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required."}), 401
    user = engine.get_user_by_id(uid)
    if not user:
        return jsonify({"error": "User not found."}), 404

    catalog = engine.load_catalog()
    questions = catalog["questions"]

    is_diagnostic = not bool(user["diagnostic_done"])

    if is_diagnostic:
        diag_idx = session.get("diag_idx", 0)
        if diag_idx >= len(engine.TOPICS_ORDER):
            engine.mark_diagnostic_done(user["id"])
            session.pop("diag_idx", None)
            return jsonify({"diagnostic_completed": True})

        target_topic = engine.TOPICS_ORDER[diag_idx]
        pool = [q for q in questions if q["topic"] == target_topic]
        beg = [q for q in pool if q["difficulty"] == "beginner"] or pool
        chosen = beg[0]
        session["current_q_id"] = chosen["id"]
        session["q_started"] = time.time()
        return jsonify({
            "mode": "diagnostic",
            "progress": f"Question {diag_idx + 1} of {len(engine.TOPICS_ORDER)}",
            "question": {
                "id": chosen["id"],
                "topic": chosen["topic"],
                "topic_name": engine.TOPIC_LABELS[chosen["topic"]],
                "difficulty": chosen["difficulty"],
                "prompt": chosen["prompt"],
                "choices": chosen["choices"],
                "hints": chosen["hints"],
            }
        })
    else:
        skills = engine.get_skills(user["id"])
        topic = adaptive.recommend_topic(skills)
        diff = adaptive.recommend_difficulty(skills[topic]["mastery"])
        pool = [q for q in questions if q["topic"] == topic and q["difficulty"] == diff] or [q for q in questions if q["topic"] == topic]
        chosen = random.choice(pool)
        session["current_q_id"] = chosen["id"]
        session["q_started"] = time.time()
        return jsonify({
            "mode": "adaptive",
            "mastery_info": f"Live {engine.TOPIC_LABELS[topic]} Mastery: {skills[topic]['mastery']:.0%}",
            "question": {
                "id": chosen["id"],
                "topic": chosen["topic"],
                "topic_name": engine.TOPIC_LABELS[chosen["topic"]],
                "difficulty": chosen["difficulty"],
                "prompt": chosen["prompt"],
                "choices": chosen["choices"],
                "hints": chosen["hints"],
            }
        })


@app.route("/api/play/submit", methods=["POST"])
def play_submit():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required."}), 401
    user = engine.get_user_by_id(uid)
    data = request.get_json(silent=True) or request.form
    q_id = data.get("question_id") or session.get("current_q_id")
    chosen_idx = int(data.get("choice_index", -1))
    hints_used = int(data.get("hints_used", 0))

    if chosen_idx < 0:
        return jsonify({"error": "Please select an answer option."}), 400

    catalog = engine.load_catalog()
    by_id = {q["id"]: q for q in catalog["questions"]}
    q = by_id.get(q_id)
    if not q:
        return jsonify({"error": "Question not found."}), 404

    correct = (chosen_idx == q["answer"])
    started = session.get("q_started", time.time())
    elapsed = max(1.0, time.time() - started)

    diag_idx = session.get("diag_idx", 0)
    attempt_num = diag_idx + 1 if not user["diagnostic_done"] else 1

    result = adaptive.apply_attempt(
        user["id"],
        q["topic"],
        q["id"],
        q["difficulty"],
        chosen_idx,
        correct,
        elapsed,
        hints_used,
        attempt_number=attempt_num,
    )

    if not user["diagnostic_done"]:
        session["diag_idx"] = diag_idx + 1

    updated_user = engine.get_user_by_id(user["id"])

    return jsonify({
        "correct": correct,
        "picked": q["choices"][chosen_idx],
        "target": q["choices"][q["answer"]],
        "explain": q["explain"],
        "prompt": q["prompt"],
        "topic": engine.TOPIC_LABELS[q["topic"]],
        "xp_gained": result["xp_gained"],
        "new_xp": result["xp"],
        "streak": result["streak"],
        "mastery": result["mastery"],
        "level": adaptive.level_for(updated_user["xp"]),
    })


@app.route("/api/chat/doubt", methods=["POST"])
def chat_doubt():
    data = request.get_json(silent=True) or request.form
    topic = data.get("topic", "Python Concept")
    picked = data.get("picked", "Selected Option")
    target = data.get("target", "Target Answer")
    explain = data.get("explain", "Explanation")
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Message query is required."}), 400

    q_lower = query.lower()
    if "why" in q_lower or "explain" in q_lower or "how" in q_lower:
        reply = (
            f"In Python **{topic}**, choosing `{picked}` is incorrect because: {explain}. "
            f"The target `{target}` follows standard syntax rules and ensures proper execution."
        )
    elif "example" in q_lower or "code" in q_lower:
        reply = (
            f"Here is a code example illustrating **{topic}**:\n\n"
            f"```python\n# Targeted Concept: {target}\n# Principle: {explain}\n```\n"
            "Try running similar patterns to strengthen your memory!"
        )
    else:
        reply = (
            f"Great question on **{topic}**! Remember that `{target}` is the expected standard. "
            f"{explain} Keep practicing!"
        )

    return jsonify({"reply": reply})


@app.route("/api/skill_map", methods=["GET"])
def skill_map():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required."}), 401
    skills = engine.get_skills(uid)
    nodes = []
    for t in engine.TOPICS_ORDER:
        unlocked = adaptive.topic_unlocked(skills, t)
        row = skills[t]
        nodes.append({
            "id": t,
            "name": engine.TOPIC_LABELS[t],
            "unlocked": unlocked,
            "mastery": row["mastery"],
            "attempts": row["n"],
            "unlock_threshold": f"{engine.MASTERY_UNLOCK:.0%} mastery & {engine.MIN_ATTEMPTS_UNLOCK} attempts",
        })
    return jsonify({"nodes": nodes})


@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required."}), 401
    user = engine.get_user_by_id(uid)
    skills = engine.get_skills(uid)
    rows = engine.attempts_for(uid)
    overall = sum(skills[t]["mastery"] for t in engine.TOPICS_ORDER) / len(engine.TOPICS_ORDER)
    weakest = min(engine.TOPICS_ORDER, key=lambda t: skills[t]["mastery"])
    learn, why = adaptive.next_learn(skills)

    topic_accuracy = {}
    for t in engine.TOPICS_ORDER:
        topic_attempts = [r for r in rows if r["topic"] == t]
        if topic_attempts:
            acc = sum(1 for r in topic_attempts if r["correct"]) / len(topic_attempts)
            topic_accuracy[engine.TOPIC_LABELS[t]] = round(acc * 100, 1)
        else:
            topic_accuracy[engine.TOPIC_LABELS[t]] = 0.0

    return jsonify({
        "overall_mastery": overall,
        "weakest_topic": engine.TOPIC_LABELS[weakest],
        "next_learn": learn,
        "next_learn_why": why,
        "skills": {engine.TOPIC_LABELS[t]: skills[t]["mastery"] for t in engine.TOPICS_ORDER},
        "accuracy_by_topic": topic_accuracy,
        "attempts": rows[-20:],
    })


@app.route("/api/leaderboard", methods=["GET"])
def leaderboard():
    players = engine.list_users()
    current_uid = session.get("user_id")
    board = []
    for i, p in enumerate(players, start=1):
        board.append({
            "rank": i,
            "username": p["username"],
            "role": p.get("role", "student"),
            "level": adaptive.level_for(p["xp"]),
            "xp": p["xp"],
            "streak": p["streak"],
            "is_you": (p["id"] == current_uid),
        })
    return jsonify({"leaderboard": board})


@app.route("/api/teacher/claim", methods=["POST"])
def teacher_claim():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required."}), 401
    user = engine.get_user_by_id(uid)
    if not user or user.get("role") == "student":
        return jsonify({"error": "Access Denied: Teacher permissions required."}), 403

    data = request.get_json(silent=True) or request.form
    student_uid = data.get("student_uid", "").strip()
    if not student_uid:
        return jsonify({"error": "Student ID is required."}), 400

    status, msg = engine.claim_student(user["id"], student_uid)
    return jsonify({"status": status, "message": msg})


@app.route("/api/teacher/students", methods=["GET"])
def teacher_students():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"error": "Authentication required."}), 401
    user = engine.get_user_by_id(uid)
    if not user or user.get("role") == "student":
        return jsonify({"error": "Access Denied: Teacher permissions required."}), 403

    claimed = engine.get_teacher_students(user["id"])
    analyses = []
    for s in claimed:
        skills = engine.get_skills(s["id"])
        attempts = engine.attempts_for(s["id"])
        avg_m = sum(skills[t]["mastery"] for t in engine.TOPICS_ORDER) / len(engine.TOPICS_ORDER)
        weakest_key = min(engine.TOPICS_ORDER, key=lambda t: skills[t]["mastery"])

        if avg_m >= 0.65:
            cat = "Performing Well"
        elif avg_m >= 0.40:
            cat = "Moderate"
        else:
            cat = "Needs Intervention"

        uni_info = s.get("uni_id_card") or "Unverified"
        if uni_info.startswith("REG:"):
            verify_str = f"Reg No: {uni_info[5:]}"
        elif uni_info.startswith("CARD:"):
            verify_str = f"ID Card Uploaded ({uni_info[6:]})"
        else:
            verify_str = uni_info

        analyses.append({
            "id": s["id"],
            "username": s["username"],
            "student_uid": s["student_uid"],
            "verification": verify_str,
            "overall_mastery": avg_m,
            "category": cat,
            "weakest_topic": engine.TOPIC_LABELS[weakest_key],
            "weakest_mastery": skills[weakest_key]["mastery"],
            "attempts_count": len(attempts),
            "xp": s["xp"],
            "streak": s["streak"],
            "skills": {engine.TOPIC_LABELS[t]: skills[t]["mastery"] for t in engine.TOPICS_ORDER},
        })

    return jsonify({"students": analyses})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
