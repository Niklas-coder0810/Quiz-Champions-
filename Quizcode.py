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
        "winner": None,
        "skins": [],
        "joker_used": []
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# =========================================================
# CHARACTER SKINS
# =========================================================

CHARACTERS = {
    "🐼 Panda": "🐼",
    "🦊 Fuchs": "🦊",
    "🐸 Frosch": "🐸",
    "🐯 Tiger": "🐯",
    "🦄 Unicorn": "🦄",
    "🤖 Roboter": "🤖"
}

# =========================================================
# LOAD QUESTIONS
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
# CSS
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
}

button {
    border-radius:15px !important;
    height:60px !important;
    font-weight:bold !important;
    background: linear-gradient(90deg,#00ffd5,#0099ff) !important;
    color:black !important;
    font-size:18px !important;
}

/* RADIO */

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

/* INPUT FIX */

.stSelectbox div[data-baseweb="select"] > div {
    color: black !important;
    background: white !important;
    font-weight: bold !important;
}

div[role="option"] {
    color: black !important;
    background: white !important;
}

.stNumberInput input {
    color: black !important;
    background: white !important;
    font-weight: bold !important;
}

.stTextInput input {
    color: black !important;
    background: white !important;
    font-weight: bold !important;
}

label {
    color: white !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# START SCREEN
# =========================================================

if not st.session_state.started:

    st.markdown(
        '<div class="title">🧠 QUIZ BATTLE</div>',
        unsafe_allow_html=True
    )

    count = st.selectbox(
        "Spieleranzahl",
        [1,2,3,4]
    )

    max_points = st.slider(
        "🏆 Bis wie viele Punkte?",
        1,
        50,
        10
    )

    players = []
    skins = []

    for i in range(count):

        name = st.text_input(f"Spieler {i+1}")

        if name == "":
            name = f"Spieler {i+1}"

        skin = st.selectbox(
            f"Charakter Spieler {i+1}",
            list(CHARACTERS.keys()),
            key=f"skin_{i}"
        )

        players.append(name)
        skins.append(CHARACTERS[skin])

    if st.button("🚀 START"):

        st.session_state.started = True
        st.session_state.players = players
        st.session_state.scores = [0]*count
        st.session_state.max_points = max_points
        st.session_state.skins = skins
        st.session_state.joker_used = [False]*count

        st.rerun()

# =========================================================
# GAME
# =========================================================

else:

    player = st.session_state.players[
        st.session_state.turn
    ]

    # =====================================================
    # HOME BUTTON
    # =====================================================

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

    st.markdown(
        f"""
        <h3 style='text-align:center;color:white'>
        🏆 Ziel: {st.session_state.max_points} Punkte
        </h3>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # PLAYER BOXES
    # =====================================================

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
                <div style='font-size:55px'>
                {st.session_state.skins[i]}
                </div>

                {p}<br>

                ⭐ {st.session_state.scores[i]} Punkte
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

    if q is None:

        st.markdown(
            """
            <div class='title'>
            🏁 Keine Fragen mehr!
            </div>
            """,
            unsafe_allow_html=True
        )

        st.stop()

    st.markdown(
        f"<div class='question'>{q['q']}</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # 50/50 JOKER
    # =====================================================

    options = q["o"][:] if "o" in q else None

    current_player = st.session_state.turn

    if (
        "o" in q
        and not st.session_state.joker_used[current_player]
    ):

        if st.button("🃏 50/50 Joker"):

            correct = q["a"]

            wrong = [
                o for o in q["o"]
                if o != correct
            ]

            remove = random.sample(wrong, 2)

            options = [
                o for o in q["o"]
                if o not in remove
            ]

            st.session_state.joker_used[
                current_player
            ] = True

            st.session_state.reduced_options = options

    if "reduced_options" in st.session_state:
        options = st.session_state.reduced_options

    answer = None

    # =====================================================
    # MULTIPLE CHOICE
    # =====================================================

    if "o" in q:

        answer = st.radio(
            "Antwort auswählen",
            options
        )

    # =====================================================
    # TRUE FALSE
    # =====================================================

    elif isinstance(q["a"], bool):

        answer = st.radio(
            "Antwort auswählen",
            ["Wahr","Falsch"]
        )

    # =====================================================
    # NUMBER
    # =====================================================

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

        if "o" in q:

            correct = answer == q["a"]

        elif isinstance(q["a"], bool):

            correct = (
                (answer == "Wahr") == q["a"]
            )

        else:

            tolerance = q["a"] * 0.1

            correct = (
                abs(answer - q["a"]) <= tolerance
            )

        # =================================================
        # RESULT
        # =================================================

        if correct:

            st.session_state.scores[
                st.session_state.turn
            ] += 1

            st.session_state.msg = "✅ +1 Punkt!"

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

        # =================================================
        # NEXT TURN
        # =================================================

        st.session_state.q = None

        if "reduced_options" in st.session_state:
            del st.session_state.reduced_options

        st.session_state.turn = (
            st.session_state.turn + 1
        ) % len(st.session_state.players)

        st.rerun()

    # =====================================================
    # WINNER
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
