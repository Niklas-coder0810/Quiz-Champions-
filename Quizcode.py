import streamlit as st
import random
import json

# =========================================================
# PAGE
# =========================================================

st.set_page_config(page_title="Quiz Battle", layout="wide")

# =========================================================
# SESSION STATE
# =========================================================

def init():
    defaults = {
        "started": False,
        "players": [],
        "scores": [],
        "turn": 0,
        "q": None,
        "msg": "",
        "used_questions": []
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

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
# GET RANDOM UNUSED QUESTION
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
# DESIGN
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
# START SCREEN
# =========================================================

if not st.session_state.started:

    st.markdown(
        '<div class="title">🧠 QUIZ BATTLE</div>',
        unsafe_allow_html=True
    )

    count = st.selectbox("Spieleranzahl", [1,2,3,4])

    players = []

    for i in range(count):

        name = st.text_input(f"Spieler {i+1}")

        if not name:
            name = f"Spieler {i+1}"

        players.append(name)

    if st.button("🚀 START"):

        st.session_state.started = True
        st.session_state.players = players
        st.session_state.scores = [0] * count

        st.rerun()

# =========================================================
# GAME
# =========================================================

else:

    # =========================================
    # NEW QUESTION
    # =========================================

    if st.session_state.q is None:
        st.session_state.q = get_question()

    # =========================================
    # END GAME
    # =========================================

    if st.session_state.q is None:

        st.title("🏁 Keine Fragen mehr!")

        winner_index = st.session_state.scores.index(
            max(st.session_state.scores)
        )

        winner = st.session_state.players[winner_index]

        st.success(f"🎉 Gewinner: {winner}")

        st.write("Punkte:")

        for i, p in enumerate(st.session_state.players):
            st.write(f"{p}: {st.session_state.scores[i]}")

        st.stop()

    q = st.session_state.q

    # =========================================
    # PLAYER INFO
    # =========================================

    player = st.session_state.players[st.session_state.turn]

    st.markdown(
        '<div class="title">🎯 QUIZ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='turn'>👉 Jetzt dran: {player}</div>",
        unsafe_allow_html=True
    )

    cols = st.columns(len(st.session_state.players))

    for i, p in enumerate(st.session_state.players):

        style = (
            "player-box active"
            if i == st.session_state.turn
            else "player-box"
        )

        with cols[i]:
            st.markdown(
                f"<div class='{style}'>{p}<br>{st.session_state.scores[i]} Punkte</div>",
                unsafe_allow_html=True
            )

    # =========================================
    # QUESTION
    # =========================================

    st.markdown(
        f"<div class='question'>{q['q']}</div>",
        unsafe_allow_html=True
    )

    answer = None

    # Multiple Choice
    if "o" in q:

        answer = st.radio(
            "Antwort",
            q["o"]
        )

    # True / False
    elif isinstance(q["a"], bool):

        answer = st.radio(
            "Antwort",
            ["Wahr", "Falsch"]
        )

    # Number
    else:

        answer = st.number_input(
            "Antwort",
            value=0.0
        )

    # =========================================
    # CHECK ANSWER
    # =========================================

    if st.button("✅ Antwort bestätigen"):

        correct = False

        if "o" in q:

            correct = answer == q["a"]

        elif isinstance(q["a"], bool):

            correct = (
                (answer == "Wahr") == q["a"]
            )

        else:

            correct = abs(answer - q["a"]) <= 0.1

        # =====================================
        # POINTS
        # =====================================

        if correct:

            st.session_state.scores[
                st.session_state.turn
            ] += 1

            st.session_state.msg = "✅ Richtig!"

        else:

            st.session_state.msg = (
                f"❌ Falsch! Richtige Antwort: {q['a']}"
            )

        # =====================================
        # NEXT TURN
        # =====================================

        st.session_state.turn = (
            st.session_state.turn + 1
        ) % len(st.session_state.players)

        st.session_state.q = None

        st.rerun()

    # =========================================
    # MESSAGE
    # =========================================

    if st.session_state.msg:

        st.markdown(
            f"""
            <h2 style='text-align:center'>
            {st.session_state.msg}
            </h2>
            """,
            unsafe_allow_html=True
        )
