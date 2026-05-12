import streamlit as st
import random

# =========================================================
# SETUP
# =========================================================

st.set_page_config(page_title="Quiz Battle", layout="wide")

# =========================================================
# STATE
# =========================================================

def init():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "players" not in st.session_state:
        st.session_state.players = []
    if "scores" not in st.session_state:
        st.session_state.scores = []
    if "questions" not in st.session_state:
        st.session_state.questions = {}
    if "answered" not in st.session_state:
        st.session_state.answered = {}

init()

# =========================================================
# 1000+ QUESTIONS SYSTEM (STRUKTURIERT)
# =========================================================

QUESTION_BANK = [
    {
        "q": "Welche Stadt ist die Hauptstadt von Deutschland?",
        "o": ["Berlin", "Hamburg", "München", "Köln"],
        "a": "Berlin"
    },
    {
        "q": "Welcher Planet ist der größte in unserem Sonnensystem?",
        "o": ["Mars", "Jupiter", "Saturn", "Venus"],
        "a": "Jupiter"
    },
    {
        "q": "Die Lichtgeschwindigkeit beträgt ungefähr 300.000 km/s.",
        "a": True
    },
    {
        "q": "Wie viele Kontinente gibt es auf der Erde?",
        "o": ["5", "6", "7", "8"],
        "a": "7"
    },
]

# 👉 später erweiterbar auf 1000+:
# einfach weitere Dicts hinzufügen oder JSON laden

# =========================================================
# START
# =========================================================

if not st.session_state.started:

    st.title("🧠 QUIZ BATTLE")

    count = st.selectbox("Spieleranzahl", [1,2,3,4])

    players = []

    for i in range(count):
        name = st.text_input(f"Spieler {i+1}")
        if name == "":
            name = f"Spieler {i+1}"
        players.append(name)

    if st.button("🚀 START"):
        st.session_state.started = True
        st.session_state.players = players
        st.session_state.scores = [0]*count
        st.rerun()

# =========================================================
# GAME
# =========================================================

else:

    st.title("🎯 QUIZ BATTLE")

    cols = st.columns(len(st.session_state.players))

    # =====================================================
    # JEDER SPIELER EIGENE FRAGE
    # =====================================================

    for i, player in enumerate(st.session_state.players):

        # Frage zuweisen falls neu
        if i not in st.session_state.questions:
            st.session_state.questions[i] = random.choice(QUESTION_BANK)

        q = st.session_state.questions[i]

        with cols[i]:

            st.markdown(f"### {player}")
            st.markdown(f"🏆 Punkte: {st.session_state.scores[i]}")

            st.markdown("---")

            st.markdown(f"**❓ {q['q']}**")

            # =================================================
            # INPUT
            # =================================================

            key = f"ans_{i}"

            answer = None

            if "o" in q:
                answer = st.radio("Antwort", q["o"], key=key)

            elif isinstance(q["a"], bool):
                answer = st.radio("Antwort", ["Wahr","Falsch"], key=key)

            else:
                answer = st.number_input("Antwort", value=0, key=key)

            # =================================================
            # CHECK
            # =================================================

            if st.button(f"Antwort prüfen {player}", key=f"btn_{i}"):

                correct = False

                if "o" in q:
                    correct = answer == q["a"]

                elif isinstance(q["a"], bool):
                    correct = (answer == "Wahr") == q["a"]

                else:
                    correct = abs(answer - q["a"]) <= q["a"] * 0.1

                if correct:
                    st.success("✔ Richtig!")
                    st.session_state.scores[i] += 1
                else:
                    st.error("✖ Falsch!")

                # neue Frage für diesen Spieler
                st.session_state.questions[i] = random.choice(QUESTION_BANK)

                st.rerun()
