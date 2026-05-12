import streamlit as st
random
import time

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

    # 🔥 NEU: Fragen pro Spieler
    if "qs" not in st.session_state:
        st.session_state.qs = {}

init()

# =========================================================
# BACKGROUND DESIGN (UNCHANGED)
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
    linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)),
    url("https://images.unsplash.com/photo-1506744038136-46273834b3fb");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;

    color: white;
}

.title {
    text-align:center;
    font-size:70px;
    font-weight:900;
    text-shadow:0 0 25px #00ffd5;
}

.player-box {
    padding:15px;
    border-radius:15px;
    background: rgba(255,255,255,0.1);
    text-align:center;
    font-weight:bold;
}

.active {
    border:2px solid #00ffd5;
    box-shadow:0 0 20px #00ffd5;
    transform: scale(1.05);
}

.question {
    font-size:34px;
    text-align:center;
    padding:30px;
    background: rgba(0,0,0,0.4);
    border-radius:20px;
    margin:20px 0;
}

.turn {
    text-align:center;
    font-size:32px;
    font-weight:900;
    color:#00ffd5;
    margin-bottom:20px;
}

.points {
    text-align:center;
    font-size:24px;
    margin-top:10px;
    color:#aaa;
}

button {
    border-radius:15px !important;
    height:60px !important;
    font-weight:bold !important;
    background: linear-gradient(90deg,#00ffd5,#0099ff) !important;
    color:black !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# QUESTIONS
# =========================================================

questions = [
    {"q":"Hauptstadt Deutschland?", "o":["Berlin","Paris","Rom"], "a":"Berlin"},
    {"q":"Die Sonne ist ein Stern", "a":True},
    {"q":"Wie viele Knochen hat Mensch?", "a":206}
]

# =========================================================
# START
# =========================================================

if not st.session_state.started:

    st.markdown('<div class="title">🧠 QUIZ BATTLE</div>', unsafe_allow_html=True)

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

    player_index = st.session_state.turn
    player = st.session_state.players[player_index]

    st.markdown('<div class="title">🎯 QUIZ</div>', unsafe_allow_html=True)

    st.markdown(
        f"<div class='turn'>👉 Jetzt dran: {player}</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # PLAYERS
    # =====================================================

    cols = st.columns(len(st.session_state.players))

    for i,p in enumerate(st.session_state.players):

        style = "player-box active" if i == st.session_state.turn else "player-box"

        with cols[i]:
            st.markdown(
                f"<div class='{style}'>{p}<br>{st.session_state.scores[i]} Punkte</div>",
                unsafe_allow_html=True
            )

    # =====================================================
    # 🔥 NEU: JE SPIELER EIGENE FRAGE
    # =====================================================

    if player_index not in st.session_state.qs:
        st.session_state.qs[player_index] = random.choice(questions)

    q = st.session_state.qs[player_index]

    st.markdown(f"<div class='question'>{q['q']}</div>", unsafe_allow_html=True)

    answer = None

    if "o" in q:
        answer = st.radio("Antwort", q["o"])
    elif isinstance(q["a"], bool):
        answer = st.radio("Antwort", ["Wahr","Falsch"])
    else:
        answer = st.number_input("Antwort", value=0)

    # =====================================================
    # CHECK ANSWER (UNVERÄNDERT LOGIK)
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
            st.session_state.scores[player_index] += 1
            st.session_state.msg = "✅ +1 Punkt!"
        else:
            st.session_state.msg = "❌ Falsch!"

        # 🔥 NEU: neue Frage NUR für diesen Spieler
        st.session_state.qs[player_index] = random.choice(questions)

        st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)

        st.rerun()

    # =====================================================
    # FEEDBACK (UNVERÄNDERT)
    # =====================================================

    if st.session_state.get("msg","") != "":

        st.markdown(
            f"<h2 style='text-align:center'>{st.session_state.msg}</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='points'>Aktuelle Punkte: {st.session_state.scores}</div>",
            unsafe_allow_html=True
        )
