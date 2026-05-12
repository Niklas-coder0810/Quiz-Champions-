import streamlit as st
import random
import uuid
import requests

# =========================================================
# SUPABASE CONFIG (HIER EINTRAGEN)
# =========================================================

SUPABASE_URL = "HIER_URL_EINSETZEN"
SUPABASE_KEY = "HIER_KEY_EINSETZEN"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# =========================================================
# PAGE
# =========================================================

st.set_page_config(page_title="Online Quiz", layout="wide")

bg = "https://images.unsplash.com/photo-1506744038136-46273834b3fb"

st.markdown(f"""
<style>

.stApp {{
    background:
    linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
    url("{bg}");

    background-size: cover;
    background-position: center;
    color:white;
}}

.card {{
    background: rgba(255,255,255,0.12);
    padding:20px;
    border-radius:20px;
    backdrop-filter: blur(10px);
}}

button {{
    border-radius:15px !important;
    font-weight:bold !important;
}}

</style>
""", unsafe_allow_html=True)

# =========================================================
# QUESTIONS
# =========================================================

questions = [
    {"q":"Hauptstadt Deutschland?", "o":["Berlin","Paris","Rom"], "a":"Berlin"},
    {"q":"Sonne ist ein Stern?", "a":True},
    {"q":"Wie viele Knochen hat Mensch?", "a":206}
]

# =========================================================
# SUPABASE HELPERS
# =========================================================

def get_room(room_id):
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/rooms?id=eq.{room_id}",
        headers=HEADERS
    )
    data = r.json()
    return data[0] if data else None


def update_room(room_id, state):
    requests.patch(
        f"{SUPABASE_URL}/rest/v1/rooms?id=eq.{room_id}",
        headers=HEADERS,
        json={"state": state}
    )

def create_room(room_id):
    state = {
        "players": [],
        "scores": [],
        "turn": 0,
        "question": None
    }

    requests.post(
        f"{SUPABASE_URL}/rest/v1/rooms",
        headers=HEADERS,
        json={"id": room_id, "state": state}
    )

# =========================================================
# URL PARAMETER (ROOM SYSTEM)
# =========================================================

params = st.query_params

# =========================================================
# START SCREEN
# =========================================================

if "room" not in params:

    st.title("🧠 ONLINE QUIZ LOBBY")

    if st.button("🎮 Neue Lobby erstellen"):

        room_id = str(uuid.uuid4())[:6]
        create_room(room_id)

        st.success(f"Lobby erstellt!")
        st.code(f"?room={room_id}")

# =========================================================
# LOBBY / GAME
# =========================================================

else:

    room_id = params["room"]
    room = get_room(room_id)

    if not room:
        st.error("Lobby existiert nicht")
        st.stop()

    state = room["state"]

    st.title(f"🎯 Lobby: {room_id}")

    # =====================================================
    # PLAYER JOIN
    # =====================================================

    if "name" not in st.session_state:

        name = st.text_input("Dein Name")

        if st.button("Beitreten"):

            if len(state["players"]) >= 4:
                st.error("Lobby voll (max 4 Spieler)")
                st.stop()

            state["players"].append(name)
            state["scores"].append(0)

            update_room(room_id, state)

            st.session_state.name = name
            st.rerun()

        st.stop()

    # =====================================================
    # GAME STATE
    # =====================================================

    player = state["players"][state["turn"]]

    st.subheader(f"👉 Dran: {player}")

    # neue Frage
    if not state["question"]:
        state["question"] = random.choice(questions)
        update_room(room_id, state)

    q = state["question"]

    answer = None

    if "o" in q:
        answer = st.radio(q["q"], q["o"])
    else:
        if isinstance(q["a"], bool):
            answer = st.radio(q["q"], ["Wahr","Falsch"])
        else:
            answer = st.number_input(q["q"], value=0)

    # =====================================================
    # ANSWER
    # =====================================================

    if st.button("Antwort senden"):

        correct = False

        if "o" in q:
            correct = answer == q["a"]

        elif isinstance(q["a"], bool):
            correct = (answer == "Wahr") == q["a"]

        else:
            correct = abs(answer - q["a"]) <= q["a"] * 0.1

        if correct:
            state["scores"][state["turn"]] += 1
            st.success("Richtig!")
        else:
            st.error("Falsch!")

        # nächster Spieler
        state["turn"] = (state["turn"] + 1) % len(state["players"])
        state["question"] = None

        update_room(room_id, state)
        st.rerun()

    # =====================================================
    # SCOREBOARD
    # =====================================================

    st.write("---")
    st.write("### Punkte")

    for p, s in zip(state["players"], state["scores"]):
        st.write(f"{p}: {s}")
