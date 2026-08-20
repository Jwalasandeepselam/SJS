"""SQLite persistence for AdaptiveAI — Vercel Serverless Ready."""

from __future__ import annotations

import hashlib
import json
import os
import random
import sqlite3
import string
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def get_db_path() -> Path:
    try:
        d = ROOT / "data"
        d.mkdir(parents=True, exist_ok=True)
        test_file = d / ".write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return d / "adaptiveai.sqlite"
    except Exception:
        d = Path("/tmp/adaptiveai_data")
        d.mkdir(parents=True, exist_ok=True)
        return d / "adaptiveai.sqlite"


def get_id_cards_dir() -> Path:
    try:
        d = ROOT / "data" / "id_cards"
        d.mkdir(parents=True, exist_ok=True)
        test_file = d / ".write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return d
    except Exception:
        d = Path("/tmp/adaptiveai_data/id_cards")
        d.mkdir(parents=True, exist_ok=True)
        return d


def get_questions_path() -> Path:
    candidates = [
        ROOT / "data" / "questions.json",
        ROOT.parent / "data" / "questions.json",
        Path("/var/task/data/questions.json"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


TOPICS_ORDER = ["variables", "conditions", "loops", "functions", "oop", "files"]
TOPIC_LABELS = {
    "variables": "Variables",
    "conditions": "Conditions",
    "loops": "Loops",
    "functions": "Functions",
    "oop": "OOP",
    "files": "File Handling",
}
MASTERY_UNLOCK = 0.72
MIN_ATTEMPTS_UNLOCK = 3


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_password(password: str, salt: str = "adaptiveai-v1") -> str:
    return hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()


def generate_student_uid() -> str:
    digits = "".join(random.choices(string.digits + string.ascii_uppercase, k=6))
    return f"STU-{digits}"


def connect() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    get_id_cards_dir().mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student',
                student_uid TEXT,
                uni_id_card TEXT,
                claimed_by_teacher_id INTEGER,
                created_at TEXT NOT NULL,
                xp INTEGER NOT NULL DEFAULT 0,
                streak INTEGER NOT NULL DEFAULT 0,
                last_correct_at TEXT,
                diagnostic_done INTEGER NOT NULL DEFAULT 0,
                badges TEXT NOT NULL DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS skills (
                user_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                mastery REAL NOT NULL DEFAULT 0.0,
                n INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, topic),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                question_id TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                answer INTEGER,
                correct INTEGER NOT NULL,
                response_time REAL,
                hints_used INTEGER NOT NULL DEFAULT 0,
                attempt_number INTEGER NOT NULL DEFAULT 1,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES users(id)
            );
            """
        )
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        cols = [col["name"] for col in cursor.fetchall()]
        if "role" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'student'")
        if "student_uid" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN student_uid TEXT")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_student_uid ON users(student_uid)")
        if "uni_id_card" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN uni_id_card TEXT")
        if "claimed_by_teacher_id" not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN claimed_by_teacher_id INTEGER")


def load_catalog() -> dict:
    p = get_questions_path()
    return json.loads(p.read_text(encoding="utf-8"))


def get_user(username: str) -> dict | None:
    init_db()
    with connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE LOWER(username) = ?", (username.strip().lower(),)).fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    init_db()
    with connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def get_user_by_student_uid(student_uid: str) -> dict | None:
    init_db()
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE UPPER(student_uid) = ?",
            (student_uid.strip().upper(),),
        ).fetchone()
        return dict(row) if row else None


def create_user(
    username: str,
    password: str,
    role: str = "student",
    uni_id_card: str | None = None,
) -> dict:
    init_db()
    student_uid = generate_student_uid() if role == "student" else None
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO users (username, password_hash, role, student_uid, uni_id_card, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (username.strip(), hash_password(password), role, student_uid, uni_id_card, utcnow()),
        )
        uid = cur.lastrowid
        for topic in TOPICS_ORDER:
            conn.execute(
                "INSERT INTO skills (user_id, topic, mastery, n) VALUES (?, ?, 0.0, 0)",
                (uid, topic),
            )
    user = get_user_by_id(uid)
    assert user is not None
    return user


def authenticate(username: str, password: str) -> dict | None:
    init_db()
    user = get_user(username)
    if not user:
        return None
    if user["password_hash"] != hash_password(password):
        return None
    return user


def claim_student(teacher_id: int, student_uid: str) -> tuple[str, str]:
    init_db()
    student = get_user_by_student_uid(student_uid)
    if not student:
        return ("error", "Student ID not found. Please verify the unique ID.")
    if student.get("role", "student") != "student":
        return ("error", "The provided ID does not belong to a student account.")
    
    existing_teacher = student.get("claimed_by_teacher_id")
    if existing_teacher and existing_teacher != teacher_id:
        return ("error", "This student is already in observation with someone else.")
    
    if existing_teacher == teacher_id:
        return ("info", f"Student {student['username']} ({student['student_uid']}) is already in your observation list.")
        
    with connect() as conn:
        conn.execute(
            "UPDATE users SET claimed_by_teacher_id = ? WHERE id = ?",
            (teacher_id, student["id"]),
        )
    return ("success", f"Student {student['username']} ({student['student_uid']}) added to your observation list!")


def get_teacher_students(teacher_id: int) -> list[dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM users WHERE claimed_by_teacher_id = ? ORDER BY username",
            (teacher_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def list_users() -> list[dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY xp DESC, username").fetchall()
        return [dict(r) for r in rows]


def get_skills(user_id: int) -> dict[str, dict]:
    init_db()
    with connect() as conn:
        rows = conn.execute("SELECT * FROM skills WHERE user_id = ?", (user_id,)).fetchall()
        return {r["topic"]: dict(r) for r in rows}


def badges_of(user: dict) -> list[str]:
    raw = user.get("badges") or "[]"
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_badges(user_id: int, badges: list[str]) -> None:
    init_db()
    with connect() as conn:
        conn.execute("UPDATE users SET badges = ? WHERE id = ?", (json.dumps(badges), user_id))


def update_xp_streak(user_id: int, xp: int, streak: int, last_correct_at: str | None) -> None:
    init_db()
    with connect() as conn:
        conn.execute(
            "UPDATE users SET xp = ?, streak = ?, last_correct_at = ? WHERE id = ?",
            (xp, streak, last_correct_at, user_id),
        )


def mark_diagnostic_done(user_id: int) -> None:
    init_db()
    with connect() as conn:
        conn.execute("UPDATE users SET diagnostic_done = 1 WHERE id = ?", (user_id,))


def log_attempt(
    student_id: int,
    topic: str,
    question_id: str,
    difficulty: str,
    answer: int | None,
    correct: bool,
    response_time: float,
    hints_used: int,
    attempt_number: int,
) -> None:
    init_db()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO attempts (
                student_id, topic, question_id, difficulty, answer, correct,
                response_time, hints_used, attempt_number, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                topic,
                question_id,
                difficulty,
                answer,
                int(correct),
                response_time,
                hints_used,
                attempt_number,
                utcnow(),
            ),
        )


def set_skill(user_id: int, topic: str, mastery: float, n: int) -> None:
    init_db()
    with connect() as conn:
        conn.execute(
            "UPDATE skills SET mastery = ?, n = ? WHERE user_id = ? AND topic = ?",
            (max(0.0, min(1.0, mastery)), n, user_id, topic),
        )


def attempts_for(user_id: int | None = None) -> list[dict]:
    init_db()
    with connect() as conn:
        if user_id is None:
            rows = conn.execute("SELECT * FROM attempts ORDER BY timestamp").fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM attempts WHERE student_id = ? ORDER BY timestamp",
                (user_id,),
            ).fetchall()
        return [dict(r) for r in rows]
