# =========================================================
# ULTIMATIVES ALLGEMEINWISSENS QUIZ
# KOMPLETTER FINALER CODE
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

# =========================================================
# HINTERGRUND WECHSEL
# =========================================================

st_autorefresh(interval=20000, key="bgrefresh")

# =========================================================
# SESSION STATE
# =========================================================

if "bg_index" not in st.session_state:
    st.session_state.bg_index = 0

if "started" not in st.session_state:
    st.session_state.started = False

if "scores" not in st.session_state:
    st.session_state.scores = []

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = None

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

# sanfter Hintergrundwechsel
st.session_state.bg_index += 1

if st.session_state.bg_index >= len(backgrounds):
    st.session_state.bg_index = 0

bg = backgrounds[st.session_state.bg_index]

# =========================================================
# DESIGN
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background:
        linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.75)),
        url("{bg}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;

        color: white;

        animation: backgroundFade 2s ease-in-out;
        transition: background-image 2s ease-in-out;
    }}

    @keyframes backgroundFade {{
        0% {{
            opacity: 0.92;
        }}

        100% {{
            opacity: 1;
        }}
    }}

    .title {{
        text-align: center;
        font-size: 70px;
        font-weight: 900;
        color: white;
        margin-top: 20px;
        margin-bottom: 5px;

        text-shadow:
        0 0 10px rgba(0,255,213,0.8),
        0 0 20px rgba(0,255,213,0.6),
        0 0 40px rgba(0,255,213,0.4);
    }}

    .subtitle {{
        text-align: center;
        font-size: 24px;
        color: #d6d6d6;
        margin-bottom: 40px;
    }}

    .glass {{
        background: rgba(255,255,255,0.10);
        backdrop-filter: blur(20px);

        border-radius: 30px;
        padding: 35px;

        border: 1px solid rgba(255,255,255,0.2);

        box-shadow:
        0 8px 32px rgba(0,0,0,0.35),
        0 0 20px rgba(255,255,255,0.05);
    }}

    .player-card {{
        background: rgba(255,255,255,0.10);

        border-radius: 25px;

        padding: 25px;

        text-align: center;

        font-size: 24px;

        font-weight: bold;

        transition: all 0.3s ease;

        border: 2px solid rgba(255,255,255,0.08);
    }}

    .active-player {{
        border: 3px solid #00ffd5;

        background: rgba(0,255,213,0.18);

        transform: scale(1.05);

        box-shadow:
        0 0 20px rgba(0,255,213,0.8),
        0 0 40px rgba(0,255,213,0.3);
    }}

    .question-box {{
        background: rgba(0,0,0,0.45);

        border-radius: 30px;

        padding: 45px;

        margin-top: 30px;
        margin-bottom: 30px;

        text-align: center;

        font-size: 36px;

        font-weight: bold;

        animation: questionFade 0.7s ease;
    }}

    @keyframes questionFade {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}

        to {{
            opacity: 1;
            transform: translateY(0px);
        }}
    }}

    .turn-box {{
        text-align: center;

        font-size: 32px;

        font-weight: bold;

        color: #00ffd5;

        margin-top: 10px;
        margin-bottom: 30px;

        animation: pulse 1.8s infinite;
    }}

    @keyframes pulse {{
        0% {{
            transform: scale(1);
        }}

        50% {{
            transform: scale(1.04);
        }}

        100% {{
            transform: scale(1);
        }}
    }}

    /* BUTTONS */

    div.stButton > button {{

        width: 100%;

        height: 65px;

        border-radius: 18px;

        border: none;

        font-size: 22px;

        font-weight: bold;

        color: white;

        background:
        linear-gradient(
            135deg,
            #00ffd5,
            #0099ff,
            #6a5cff
        );

        background-size: 200% 200%;

        animation: gradientMove 4s ease infinite;

        transition: all 0.3s ease;

        box-shadow:
        0 0 15px rgba(0,255,213,0.4),
        0 0 25px rgba(0,153,255,0.3);
    }}

    div.stButton > button:hover {{

        transform: scale(1.03);

        box-shadow:
        0 0 25px rgba(0,255,213,0.8),
        0 0 45px rgba(0,153,255,0.5);
    }}

    @keyframes gradientMove {{
        0% {{
            background-position: 0% 50%;
        }}

        50% {{
            background-position: 100% 50%;
        }}

        100% {{
            background-position: 0% 50%;
        }}
    }}

    /* FORMULAR */

    .stTextInput label,
    .stSelectbox label,
    .stNumberInput label,
    .stRadio label {{
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }}

    div[data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.10);
        border-radius: 15px;
    }}

    input {{
        border-radius: 12px !important;
    }}

    h1,h2,h3,h4,h5 {{
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
# STARTMENÜ
# =========================================================

if not st.session_state.started:

    st.markdown(
        '<div class="title">🧠 ULTIMATIVES QUIZ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Das modernste Allgemeinwissens Quiz</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    player_count = st.selectbox(
        "🎮 Anzahl Spieler",
        [1, 2, 3, 4],
        index=0
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
        "🏆 Schwierigkeit",
        list(levels.keys())
    )

    target_points = st.number_input(
        "⭐ Punkte zum Gewinnen",
        min_value=5,
        max_value=100,
        value=10
    )

    if st.button("🚀 SPIEL STARTEN", use_container_width=True):

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

    current_player = st.session_state.players[
        st.session_state.turn
    ]

    st.markdown(
        '<div class="title">🎯 QUIZ DUELL</div>',
        unsafe_allow_html=True
    )

    # SPIELER KARTEN

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

    # GEWINNER

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

    # FRAGE

    if st.session_state.current_question is None:

        st.session_state.current_question = random.choice(
            st.session_state.available_questions
        )

    q = st.session_state.current_question

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
            "Antwort auswählen",
            q["options"]
        )

        if st.button("✅ Antwort bestätigen"):

            if answer == q["answer"]:
                correct = True

    # =====================================================
    # WAHR/FALSCH
    # =====================================================

    elif q["type"] == "tf":

        answer = st.radio(
            "Wahr oder falsch?",
            ["Wahr", "Falsch"]
        )

        if st.button("✅ Antwort bestätigen"):

            if (answer == "Wahr") == q["answer"]:
                correct = True

    # =====================================================
    # SCHÄTZFRAGEN
    # =====================================================

    elif q["type"] == "estimate":

        answer = st.number_input(
            "Deine Schätzung",
            value=0
        )

        if st.button("✅ Antwort bestätigen"):

            tolerance = q["answer"] * 0.10

            if abs(answer - q["answer"]) <= tolerance:
                correct = True

    # =====================================================
    # AUSWERTUNG
    # =====================================================

    if correct:

        points = levels[
            st.session_state.level
        ]["points"]

        st.success(f"✅ Richtig! +{points} Punkte")

        st.balloons()

        st.session_state.scores[
            st.session_state.turn
        ] += points

    elif "Antwort bestätigen":

        pass

    # Nächster Spieler

    if st.button("➡️ NÄCHSTE FRAGE", use_container_width=True):

        st.session_state.current_question = None

        st.session_state.turn += 1

        if st.session_state.turn >= len(st.session_state.players):

            st.session_state.turn = 0

        st.rerun()
