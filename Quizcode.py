import streamlit as st
import random

# =========================================================
# PAGE
# =========================================================

st.set_page_config(page_title="Quiz Battle", layout="wide")

# =========================================================
# STATE
# =========================================================

def reset_game():
    st.session_state.started = False
    st.session_state.players = []
    st.session_state.scores = []
    st.session_state.turn = 0
    st.session_state.phase = "question"
    st.session_state.q = None
    st.session_state.msg = ""

def init():
    if "started" not in st.session_state:
        reset_game()

init()

# =========================================================
# DESIGN (CLEANER + MODERN)
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
    radial-gradient(circle at top, #1a1a2e, #0f0f1a);
    color: white;
    font-family: Arial;
}

/* TOP TITLE */
.title {
    text-align:center;
    font-size:60px;
    font-weight:900;
    margin-bottom:10px;
    background: linear-gradient(90deg,#00ffd5,#4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* CARD STYLE */
.card {
    background: rgba(255,255,255,0.08);
    padding:25px;
    border-radius:20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0,255,213,0.15);
    margin:10px 0;
}

/* ACTIVE PLAYER */
.active {
    border:2px solid #00ffd5;
    box-shadow:0 0 15px #00ffd5;
    transform: scale(1.03);
}

/* QUESTION */
.question {
    font-size:30px;
    text-align:center;
    padding:25px;
    border-radius:20px;
    background: rgba(0,0,0,0.35);
    margin:20px 0;
}

/* TURN TEXT */
.turn {
    text-align:center;
    font-size:26px;
    font-weight:800;
    color:#00ffd5;
}

/* BUTTONS */
button {
    border-radius:12px !important;
    height:55px !important;
    font-weight:bold !important;
    background: linear-gradient(90deg,#00ffd5,#4facfe) !important;
    color:black !important;
}

/* HOME BUTTON */
.home-btn button {
    background: #ff4d4d !important;
    color:white !important;
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
# RESET BUTTON (HOME)
# =========================================================

st.sidebar.markdown("## 🏠 Menü")

if st.sidebar.button("🔴 Home / Spiel beenden"):
    reset_game()
    st.rerun()

# =========================================================
# START SCREEN
# =========================================================

if not st.session_state.started:

    st.markdown('<div class="title">🧠 QUIZ BATTLE</div>', unsafe_allow_html=True)

    count = st.selectbox("Spieleranzahl", [1,2,3,4])

    players = []

    for i in range(count):
        name = st.text_input(f"Spieler {i+1}")
        if name == "":
            name = f"Spieler {i+1}"
        players.append(name)

    if st.button("🚀 START GAME"):
        st.session_state.started = True
        st.session_state.players = players
        st.session_state.scores = [0]*count
        st.rerun()

# =========================================================
# GAME
# =========================================================

else:

    player = st.session_state.players[st.session_state.turn]

    st.markdown('<div class="title">🎯 QUIZ BATTLE</div>', unsafe_allow_html=True)

    st.markdown(f"<div class='turn'>👉 Jetzt dran: {player}</div>", unsafe_allow_html=True)

    # =====================================================
    # SCOREBOARD
    # =====================================================

    cols = st.columns(len(st.session_state.players))

    for i,p in enumerate(st.session_state.players):

        style = "card active" if i == st.session_state.turn else "card"

        with cols[i]:
            st.markdown(
                f"<div class='{style}'><h3>{p}</h3><h2>{st.session_state.scores[i]} ⭐</h2></div>",
                unsafe_allow_html=True
            )

    # =====================================================
    # QUESTION
    # =====================================================

    if st.session_state.q is None:
        st.session_state.q = random.choice(questions)

    q = st.session_state.q

    st.markdown(f"<div class='question'>{q['q']}</div>", unsafe_allow_html=True)

    answer = None

    if "o" in q:
        answer = st.radio("Antwort", q["o"])
    elif isinstance(q["a"], bool):
        answer = st.radio("Antwort", ["Wahr","Falsch"])
    else:
        answer = st.number_input("Antwort", value=0)

    # =====================================================
    # CHECK ANSWER
    # =====================================================

    if st.button("✅ Bestätigen"):

        correct = False

        if "o" in q:
            correct = answer == q["a"]

        elif isinstance(q["a"], bool):
            correct = (answer == "Wahr") == q["a"]

        else:
            correct = abs(answer - q["a"]) <= q["a"] * 0.1

        if correct:
            st.session_state.scores[st.session_state.turn] += 1
            st.session_state.msg = "✅ +1 Punkt!"
        else:
            st.session_state.msg = "❌ Falsch!"

        st.session_state.q = None
        st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)

        st.rerun()

    # =====================================================
    # FEEDBACK
    # =====================================================

    if st.session_state.msg:
        st.markdown(f"<h2 style='text-align:center'>{st.session_state.msg}</h2>", unsafe_allow_html=True)
