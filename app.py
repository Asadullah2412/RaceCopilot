# app.py
# Streamlit UI — the only file the user interacts with.
# Never imports google.generativeai directly.
# All API logic lives in gemini_client.py.

import streamlit as st
from gemini_client import analyse_debrief, followup_chat

# ─────────────────────────────────────────────
# PAGE CONFIG
# Must be the first Streamlit call in the file.
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Pit Wall Engineer",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #0d0d0d;
    color: #e8e2d9;
}

/* ── Header ── */
.pit-header {
    display: flex;
    align-items: baseline;
    gap: 14px;
    padding: 8px 0 24px;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 28px;
}
.pit-header h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #e8e2d9;
    margin: 0;
}
.pit-header .sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #e8331a;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Sidebar labels ── */
.sidebar-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #666;
    margin: 20px 0 8px;
}

/* ── Debrief box ── */
.debrief-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 6px;
}

/* ── Output cards ── */
.card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 6px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.card-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #e8331a;
    margin-bottom: 14px;
}
.corner-row {
    border-bottom: 1px solid #1e1e1e;
    padding: 10px 0;
}
.corner-row:last-child { border-bottom: none; }
.corner-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e8e2d9;
    letter-spacing: 0.03em;
}
.corner-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #555;
    margin-top: 2px;
}
.corner-text {
    font-size: 0.88rem;
    color: #aaa;
    margin-top: 4px;
    line-height: 1.5;
}
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 3px;
    margin-right: 6px;
}
.badge-high   { background: #3a1010; color: #e8331a; }
.badge-medium { background: #2a2010; color: #c8922a; }
.badge-low    { background: #101a10; color: #4a9a4a; }
.change-item {
    border-left: 2px solid #e8331a;
    padding: 6px 0 6px 14px;
    margin-bottom: 10px;
}
.change-item:last-child { margin-bottom: 0; }
.change-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e8e2d9;
}
.change-sub {
    font-size: 0.82rem;
    color: #777;
    margin-top: 2px;
    line-height: 1.4;
}
.insight-item {
    padding: 8px 0;
    border-bottom: 1px solid #1e1e1e;
}
.insight-item:last-child { border-bottom: none; }
.insight-corner {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #c8922a;
}
.insight-tip {
    font-size: 0.86rem;
    color: #aaa;
    margin-top: 3px;
    line-height: 1.5;
}
.driving-note {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #aaa;
    padding: 6px 0;
    border-bottom: 1px solid #1a1a1a;
    line-height: 1.5;
}
.driving-note:last-child { border-bottom: none; }
.driving-note::before { content: "→  "; color: #e8331a; }

/* ── Summary bar ── */
.summary-bar {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #e8331a;
    border-radius: 4px;
    padding: 14px 18px;
    margin-bottom: 20px;
    font-size: 0.92rem;
    color: #ccc;
    line-height: 1.6;
    font-style: italic;
}

/* ── Follow-up questions ── */
.fq-item {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #666;
    padding: 5px 0;
}
.fq-item::before { content: "?  "; color: #555; }

/* ── Chat messages ── */
.chat-engineer {
    background: #141414;
    border: 1px solid #222;
    border-radius: 0 6px 6px 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.88rem;
    color: #ccc;
    line-height: 1.6;
    max-width: 85%;
}
.chat-driver {
    background: #1a1008;
    border: 1px solid #2a1e08;
    border-radius: 6px 0 6px 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 0.88rem;
    color: #c8922a;
    line-height: 1.6;
    max-width: 85%;
    margin-left: auto;
}
.chat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 4px;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 28px 0;
}

/* ── Button overrides ── */
.stButton > button {
    background: #e8331a !important;
    color: #fff !important;
    border: none !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 4px !important;
    padding: 10px 24px !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: #141414 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e2d9 !important;
    font-family: 'Barlow', sans-serif !important;
    border-radius: 4px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #e8331a !important;
    box-shadow: none !important;
}

/* ── Streamlit chrome cleanup ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "debrief_submitted": False,   # gates which UI state is shown
        "analysis":          None,    # parsed JSON dict from analyse_debrief()
        "chat_history":      [],      # list of {"role": "user"|"engineer", "text": str}
        "raw_debrief":       "",      # stored so we can display it after submission
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─────────────────────────────────────────────
# SIDEBAR — session context
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="sidebar-section">Session</p>', unsafe_allow_html=True)

    sim = st.selectbox("Sim platform", [
        "Assetto Corsa Competizione",
        "iRacing",
        "F1 24",
        "F1 23",
        "rFactor 2",
        "Automobilista 2",
        "Le Mans Ultimate",
        "Gran Turismo 7",
    ])

    car_class = st.selectbox("Car class", [
        "GT3", "GT4", "GTE", "LMP2", "LMP3",
        "Formula — open wheel", "Touring car", "Hypercar",
    ])

    track = st.text_input("Track", placeholder="e.g. Spa-Francorchamps")

    col1, col2 = st.columns(2)
    with col1:
        laps = st.number_input("Laps", min_value=1, max_value=200, value=10)
    with col2:
        conditions = st.selectbox("Conditions", ["Dry", "Damp", "Wet"])

    st.markdown('<p class="sidebar-section">Quick starts</p>', unsafe_allow_html=True)

    quick_prompts = {
        "Rear snap":        "The rear keeps snapping on me, especially under braking and through fast corners.",
        "Understeer":       "The car is pushing wide at the front through slow corners, I can't rotate it.",
        "Tyre deg":         "My tyres are dying fast, they feel dead after 10 laps and I'm losing loads of time.",
        "Traction issues":  "I'm losing the rear on corner exit, lots of wheelspin especially on slow corners.",
    }

    for label, text in quick_prompts.items():
        if st.button(label, key=f"quick_{label}", use_container_width=True):
            st.session_state["prefill"] = text

    st.markdown("---")

    if st.button("🔄  New session", use_container_width=True):
        for key in ["debrief_submitted", "analysis", "chat_history", "raw_debrief", "prefill"]:
            st.session_state.pop(key, None)
        st.rerun()


# ─────────────────────────────────────────────
# MAIN AREA — header
# ─────────────────────────────────────────────

st.markdown("""
<div class="pit-header">
    <h1>🏁 Pit Wall</h1>
    <span class="sub">Race Engineer AI</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STATE 1 — DEBRIEF INPUT
# Shown when no debrief has been submitted yet.
# ─────────────────────────────────────────────

if not st.session_state.debrief_submitted:

    st.markdown('<p class="debrief-label">Driver debrief — just talk, describe what you felt</p>', unsafe_allow_html=True)

    prefill = st.session_state.pop("prefill", "")

    debrief_text = st.text_area(
        label="debrief",
        label_visibility="collapsed",
        value=prefill,
        placeholder=(
            "e.g. Did 10 laps at Spa in the GT3. Rear was really unstable through Eau Rouge "
            "especially on the first few cold laps. Lost the car completely on lap 9 at Pouhon. "
            "Braking into La Source feels okay but I think I'm leaving time there. "
            "Struggling with traction out of Bus Stop..."
        ),
        height=200,
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("Analyse", use_container_width=True)

    if submit:
        if not track.strip():
            st.error("Set your track in the sidebar before submitting.")
        elif not debrief_text.strip():
            st.error("Write something in the debrief box first.")
        else:
            with st.spinner("Engineer is reviewing your debrief..."):
                result = analyse_debrief(
                    sim=sim,
                    car_class=car_class,
                    track=track,
                    laps=laps,
                    conditions=conditions,
                    driver_debrief=debrief_text,
                )

            if result["status"] == "error":
                st.error(result["message"])
            else:
                st.session_state.analysis         = result["data"]
                st.session_state.raw_debrief      = debrief_text
                st.session_state.debrief_submitted = True
                st.rerun()


# ─────────────────────────────────────────────
# STATES 2 & 3 — ANALYSIS OUTPUT + FOLLOW-UP
# Shown after a successful debrief submission.
# ─────────────────────────────────────────────

else:
    data = st.session_state.analysis

    # ── Summary bar ──────────────────────────
    if data.get("summary"):
        st.markdown(
            f'<div class="summary-bar">{data["summary"]}</div>',
            unsafe_allow_html=True,
        )

    # ── Four output columns ──────────────────
    left_col, right_col = st.columns(2, gap="large")

    # CORNER NOTES
    with left_col:
        if data.get("corner_notes"):
            st.markdown('<div class="card"><p class="card-title">Corner notes</p>', unsafe_allow_html=True)
            for c in data["corner_notes"]:
                lap_ctx = f' &nbsp;·&nbsp; {c.get("lap_context")}' if c.get("lap_context") and c.get("lap_context") != "null" else ""
                st.markdown(f"""
                <div class="corner-row">
                    <div class="corner-name">{c.get("corner","")}</div>
                    <div class="corner-meta">{c.get("issue","")}{lap_ctx}</div>
                    <div class="corner-text">{c.get("diagnosis","")}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # DRIVING NOTES
        if data.get("driving_notes"):
            st.markdown('<div class="card"><p class="card-title">Driving notes</p>', unsafe_allow_html=True)
            for note in data["driving_notes"]:
                st.markdown(f'<div class="driving-note">{note}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # CAR DIAGNOSIS + SETUP CHANGES + TRACK INSIGHT
    with right_col:
        if data.get("car_diagnosis"):
            st.markdown('<div class="card"><p class="card-title">Car diagnosis</p>', unsafe_allow_html=True)
            for item in data["car_diagnosis"]:
                sev = item.get("severity", "medium").lower()
                badge_class = f"badge-{sev}"
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <span class="badge {badge_class}">{sev}</span>
                    <span style="font-size:0.9rem; font-weight:500; color:#e8e2d9;">{item.get("issue","")}</span>
                    <div class="corner-text">{item.get("explanation","")}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if data.get("setup_changes"):
            st.markdown('<div class="card"><p class="card-title">Setup changes</p>', unsafe_allow_html=True)
            for s in data["setup_changes"]:
                st.markdown(f"""
                <div class="change-item">
                    <div class="change-title">{s.get("change","")}</div>
                    <div class="change-sub">{s.get("reason","")} — <em>{s.get("expected_effect","")}</em></div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if data.get("track_insight"):
            st.markdown('<div class="card"><p class="card-title">Track insight</p>', unsafe_allow_html=True)
            for t in data["track_insight"]:
                st.markdown(f"""
                <div class="insight-item">
                    <div class="insight-corner">{t.get("corner","")}</div>
                    <div class="insight-tip">{t.get("tip","")}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Engineer follow-up questions ─────────
    if data.get("follow_up_questions"):
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="debrief-label">Engineer wants to know</p>', unsafe_allow_html=True)
        for q in data["follow_up_questions"]:
            st.markdown(f'<div class="fq-item">{q}</div>', unsafe_allow_html=True)

    # ── Follow-up chat ───────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<p class="debrief-label">Follow-up — ask anything from the debrief</p>', unsafe_allow_html=True)

    # Render existing chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; margin-bottom:6px;">
                <div>
                    <div class="chat-label" style="text-align:right;">Driver</div>
                    <div class="chat-driver">{msg["text"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin-bottom:6px;">
                <div class="chat-label">Engineer</div>
                <div class="chat-engineer">{msg["text"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # Chat input
    follow_up = st.chat_input("Ask a follow-up — e.g. 'tell me more about Pouhon technique'")

    if follow_up:
        st.session_state.chat_history.append({"role": "user", "text": follow_up})

        with st.spinner("Engineer is thinking..."):
            result = followup_chat(
                sim=sim,
                car_class=car_class,
                track=track,
                laps=laps,
                conditions=conditions,
                original_analysis=data,
                chat_history=st.session_state.chat_history,
                new_question=follow_up,
            )

        if result["status"] == "error":
            st.error(result["message"])
        else:
            st.session_state.chat_history.append({
                "role": "engineer",
                "text": result["reply"],
            })

        st.rerun()