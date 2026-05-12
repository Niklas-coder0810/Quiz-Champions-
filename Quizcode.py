import streamlit as st
import random

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Ultimatives Quiz",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# SESSION STATE FIX
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "players" not in st.session_state:
    st.session_state.players = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "question" not in st.session_state:
    st.session_state.question = None

if "level" not in st.session_state:
    st.session_state.level = "Anfänger"

# =========================================================
# BACKGROUND (FLÜSSIG ANIMIERT, OHNE BUGS)
# =========================================================

background = "https://images.unsplash.com/photo-1506744038136-46273834b3fb"

st.markdown(f"""
<style>

.stApp {{
    background:
    linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.75)),
    url("{background}");

    background-size: cover;
    background-position: center;

    animation: zoom 30s infinite ease-in-out;
    color: white;
}}

@keyframes zoom {{
    0% {{background-size: 100%;}}
    50% {{background-size: 110%;}}
    100% {{background-size: 100%;}}
}}

.title {{
    text-align:center;
    font-size:70px;
    font-weight:900;
    text-shadow:0 0 20px #00ffd5;
}}

.subtitle {{
    text-align:center;
    font-size:22px;
    color:#ccc;
    margin-bottom:30px;
}}

.card {{
    background: rgba(255,255,255,0.10);
    padding: 25px;
    border-radius: 25px;
    backdrop-filter: blur(15px);
}}

.player {{
    padding:15px;
    border-radius:15px;
    background: rgba(255,255,255,0.1);
    text-align:center;
}}

.active {{
    border: 2px solid #00ffd5;
    box-shadow: 0 0 15px #00ffd5;
}}

.question {{
    font-size:32px;
    text-align:center;
    margin:20px;
    padding:30px;
    border-radius:20px;
    background: rgba(0,0,0,0.4);
}}

button {{
    background: linear-gradient(90deg,#00ffd5,#0099ff);
    color:black !important;
    font-weight:bold;
    border-radius:15px !important;
    height:60px;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FRAGEN
# =========================================================

abc_questions = [
    {"q": "Hauptstadt von Deutschland?", "o": ["Berlin","Hamburg","München"], "a":"Berlin"},
    {"q": "Größter Planet?", "o": ["Mars","Jupiter","Venus"], "a":"Jupiter"},
]

tf_questions = [
    {"q": "Die Sonne ist ein Stern.", "a": True},
    {"q": "Wasser kocht bei 50°C.", "a": False},
]

est_questions = [
    {"q": "Wie viele Knochen hat der Mensch?", "a":206},
    {"q": "Wie hoch ist der Mount Everest?", "a":8849},
]

# =========================================================
# STARTMENÜ
# =========================================================

if not st.session_state.started:

    st.markdown('<div class="title">🧠 QUIZ GAME</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Multiplayer Allgemeinwissen</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        players_count = st.selectbox("Spieleranzahl", [1,2,3,4])
        players = []

        for i in range(players_count):
            name = st.text_input(f"Spieler {i+1}", key=i)
            if name == "":
                name = f"Spieler {i+1}"
            players.append(name)

        level = st.selectbox("Level", ["Anfänger","Amateur","Profi","Quiz Master"])
        points_goal = st.number_input("Punkte zum Gewinnen", 5, 100, 10)

        if st.button("🚀 SPIEL STARTEN"):
            st.session_state.started = True
            st.session_state.players = players
            st.session_state.scores = [0]*players_count
            st.session_state.level = level
            st.session_state.goal = points_goal
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SPIEL
# =========================================================

else:

    player = st.session_state.players[st.session_state.turn]

    st.markdown('<div class="title">🎯 QUIZ</div>', unsafe_allow_html=True)

    cols = st.columns(len(st.session_state.players))

    for i,p in enumerate(st.session_state.players):

        style = "player active" if i == st.session_state.turn else "player"

        with cols[i]:
            st.markdown(
                f"<div class='{style}'>{p}<br>{st.session_state.scores[i]} Punkte</div>",
                unsafe_allow_html=True
            )

    st.markdown(f"<div class='question'>🎮 {player} ist dran</div>", unsafe_allow_html=True)

    # neue Frage
    if st.session_state.question is None:

        t = random.choice(["abc","tf","est"])

        if t == "abc":
            st.session_state.question = random.choice(abc_questions)

        elif t == "tf":
            st.session_state.question = random.choice(tf_questions)

        else:
            st.session_state.question = random.choice(est_questions)

    q = st.session_state.question

    # =====================================================
    # ABC
    # =====================================================

    if "o" in q:

        ans = st.radio(q["q"], q["o"])

        if st.button("Antwort prüfen"):
            if ans == q["a"]:
                st.success("Richtig!")
                st.session_state.scores[st.session_state.turn] += 1
            else:
                st.error("Falsch!")

            st.session_state.question = None
            st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)
            st.rerun()

    # =====================================================
    # TRUE/FALSE
    # =====================================================

    elif isinstance(q["a"], bool):

        ans = st.radio(q["q"], ["Wahr","Falsch"])

        if st.button("Antwort prüfen"):
            if (ans == "Wahr") == q["a"]:
                st.success("Richtig!")
                st.session_state.scores[st.session_state.turn] += 1
            else:
                st.error("Falsch!")

            st.session_state.question = None
            st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)
            st.rerun()

    # =====================================================
    # SCHÄTZFRAGE
    # =====================================================

    else:

        ans = st.number_input(q["q"], value=0)

        if st.button("Antwort prüfen"):

            if abs(ans - q["a"]) <= q["a"] * 0.1:
                st.success("Richtig!")
                st.session_state.scores[st.session_state.turn] += 1
            else:
                st.error(f"Falsch! Antwort war {q['a']}")

            st.session_state.question = None
            st.session_state.turn = (st.session_state.turn + 1) % len(st.session_state.players)
            st.rerun()

    # =====================================================
    # GEWINNER
    # =====================================================

    for i,s in enumerate(st.session_state.scores):
        if s >= st.session_state.goal:
            st.balloons()
            st.success(f"🏆 {st.session_state.players[i]} gewinnt!")
            st.stop()
