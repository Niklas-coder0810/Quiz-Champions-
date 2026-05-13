import streamlit as st
import random
import json

# =========================================================
# PAGE
# =========================================================

st.set_page_config(page_title="Quiz Battle", layout="wide")

# =========================================================
# STATE
# =========================================================

def init():

    defaults = {
        "started": False,
        "players": [],
        "scores": [],
        "turn": 0,
        "q": None,
        "msg": "",
        "used_questions": [],
        "max_points": 10,
        "winner": None
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# 🔥 LOAD QUESTIONS FROM FILE
# =========================================================

@st.cache_data
def load_questions():

    with open("questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    random.shuffle(data)

    return data

if "bank" not in st.session_state:
    st.session_state.bank = load_questions()

# =========================================================
# RANDOM UNUSED QUESTION
# =========================================================

def get_question():

    available = [
        q for i, q in enumerate(st.session_state.bank)
        if i not in st.session_state.used_questions
    ]

    if not available:
        return None

    q = random.choice(available)

    index = st.session_state.bank.index(q)

    st.session_state.used_questions.append(index)

    return q

# =========================================================
# BACKGROUND DESIGN
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
    background: rgba(255,255,255,0.15);
    text-align:center;
    font-weight:bold;
    color:white;
    font-size:22px;
    text-shadow:0 0 10px black;
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
    background: rgba(0,0,0,0.45);
    border-radius:20px;
    margin:20px 0;
    color:white;
    font-weight:bold;
    text-shadow:0 0 10px black;
}

.turn {
    text-align:center;
    font-size:32px;
    font-weight:900;
    color:#00ffd5;
    margin-bottom:20px;
    text-shadow:0 0 10px black;
}

.points {
    text-align:center;
    font-size:24px;
    margin-top:10px;
    color:white;
    font-weight:bold;
    text-shadow:0 0 10px black;
}

button {
    border-radius:15px !important;
    height:60px !important;
    font-weight:bold !important;
    background: linear-gradient(90deg,#00ffd5,#0099ff) !important;
    color:black !important;
    font-size:18px !important;
}

/* =========================================
   RADIO BUTTONS
========================================= */

div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.15);
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 12px;
    border: 2px solid rgba(255,255,255,0.2);
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
    color: white !important;
    text-shadow: 0 0 10px black;
}

div[data-testid="stRadio"] label:hover {
    border: 2px solid #00ffd5;
    box-shadow: 0 0 15px #00ffd5;
    transform: scale(1.02);
    background: rgba(255,255,255,0.22);
}

div[data-testid="stRadio"] div {
    gap: 15px;
}

/* =========================================
   LABELS
========================================= */

label, .stMarkdown, p, span {
    color: white !important;
    text-shadow: 0 0 8px black;
}

/* =========================================
   INPUT FIELDS
========================================= */

.stTextInput input,
.stNumberInput input {
    background: rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    font-size: 20px !important;
    font-weight: bold !important;
}

/* =========================================
   SELECTBOX / SLIDER
========================================= */

.stSelectbox div,
.stSlider {
    color: white !important;
    text-shadow: 0 0 8px black;
}

/* =========================================
   SIDEBAR FIX
========================================= */

section[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# BACKGROUND DESIGN
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
    background: rgba(255,255,255,0.15);
    text-align:center;
    font-weight:bold;
    color:white;
    font-size:22px;
    text-shadow:0 0 10px black;
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
    background: rgba(0,0,0,0.45);
    border-radius:20px;
    margin:20px 0;
    color:white;
    font-weight:bold;
    text-shadow:0 0 10px black;
}

.turn {
    text-align:center;
    font-size:32px;
    font-weight:900;
    color:#00ffd5;
    margin-bottom:20px;
    text-shadow:0 0 10px black;
}

.points {
    text-align:center;
    font-size:24px;
    margin-top:10px;
    color:white;
    font-weight:bold;
    text-shadow:0 0 10px black;
}

button {
    border-radius:15px !important;
    height:60px !important;
    font-weight:bold !important;
    background: linear-gradient(90deg,#00ffd5,#0099ff) !important;
    color:black !important;
    font-size:18px !important;
}

# =========================================================
# START
# =========================================================

if not st.session_state.started:

    st.markdown(
        '<div class="title">🧠 QUIZ BATTLE</div>',
        unsafe_allow_html=True
    )

    count = st.selectbox(
        "Spieler",
        [1,2,3,4]
    )

    # =========================================
    # MAX POINTS
    # =========================================

    max_points = st.slider(
        "🏆 Bis wie viele Punkte?",
        1,
        50,
        10
    )

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
        st.session_state.max_points = max_points

        st.rerun()

# =========================================================
# GAME
# =========================================================

else:

    player = st.session_state.players[
        st.session_state.turn
    ]

    # =========================================
    # HOME BUTTON
    # =========================================

    top1, top2 = st.columns([8,2])

    with top2:

        if st.button("🏠 Home"):

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()

    st.markdown(
        '<div class="title">🎯 QUIZ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='turn'>👉 Jetzt dran: {player}</div>",
        unsafe_allow_html=True
    )

    # =========================================
    # TARGET SCORE
    # =========================================

    st.markdown(
        f"""
        <h3 style='text-align:center;color:white'>
        🏆 Ziel: {st.session_state.max_points} Punkte
        </h3>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(
        len(st.session_state.players)
    )

    for i,p in enumerate(
        st.session_state.players
    ):

        style = (
            "player-box active"
            if i == st.session_state.turn
            else "player-box"
        )

        with cols[i]:

            st.markdown(
                f"""
                <div class='{style}'>
                {p}<br>
                {st.session_state.scores[i]} Punkte
                </div>
                """,
                unsafe_allow_html=True
            )

    # =====================================================
    # QUESTION
    # =====================================================

    if st.session_state.q is None:
        st.session_state.q = get_question()

    q = st.session_state.q

    # =========================================
    # NO QUESTIONS LEFT
    # =========================================

    if q is None:

        st.markdown(
            """
            <div class='title'>
            🏁 Keine Fragen mehr!
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🔄 Neues Spiel"):

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()

        st.stop()

    st.markdown(
        f"<div class='question'>{q['q']}</div>",
        unsafe_allow_html=True
    )

    answer = None

    # =========================================
    # MULTIPLE CHOICE
    # =========================================

    if "o" in q:

        answer = st.radio(
            "Antwort auswählen",
            q["o"]
        )

    # =========================================
    # TRUE / FALSE
    # =========================================

    elif isinstance(q["a"], bool):

        answer = st.radio(
            "Antwort auswählen",
            ["Wahr","Falsch"]
        )

    # =========================================
    # NUMBER INPUT
    # =========================================

    else:

        answer = st.number_input(
            "Schätz deine Antwort",
            value=0.0
        )

    # =====================================================
    # CHECK
    # =====================================================

    if st.button("✅ Antwort bestätigen"):

        correct = False

        # =====================================
        # MULTIPLE CHOICE
        # =====================================

        if "o" in q:

            correct = answer == q["a"]

        # =====================================
        # TRUE / FALSE
        # =====================================

        elif isinstance(q["a"], bool):

            correct = (
                (answer == "Wahr") == q["a"]
            )

        # =====================================
        # NUMBER QUESTION
        # +- 10%
        # =====================================

        else:

            tolerance = q["a"] * 0.1

            correct = (
                abs(answer - q["a"]) <= tolerance
            )

        # =====================================
        # RESULT
        # =====================================

        if correct:

            st.session_state.scores[
                st.session_state.turn
            ] += 1

            st.session_state.msg = "✅ +1 Punkt!"

            # =================================
            # WINNER CHECK
            # =================================

            if (
                st.session_state.scores[
                    st.session_state.turn
                ]
                >= st.session_state.max_points
            ):

                st.session_state.winner = player

        else:

            st.session_state.msg = (
                f"❌ Falsch! Richtige Antwort: {q['a']}"
            )

        # =====================================
        # NEXT PLAYER
        # =====================================

        st.session_state.q = None

        st.session_state.turn = (
            st.session_state.turn + 1
        ) % len(st.session_state.players)

        st.rerun()

    # =====================================================
    # WINNER SCREEN
    # =====================================================

    if st.session_state.winner:

        st.balloons()

        st.markdown(
            f"""
            <div class='title'>
            🏆 {st.session_state.winner} GEWINNT!
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h2 style='text-align:center'>
            Ziel erreicht:
            {st.session_state.max_points} Punkte
            </h2>
            """,
            unsafe_allow_html=True
        )

        if st.button("🔄 Neues Spiel"):

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()

        st.stop()

    # =====================================================
    # FEEDBACK
    # =====================================================

    if st.session_state.msg:

        st.markdown(
            f"""
            <h2 style='text-align:center'>
            {st.session_state.msg}
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class='points'>
            Aktuelle Punkte:
            {st.session_state.scores}
            </div>
            """,
            unsafe_allow_html=True
        )
