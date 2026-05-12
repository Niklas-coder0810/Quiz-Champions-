# app.py
import streamlit as st
import random

st.set_page_config(page_title="Ultimatives Allgemeinwissens Quiz", page_icon="🧠", layout="centered")

# =========================
# FRAGENBANK
# =========================

questions = []

# -------------------------
# ABC FRAGEN
# -------------------------
abc_questions = [
    {
        "question": "Was ist die Hauptstadt von Deutschland?",
        "options": ["Berlin", "Hamburg", "München"],
        "answer": "Berlin"
    },
    {
        "question": "Welcher Planet ist der größte?",
        "options": ["Mars", "Jupiter", "Venus"],
        "answer": "Jupiter"
    },
    {
        "question": "Wie viele Kontinente gibt es?",
        "options": ["5", "6", "7"],
        "answer": "7"
    },
]

# -------------------------
# WAHR / FALSCH
# -------------------------
true_false_questions = [
    {
        "question": "Die Sonne ist ein Planet.",
        "answer": False
    },
    {
        "question": "Wasser gefriert bei 0 Grad Celsius.",
        "answer": True
    },
    {
        "question": "Ein Jahr hat 500 Tage.",
        "answer": False
    },
]

# -------------------------
# SCHÄTZFRAGEN
# +/- 10%
# -------------------------
estimate_questions = [
    {
        "question": "Wie hoch ist der Mount Everest in Metern?",
        "answer": 8849
    },
    {
        "question": "Wie viele Knochen hat ein erwachsener Mensch?",
        "answer": 206
    },
    {
        "question": "Wie viele Länder gibt es ungefähr auf der Erde?",
        "answer": 195
    },
]

# =========================
# 1000 FRAGEN ERZEUGEN
# =========================

while len(questions) < 1000:
    qtype = random.choice(["abc", "tf", "estimate"])

    if qtype == "abc":
        q = random.choice(abc_questions).copy()
        q["type"] = "abc"

    elif qtype == "tf":
        q = random.choice(true_false_questions).copy()
        q["type"] = "tf"

    else:
        q = random.choice(estimate_questions).copy()
        q["type"] = "estimate"

    questions.append(q)

# =========================
# LEVEL SYSTEM
# =========================

levels = {
    "Anfänger": {
        "range": (0, 250),
        "points": 1
    },
    "Amateur": {
        "range": (250, 500),
        "points": 2
    },
    "Profi": {
        "range": (500, 750),
        "points": 3
    },
    "Quiz Master": {
        "range": (750, 1000),
        "points": 4
    }
}

# =========================
# SESSION STATE
# =========================

if "started" not in st.session_state:
    st.session_state.started = False

if "scores" not in st.session_state:
    st.session_state.scores = []

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = None

# =========================
# STARTMENÜ
# =========================

if not st.session_state.started:

    st.title("🧠 Ultimatives Allgemeinwissens Quiz")

    player_count = st.selectbox(
        "Wie viele Spieler?",
        [1, 2, 3, 4]
    )

    player_names = []

    for i in range(player_count):
        name = st.text_input(f"Name Spieler {i+1}", key=f"name_{i}")

        if name == "":
            name = f"Spieler {i+1}"

        player_names.append(name)

    level = st.selectbox(
        "Wähle ein Level",
        list(levels.keys())
    )

    target_points = st.number_input(
        "Bis wie viele Punkte wird gespielt?",
        min_value=5,
        max_value=100,
        value=10
    )

    if st.button("Spiel starten"):

        st.session_state.started = True
        st.session_state.players = player_names
        st.session_state.scores = [0] * player_count
        st.session_state.level = level
        st.session_state.target_points = target_points
        st.session_state.turn = 0

        level_range = levels[level]["range"]

        st.session_state.available_questions = questions[
            level_range[0]:level_range[1]
        ]

        st.rerun()

# =========================
# SPIEL
# =========================

else:

    st.title("🎯 Quiz läuft")

    current_player = st.session_state.players[st.session_state.turn]

    st.subheader(f"Jetzt dran: {current_player}")

    # Punktestand anzeigen
    st.write("## Punktestand")

    for i, player in enumerate(st.session_state.players):
        st.write(f"{player}: {st.session_state.scores[i]} Punkte")

    # Gewinner prüfen
    for i, score in enumerate(st.session_state.scores):
        if score >= st.session_state.target_points:
            st.success(f"🏆 {st.session_state.players[i]} hat gewonnen!")
            st.stop()

    # Neue Frage erzeugen
    if st.session_state.current_question is None:
        st.session_state.current_question = random.choice(
            st.session_state.available_questions
        )

    q = st.session_state.current_question

    st.write("---")
    st.write(f"### {q['question']}")

    correct = False

    # =========================
    # ABC
    # =========================

    if q["type"] == "abc":

        answer = st.radio(
            "Wähle eine Antwort:",
            q["options"]
        )

        if st.button("Antwort prüfen"):

            if answer == q["answer"]:
                correct = True

    # =========================
    # WAHR / FALSCH
    # =========================

    elif q["type"] == "tf":

        answer = st.radio(
            "Wahr oder falsch?",
            ["Wahr", "Falsch"]
        )

        if st.button("Antwort prüfen"):

            bool_answer = answer == "Wahr"

            if bool_answer == q["answer"]:
                correct = True

    # =========================
    # SCHÄTZFRAGE
    # =========================

    elif q["type"] == "estimate":

        answer = st.number_input(
            "Deine Schätzung",
            value=0
        )

        if st.button("Antwort prüfen"):

            correct_value = q["answer"]

            tolerance = correct_value * 0.10

            if abs(answer - correct_value) <= tolerance:
                correct = True

    # =========================
    # AUSWERTUNG
    # =========================

    if st.session_state.get("last_checked", False) is False:

        pass

    if st.button("Nächste Runde"):

        st.session_state.current_question = None

        # Nächster Spieler
        st.session_state.turn += 1

        if st.session_state.turn >= len(st.session_state.players):
            st.session_state.turn = 0

        st.rerun()

    if correct:

        points = levels[st.session_state.level]["points"]

        st.success(f"Richtig! +{points} Punkte")

        st.session_state.scores[st.session_state.turn] += points

        st.session_state.current_question = None

        st.rerun()

    elif st.session_state.get("submitted", False):

        st.error("Leider falsch!")
