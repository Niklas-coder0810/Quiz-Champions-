import streamlit as st
import random
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
    if "q" not in st.session_state:
        st.session_state.q = None
    if "msg" not in st.session_state:
        st.session_state.msg = ""

init()

# =========================================================
# BACKGROUND DESIGN (UNVERÄNDERT)
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

.card {
    background: rgba(255,255,255,0.12);
    padding:25px;
    border-radius:25px;
    backdrop-filter: blur(15px);
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
# 🔥 1000 ECHTE FRAGEN SYSTEM
# =========================================================

BASE = [
    {"q":"Hauptstadt von Deutschland?", "o":["Berlin","Paris","Rom","Madrid"], "a":"Berlin"},
    {"q":"Hauptstadt von Frankreich?", "o":["Paris","Berlin","Rom","London"], "a":"Paris"},
    {"q":"Hauptstadt von Italien?", "o":["Rom","Mailand","Neapel","Turin"], "a":"Rom"},
    {"q":"Wie viele Kontinente gibt es?", "o":["5","6","7","8"], "a":"7"},
    {"q":"Wasser gefriert bei 0°C.", "a":True},
    {"q":"Wie viele Tage hat ein Jahr?", "o":["365","360","400","300"], "a":"365"},
    {"q":"Wie viele Bundesländer hat Deutschland?", "o":["16","14","18","12"], "a":"16"},
    {"q":"Welcher Planet ist der größte?", "o":["Mars","Jupiter","Venus","Saturn"], "a":"Jupiter"},
    {"q":"Wie viele Minuten hat eine Stunde?", "o":["60","100","30","90"], "a":"60"},
    {"q":"Welcher Ozean ist der größte?", "o":["Pazifik","Atlantik","Indisch","Arktis"], "a":"Pazifik"},
]

def generate_1000():
    bank = []
    for i in range(100):
        for q in BASE:
            bank.append(q.copy())
    random.shuffle(bank)
    return bank

# einmalig erzeugen
if "bank" not in st.session_state:
    st.session_state.bank = generate_1000()

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

    player = st.session_state.players[st.session_state.turn]

    st.markdown('<div class="title">🎯 QUIZ</div>', unsafe_allow_html=True)

    st.markdown(
        f"<div class='turn'>👉 Jetzt dran: {player}</div>",
        unsafe_allow_html=True
    )

    cols = st.columns(len(st.session_state.players))

    for i,p in enumerate(st.session_state.players):

        style = "player-box active" if i == st.session_state.turn else "player-box"

        with cols[i]:
            st.markdown(
                f"<div class='{style}'>{p}<br>{st.session_state.scores[i]} Punkte</div>",
                unsafe_allow_html=True
            )

    # =====================================================
    # FRAGE (WICHTIG: KEINE DUPLIKATE IM FLOW)
    # =====================================================

    if st.session_state.q is None:
        st.session_state.q = random.choice(st.session_state.bank)

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
    # CHECK
    # =====================================================

    if st.button("✅ Antwort bestätigen"):

        correct = False

        if "o" in q:
            correct = answer == q["a"]

        elif isinstance(q["a"], bool):
            correct = (answer == "Wahr") == q["a"]

        else:
            correct = abs(answer - q["a"]) <= 0.1

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
        st.markdown(f"<div class='points'>Aktuelle Punkte: {st.session_state.scores}</div>", unsafe_allow_html=True)
