import streamlit as st
import random

# =========================================================
# SETUP
# =========================================================

st.set_page_config(page_title="Quiz Battle", layout="wide")

# =========================================================
# SESSION STATE
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
    if "q" not in st.session_state:
        st.session_state.q = None
    if "used_joker" not in st.session_state:
        st.session_state.used_joker = {}

init()

# =========================================================
# FRAGEN
# =========================================================

questions = [
    {"type":"abc","q":"Hauptstadt Deutschland?","o":["Berlin","Paris","Rom"],"a":"Berlin"},
    {"type":"tf","q":"Die Sonne ist ein Stern","a":True},
    {"type":"est","q":"Wie viele Knochen hat der Mensch?", "a":206},
]

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

    player = st.session_state.players[st.session_state.turn]

    st.title(f"🎯 {player} ist dran")

    # neue Frage
    if st.session_state.q is None:
        st.session_state.q = random.choice(questions)

    q = st.session_state.q

    st.write("---")

    # =====================================================
    # JOKER SYSTEM
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🎲 50/50 Joker"):

            if "50" not in st.session_state.used_joker.get(player, {}):

                if q["type"] == "abc":

                    wrong = [o for o in q["o"] if o != q["a"]]

                    q["o"] = [q["a"], random.choice(wrong)]

                st.session_state.used_joker.setdefault(player, {})["50"] = True

    with col2:

        if st.button("⏭ Skip Joker"):

            st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)
            st.session_state.q = None
            st.rerun()

    with col3:

        if st.button("⭐ +1 Punkt Joker"):

            if "bonus" not in st.session_state.used_joker.get(player, {}):

                st.session_state.used_joker.setdefault(player, {})["bonus"] = True

                st.session_state.scores[st.session_state.turn] += 1

    # =====================================================
    # FRAGE
    # =====================================================

    answer = None

    if q["type"] == "abc":

        answer = st.radio(q["q"], q["o"])

    elif q["type"] == "tf":

        answer = st.radio(q["q"], ["Wahr","Falsch"])

    else:

        answer = st.number_input(q["q"], value=0)

    # =====================================================
    # CHECK BUTTON (WICHTIG FIX)
    # =====================================================

    if st.button("✅ Antwort bestätigen"):

        correct = False

        if q["type"] == "abc":
            correct = answer == q["a"]

        elif q["type"] == "tf":
            correct = (answer == "Wahr") == q["a"]

        else:
            correct = abs(answer - q["a"]) <= q["a"] * 0.1

        if correct:
            st.success("Richtig!")
            st.session_state.scores[st.session_state.turn] += 1
        else:
            st.error("Falsch!")

        st.session_state.q = None
        st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)

        st.rerun()

    # =====================================================
    # SCOREBOARD
    # =====================================================

    st.write("---")
    st.subheader("🏆 Punkte")

    for p,s in zip(st.session_state.players, st.session_state.scores):
        st.write(f"{p}: {s}")
