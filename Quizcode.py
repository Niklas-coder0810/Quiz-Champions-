# =========================================================
# ULTIMATIVES ALLGEMEINWISSENS QUIZ
# MODERNES DESIGN + MULTIPLAYER + ANIMATIONEN
# =========================================================

import streamlit as st
import random
from streamlit_autorefresh import st_autorefresh

# =========================================================
# SEITEN EINSTELLUNGEN
# =========================================================

st.set_page_config(
    page_title="Ultimatives Quiz",
    page_icon="🧠",
    layout="wide"
)

# Hintergrund alle 20 Sekunden neu laden
st_autorefresh(interval=20000, key="backgroundrefresh")

# =========================================================
# HINTERGRUND BILDER
# =========================================================

backgrounds = [
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    "https://images.unsplash.com/photo-1470770841072-f978cf4d019e",
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "https://images.unsplash.com/photo-1493246507139-91e8fad9978e",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba",
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
    "https://images.unsplash.com/photo-1426604966848-d7adac402bff",
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
    "https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07",
    "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
    "https://images.unsplash.com/photo-1494526585095-c41746248156",
    "https://images.unsplash.com/photo-1500048993953-d23a436266cf",
    "https://images.unsplash.com/photo-1439066615861-d1af74d74000",
]

bg = random.choice(backgrounds)

# =========================================================
# DESIGN
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background:
        linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.70)),
        url("{bg}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;

        animation: fadeIn 2s ease-in;
    }}

    @keyframes fadeIn {{
        from {{opacity: 0;}}
        to {{opacity: 1;}}
    }}

    .title {{
        text-align: center;
        font-size: 65px;
        font-weight: 900;
        color: white;
        margin-bottom: 10px;
        text-shadow: 0px 0px 25px rgba(0,255,213,0.9);
    }}

    .subtitle {{
        text-align: center;
        font-size: 24px;
        color: #d6d6d6;
        margin-bottom: 40px;
    }}

    .glass {{
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(18px);
        border-radius: 25px;
        padding: 30px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }}

    .player-card {{
        background: rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        transition: 0.3s;
    }}

    .active-player {{
        border: 3px solid #00ffd5;
        background: rgba(0,255,213,0.18);
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0,255,213,0.8);
    }}

    .question-box {{
        background: rgba(0,0,0,0.45);
        border-radius: 30px;
        padding: 40px;
        margin-top: 30px;
        margin-bottom: 30px;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        animation: slideUp 0.6s ease;
    }}

    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(50px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0px);
        }}
    }}

    .turn-box {{
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        color: #00ffd5;
        margin-top: 10px;
        margin-bottom: 30px;
        animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
        0% {{transform: scale(1);}}
        50% {{transform: scale(1.04);}}
        100% {{transform: scale(1);}}
    }}

    div.stButton > button {{
        width: 100%;
        border-radius: 18px;
        height: 65px;
        font-size: 22px;
        font-weight: bold;
        background: linear-gradient(90deg,#00ffd5,#0099ff);
        color: black;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0,255,213,0.4);
    }}

    div.stButton > button:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 30px rgba(0,255,213,0.9);
    }}

    div.stRadio > label {{
        font-size: 22px !important;
        color: white !important;
    }}

    .stNumberInput label {{
        color: white !important;
        font-size: 20px !important;
    }}

    .stTextInput label {{
        color: white !important;
        font-size: 20px !important;
    }}

    .stSelectbox label {{
        color: white !important;
        font-size: 20px !important;
    }}

    h1,h2,h3,h4 {{
        color: white !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FRAGENBANK
# =========================================================

questions = []

abc_questions = [
    {
        "question": "Was ist die Hauptstadt von Deutschland?",
        "options": ["Berlin", "Hamburg", "München"],
        "answer": "Berlin"
    },
    {
        "question": "Welcher Planet ist der größte?",
        "options": ["Mars", "Jupiter", "Venus"],
        "answer": "Jupiter"
    },
    {
        "question": "Wie viele Kontinente gibt es?",
        "options": ["5", "6", "7"],
        "answer": "7"
    },
]

true_false_questions = [
    {
        "question": "Die Sonne ist ein Planet.",
        "answer": False
    },
    {
        "question": "Wasser gefriert bei 0 Grad Celsius.",
        "answer": True
    },
    {
        "question": "Ein Jahr hat 500 Tage.",
        "answer": False
    },
]

estimate_questions = [
    {
        "question": "Wie hoch ist der Mount Everest in Metern?",
        "answer": 8849
    },
    {
        "question": "Wie viele Knochen hat ein Mensch?",
        "answer": 206
    },
    {
        "question": "Wie viele Länder gibt es auf der Erde?",
        "answer": 195
    },
]

while len(questions) < 1000:

    qtype = random.choice(["abc", "tf", "estimate"])

    if qtype == "abc":
        q = random.choice(abc_questions).copy()
        q["type"] = "abc"

    elif qtype == "tf":
        q = random.choice(true_false_questions).copy()
        q["type"] = "tf"

    else:
        q = random.choice(estimate_questions).copy()
        q["type"] = "estimate"

    questions.append(q)

# =========================================================
# LEVEL
# =========================================================

levels = {
    "Anfänger": {"range": (0, 250), "points": 1},
    "Amateur": {"range": (250, 500), "points": 2},
    "Profi": {"range": (500, 750), "points": 3},
    "Quiz Master": {"range": (750, 1000), "points": 4}
}

# =========================================================
# SESSION STATE
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "scores" not in st.session_state:
    st.session_state.scores = []

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = None

# =========================================================
# STARTMENÜ
# =========================================================

if not st.session_state.started:

    st.markdown('<div class="title">🧠 ULTIMATIVES QUIZ</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Das modernste Allgemeinwissens Quiz</div>', unsafe_allow_html=True)

    with st.container():

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        player_count = st.selectbox(
            "Wie viele Spieler?",
            [1, 2, 3, 4]
        )

        player_names = []

        for i in range(player_count):

            name = st.text_input(
                f"Name Spieler {i+1}",
                key=f"name_{i}"
            )

            if name == "":
                name = f"Spieler {i+1}"

            player_names.append(name)

        level = st.selectbox(
            "Wähle ein Level",
            list(levels.keys())
        )

        target_points = st.number_input(
            "Bis wie viele Punkte wird gespielt?",
            min_value=5,
            max_value=100,
            value=10
        )

        if st.button("🎮 SPIEL STARTEN"):

            st.session_state.started = True
            st.session_state.players = player_names
            st.session_state.scores = [0] * player_count
            st.session_state.level = level
            st.session_state.target_points = target_points
            st.session_state.turn = 0

            level_range = levels[level]["range"]

            st.session_state.available_questions = questions[
                level_range[0]:level_range[1]
            ]

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SPIEL
# =========================================================

else:

    current_player = st.session_state.players[st.session_state.turn]

    st.markdown('<div class="title">🎯 QUIZ DUELL</div>', unsafe_allow_html=True)

    # Spieler anzeigen
    cols = st.columns(len(st.session_state.players))

    for i, player in enumerate(st.session_state.players):

        active = ""

        if i == st.session_state.turn:
            active = "active-player"

        with cols[i]:

            st.markdown(
                f"""
                <div class="player-card {active}">
                    🎮 {player}<br><br>
                    ⭐ {st.session_state.scores[i]} Punkte
                </div>
                """,
                unsafe_allow_html=True
            )

    # Gewinner prüfen
    for i, score in enumerate(st.session_state.scores):

        if score >= st.session_state.target_points:

            st.balloons()

            st.success(
                f"🏆 {st.session_state.players[i]} hat gewonnen!"
            )

            st.stop()

    st.markdown(
        f"""
        <div class="turn-box">
            🔥 Jetzt ist {current_player} dran!
        </div>
        """,
        unsafe_allow_html=True
    )

    # Neue Frage
    if st.session_state.current_question is None:

        st.session_state.current_question = random.choice(
            st.session_state.available_questions
        )

    q = st.session_state.current_question

    # Frage anzeigen
    st.markdown(
        f"""
        <div class="question-box">
            {q['question']}
        </div>
        """,
        unsafe_allow_html=True
    )

    correct = False

    # =====================================================
    # ABC
    # =====================================================

    if q["type"] == "abc":

        answer = st.radio(
            "Wähle eine Antwort:",
            q["options"]
        )

        if st.button("✅ Antwort bestätigen"):

            if answer == q["answer"]:
                correct = True

            if correct:

                points = levels[st.session_state.level]["points"]

                st.success(f"Richtig! +{points} Punkte")
                st.balloons()

                st.session_state.scores[
                    st.session_state.turn
                ] += points

            else:

                st.error("❌ Leider falsch!")
                st.snow()

            st.session_state.current_question = None

            st.session_state.turn += 1

            if st.session_state.turn >= len(st.session_state.players):
                st.session_state.turn = 0

            st.rerun()

    # =====================================================
    # WAHR / FALSCH
    # =====================================================

    elif q["type"] == "tf":

        answer = st.radio(
            "Wahr oder falsch?",
            ["Wahr", "Falsch"]
        )

        if st.button("✅ Antwort bestätigen"):

            bool_answer = answer == "Wahr"

            if bool_answer == q["answer"]:
                correct = True

            if correct:

                points = levels[st.session_state.level]["points"]

                st.success(f"Richtig! +{points} Punkte")
                st.balloons()

                st.session_state.scores[
                    st.session_state.turn
                ] += points

            else:

                st.error("❌ Leider falsch!")
                st.snow()

            st.session_state.current_question = None

            st.session_state.turn += 1

            if st.session_state.turn >= len(st.session_state.players):
                st.session_state.turn = 0

            st.rerun()

    # =====================================================
    # SCHÄTZFRAGEN
    # =====================================================

    elif q["type"] == "estimate":

        answer = st.number_input(
            "Deine Schätzung",
            value=0
        )

        if st.button("✅ Antwort bestätigen"):

            correct_value = q["answer"]

            tolerance = correct_value * 0.10

            if abs(answer - correct_value) <= tolerance:
                correct = True

            if correct:

                points = levels[st.session_state.level]["points"]

                st.success(f"Richtig! +{points} Punkte")
                st.balloons()

                st.session_state.scores[
                    st.session_state.turn
                ] += points

            else:

                st.error(
                    f"❌ Leider falsch! Richtige Antwort: {correct_value}"
                )

                st.snow()

            st.session_state.current_question = None

            st.session_state.turn += 1

            if st.session_state.turn >= len(st.session_state.players):
                st.session_state.turn = 0

            st.rerun()
