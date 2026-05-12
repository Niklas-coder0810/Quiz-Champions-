import streamlit as st
import random

# =========================================================
# PAGE
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
    if "phase" not in st.session_state:
        st.session_state.phase = "question"
    if "q" not in st.session_state:
        st.session_state.q = None
    if "msg" not in st.session_state:
        st.session_state.msg = ""

init()

# =========================================================
# 1000+ QUESTIONS (AUTO GENERATION)
# =========================================================

def generate_questions():
    base = [
        ("Hauptstadt von Deutschland?", "Berlin"),
        ("Größter Planet?", "Jupiter"),
        ("Wie viele Kontinente gibt es?", "7"),
        ("Wasser gefriert bei wie viel Grad Celsius?", "0"),
        ("Wie viele Tage hat ein Jahr (normal)?", "365"),
        ("Welche Farbe hat die Sonne aus dem All gesehen?", "Weiß"),
        ("Wie viele Bundesländer hat Deutschland?", "16"),
        ("Welches Tier ist das schnellste Landtier?", "Gepard"),
        ("Wie viele Minuten hat eine Stunde?", "60"),
        ("Welcher Ozean ist der größte?", "Pazifik"),
    ]

    qs = []

    # 100 Wiederholungen = 1000 Fragen (leicht variiert möglich)
    for i in range(100):

        for q,a in base:

            qs.append({
                "q": q,
                "a": a
            })

    random.shuffle(qs)
    return qs

if "bank" not in st.session_state:
    st.session_state.bank = generate_questions()

# =========================================================
# START SCREEN
# =========================================================

if not st.session_state.started:

    st.title("🧠 QUIZ BATTLE")

    count = st.selectbox("Spieler", [1,2,3,4])

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

    # =====================================================
    # NEUE FRAGE (nur wenn nötig)
    # =====================================================

    if st.session_state.q is None:
        st.session_state.q = random.choice(st.session_state.bank)

    q = st.session_state.q

    # =====================================================
    # PHASE 1: FRAGE
    # =====================================================

    if st.session_state.phase == "question":

        st.title("🎯 QUIZ")

        st.markdown(f"## 👉 Jetzt dran: {player}")
        st.markdown(f"### ❓ {q['q']}")

        answer = st.text_input("Antwort eingeben")

        if st.button("Antwort bestätigen"):

            correct = answer.lower() == str(q["a"]).lower()

            if correct:
                st.session_state.scores[st.session_state.turn] += 1
                st.session_state.msg = "✅ +1 Punkt!"
            else:
                st.session_state.msg = f"❌ Falsch! Richtige Antwort: {q['a']}"

            st.session_state.phase = "result"
            st.rerun()

    # =====================================================
    # PHASE 2: RESULT FOLIE
    # =====================================================

    elif st.session_state.phase == "result":

        st.title("📢 Ergebnis")

        st.markdown(f"## {st.session_state.msg}")

        st.markdown(f"### Nächster Spieler: {st.session_state.players[(st.session_state.turn + 1) % len(st.session_state.players)]}")

        st.markdown("---")

        if st.button("➡️ Weiter"):

            st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)
            st.session_state.q = None
            st.session_state.phase = "question"

            st.rerun()

    # =====================================================
    # SCOREBOARD (IMMER SICHTBAR)
    # =====================================================

    st.write("---")
    st.subheader("🏆 Punkte")

    for p,s in zip(st.session_state.players, st.session_state.scores):
        st.write(f"{p}: {s}")
