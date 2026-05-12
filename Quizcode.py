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
    if "turn" not in st.session_state:
        st.session_state.turn = 0
    if "questions" not in st.session_state:
        st.session_state.questions = {}

init()

# =========================================================
# QUESTION BANK (später 1000+ erweiterbar)
# =========================================================

QUESTION_BANK = [
    {"q":"Hauptstadt von Deutschland?", "o":["Berlin","Paris","Rom"], "a":"Berlin"},
    {"q":"Größter Planet?", "o":["Mars","Jupiter","Venus"], "a":"Jupiter"},
    {"q":"Die Sonne ist ein Stern.", "a":True},
    {"q":"Wie viele Kontinente gibt es?", "o":["5","6","7","8"], "a":"7"},
]

# =========================================================
# START SCREEN
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

    player_index = st.session_state.turn
    player = st.session_state.players[player_index]

    st.title("🎯 QUIZ BATTLE")

    st.markdown(f"## 👉 Jetzt dran: **{player}**")

    # =====================================================
    # FRAGE FÜR DIESEN SPIELER
    # =====================================================

    if player_index not in st.session_state.questions:
        st.session_state.questions[player_index] = random.choice(QUESTION_BANK)

    q = st.session_state.questions[player_index]

    st.write("---")

    st.markdown(f"### ❓ {q['q']}")

    answer = None

    # =====================================================
    # INPUT
    # =====================================================

    if "o" in q:
        answer = st.radio("Antwort", q["o"])
    elif isinstance(q["a"], bool):
        answer = st.radio("Antwort", ["Wahr","Falsch"])
    else:
        answer = st.number_input("Antwort", value=0)

    # =====================================================
    # CHECK BUTTON (WICHTIG: NUR 1 BUTTON)
    # =====================================================

    if st.button("✅ Antwort bestätigen"):

        correct = False

        if "o" in q:
            correct = answer == q["a"]

        elif isinstance(q["a"], bool):
            correct = (answer == "Wahr") == q["a"]

        else:
            correct = abs(answer - q["a"]) <= q["a"] * 0.1

        if correct:
            st.success("✔ Richtig!")
            st.session_state.scores[player_index] += 1
        else:
            st.error("✖ Falsch!")

        # 👉 neue Frage nur für diesen Spieler
        st.session_state.questions[player_index] = random.choice(QUESTION_BANK)

        # 👉 nächster Spieler
        st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)

        st.rerun()

    # =====================================================
    # SCOREBOARD
    # =====================================================

    st.write("---")
    st.subheader("🏆 Punkte")

    for p, s in zip(st.session_state.players, st.session_state.scores):
        st.write(f"{p}: {s}")
