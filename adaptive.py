"""Adaptive skill updates, difficulty, map unlocks, XP, badges."""

from __future__ import annotations

from engine import (
    MASTERY_UNLOCK,
    MIN_ATTEMPTS_UNLOCK,
    TOPIC_LABELS,
    TOPICS_ORDER,
    badges_of,
    get_skills,
    get_user_by_id,
    log_attempt,
    mark_diagnostic_done,
    save_badges,
    set_skill,
    update_xp_streak,
    utcnow,
)

DIFFICULTY_RANK = {"beginner": 0, "intermediate": 1, "advanced": 2}


def topic_unlocked(skills: dict[str, dict], topic: str) -> bool:
    idx = TOPICS_ORDER.index(topic)
    if idx == 0:
        return True
    prev = TOPICS_ORDER[idx - 1]
    row = skills.get(prev, {"mastery": 0, "n": 0})
    return row["n"] >= MIN_ATTEMPTS_UNLOCK and row["mastery"] >= MASTERY_UNLOCK


def recommend_topic(skills: dict[str, dict]) -> str:
    unlocked = [t for t in TOPICS_ORDER if topic_unlocked(skills, t)]
    weakest = min(unlocked, key=lambda t: skills[t]["mastery"])
    strong = [t for t in unlocked if skills[t]["mastery"] >= 0.8 and skills[t]["n"] >= 3]
    if strong and skills[weakest]["mastery"] > 0.7:
        return strong[-1]
    return weakest


def recommend_difficulty(mastery: float) -> str:
    if mastery < 0.5:
        return "beginner"
    if mastery < 0.75:
        return "intermediate"
    return "advanced"


def update_mastery(mastery: float, correct: bool, hints_used: int, difficulty: str) -> float:
    weight = 0.22 + 0.06 * DIFFICULTY_RANK.get(difficulty, 1)
    observed = 1.0 if correct else 0.0
    if hints_used:
        observed *= max(0.35, 1.0 - 0.2 * hints_used)
    return mastery + weight * (observed - mastery)


def xp_for(correct: bool, hints_used: int) -> int:
    if not correct:
        return 0
    if hints_used:
        return 50
    return 100


def award_badges(user: dict, skills: dict[str, dict], streak: int) -> list[str]:
    badges = badges_of(user)
    add = []
    if user["xp"] >= 100 and "Python Beginner" not in badges:
        add.append("Python Beginner")
    loops = skills.get("loops", {})
    if loops.get("mastery", 0) >= 0.8 and loops.get("n", 0) >= 4 and "Loop Master" not in badges:
        add.append("Loop Master")
    if streak >= 7 and "Debugging Ninja" not in badges:
        add.append("Debugging Ninja")
    oop = skills.get("oop", {})
    if oop.get("n", 0) >= 3 and "OOP Explorer" not in badges:
        add.append("OOP Explorer")
    files = skills.get("files", {})
    if files.get("mastery", 0) >= 0.7 and files.get("n", 0) >= 3 and "Data Science Warrior" not in badges:
        add.append("Data Science Warrior")
    if add:
        badges = badges + add
        save_badges(user["id"], badges)
    return badges


def apply_attempt(
    user_id: int,
    topic: str,
    question_id: str,
    difficulty: str,
    answer: int | None,
    correct: bool,
    response_time: float,
    hints_used: int,
    attempt_number: int,
) -> dict:
    user = get_user_by_id(user_id)
    assert user is not None
    skills = get_skills(user_id)
    row = skills[topic]
    new_m = update_mastery(row["mastery"], correct, hints_used, difficulty)
    set_skill(user_id, topic, new_m, row["n"] + 1)
    log_attempt(
        user_id,
        topic,
        question_id,
        difficulty,
        answer,
        correct,
        response_time,
        hints_used,
        attempt_number,
    )
    gained = xp_for(correct, hints_used)
    xp = user["xp"] + gained
    streak = user["streak"] + 1 if correct else 0
    last = utcnow() if correct else user["last_correct_at"]
    update_xp_streak(user_id, xp, streak, last)
    user = get_user_by_id(user_id)
    assert user is not None
    skills = get_skills(user_id)
    badges = award_badges(user, skills, streak)
    return {
        "xp_gained": gained,
        "xp": user["xp"],
        "streak": user["streak"],
        "mastery": skills[topic]["mastery"],
        "badges": badges,
        "level": level_for(user["xp"]),
    }


def level_for(xp: int) -> int:
    return 1 + xp // 400


def next_learn(skills: dict[str, dict]) -> tuple[str, str]:
    unlocked = [t for t in TOPICS_ORDER if topic_unlocked(skills, t)]
    locked = [t for t in TOPICS_ORDER if t not in unlocked]
    weakest = min(unlocked, key=lambda t: (skills[t]["mastery"], -skills[t]["n"]))
    label = TOPIC_LABELS[weakest]
    if skills[weakest]["mastery"] < MASTERY_UNLOCK:
        why = (
            f"Improve {label} first. Mastery is {skills[weakest]['mastery']:.0%} — "
            "later topics assume you can use this idea without guessing."
        )
        return label, why
    if locked:
        nxt = TOPIC_LABELS[locked[0]]
        why = f"{label} looks solid. Unlock {nxt} by keeping this streak of correct, untimed practice."
        return nxt, why
    return label, "Python World is open. Stretch advanced items in your strongest topics."


def finish_diagnostic(user_id: int) -> None:
    mark_diagnostic_done(user_id)
