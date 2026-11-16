import streamlit as st

from src.theme import apply_theme, render_masthead


st.set_page_config(
    page_title="KrainaLe - Country by Country",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed",
)
apply_theme()

st.markdown(
    """
    <style>
      .block-container { max-width: 900px; }
      .game-intro { display:flex; justify-content:space-between; align-items:end; gap:1rem; margin:2rem 0 .8rem; }
      .game-intro h2 { margin:0; font:500 clamp(1.6rem,4vw,2.25rem)/1.1 'Fraunces',Georgia,serif; color:#1d2824; letter-spacing:-.035em; }
      .game-intro p { margin:.4rem 0 0; color:#707a70; font-size:.9rem; }
      .round-chip { padding:.45rem .65rem; border:1px solid #d3d0c4; color:#58645c; font:500 .63rem 'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase; white-space:nowrap; }
      .guess-shell { margin-top:1.1rem; padding:1rem 1.1rem .25rem; background:rgba(255,255,255,.42); border:1px solid #d3d0c4; }
      .micro-label { margin:0 0 .55rem; color:#707a70; font:500 .64rem 'DM Mono',monospace; letter-spacing:.12em; text-transform:uppercase; }
      .clue-heading { display:flex; align-items:baseline; justify-content:space-between; gap:1rem; margin:2rem 0 .8rem; padding-bottom:.55rem; border-bottom:1px solid #d3d0c4; }
      .clue-heading strong { color:#1d2824; font:500 1.35rem 'Fraunces',Georgia,serif; }
      .clue-heading span { color:#707a70; font:500 .63rem 'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase; }
      .guess-row { display:grid; grid-template-columns:2.5rem minmax(0,1fr) auto; align-items:center; gap:.8rem; padding:.9rem 0; border-bottom:1px solid #d3d0c4; }
      .guess-index { color:#9a9d8b; font:500 .7rem 'DM Mono',monospace; }
      .guess-name { color:#1d2824; font:500 1.1rem 'Fraunces',Georgia,serif; }
      .guess-note { color:#707a70; font:.72rem 'DM Mono',monospace; text-align:right; }
      .clue-grid { display:grid; grid-template-columns:1fr 1fr; gap:.75rem; }
      .clue-card { position:relative; min-height:8.5rem; padding:1rem 1.1rem; background:#203b35; color:#f2f0e8; overflow:hidden; }
      .clue-card:after { content:''; position:absolute; width:8rem; height:8rem; right:-3.3rem; bottom:-5.1rem; border:1px solid rgba(242,240,232,.18); border-radius:50%; box-shadow:0 0 0 12px rgba(242,240,232,.035),0 0 0 26px rgba(242,240,232,.025); }
      .clue-card.people { background:#e7e4d9; color:#1d2824; border:1px solid #d3d0c4; }
      .clue-label { color:#c3d65b; font:500 .64rem 'DM Mono',monospace; letter-spacing:.12em; text-transform:uppercase; }
      .people .clue-label { color:#b96748; }
      .clue-value { margin:.8rem 0 .25rem; font:500 clamp(1.45rem,4vw,2rem)/1 'Fraunces',Georgia,serif; letter-spacing:-.035em; }
      .clue-detail { color:rgba(242,240,232,.72); font-size:.77rem; }
      .people .clue-detail { color:#646e65; }
      .tiny-note { margin:1rem 0 0; color:#707a70; font:400 .68rem 'DM Mono',monospace; letter-spacing:.02em; }
      @media(max-width:600px){.game-intro{align-items:start;flex-direction:column}.clue-grid{grid-template-columns:1fr}.clue-card{min-height:7.3rem}.guess-row{grid-template-columns:1.6rem minmax(0,1fr);}.guess-note{grid-column:2;text-align:left}}
    </style>
    """,
    unsafe_allow_html=True,
)

render_masthead()

st.markdown(
    """
    <div class="game-intro">
      <div>
        <h2>Mystery country</h2>
        <p>Use each comparison to narrow down the map.</p>
      </div>
      <div class="round-chip">Practice round · unlimited guesses</div>
    </div>
    """,
    unsafe_allow_html=True,
)

sample_countries = ["Argentina", "Canada", "Germany", "Greece", "Italy", "Japan", "Portugal"]
if "mock_guesses" not in st.session_state:
    st.session_state.mock_guesses = [
        {"country": "Portugal", "area": "3.2× larger", "population": "1.8× larger"}
    ]

st.markdown('<div class="guess-shell"><p class="micro-label">Your next guess</p>', unsafe_allow_html=True)
with st.form("mock-guess", clear_on_submit=False):
    country_col, button_col = st.columns([4, 1.35])
    with country_col:
        selected_country = st.selectbox(
            "Choose a country",
            sample_countries,
            label_visibility="collapsed",
            placeholder="Search countries…",
        )
    with button_col:
        submitted = st.form_submit_button("Make guess", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if selected_country == "Italy":
        st.session_state.mock_solved = True
    elif not any(item["country"] == selected_country for item in st.session_state.mock_guesses):
        st.session_state.mock_guesses.insert(
            0,
            {"country": selected_country, "area": "about the same", "population": "a little larger"},
        )
    st.rerun()

st.markdown(
    f"""
    <div class="clue-heading">
      <strong>Reading the clues</strong>
      <span>{len(st.session_state.mock_guesses):02d} guess{'es' if len(st.session_state.mock_guesses) != 1 else ''}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.get("mock_solved"):
    st.success("That’s it - the mystery country was Italy. This is sample UI feedback.")

for index, guess in enumerate(st.session_state.mock_guesses, start=1):
    st.markdown(
        f"""
        <div class="guess-row">
          <span class="guess-index">{index:02d}</span>
          <span class="guess-name">{guess['country']}</span>
          <span class="guess-note">YOUR GUESS</span>
        </div>
        <div class="clue-grid">
          <div class="clue-card">
            <div class="clue-label">Land area</div>
            <div class="clue-value">{guess['area']}</div>
            <div class="clue-detail">Target country compared with {guess['country']}</div>
          </div>
          <div class="clue-card people">
            <div class="clue-label">Population</div>
            <div class="clue-value">{guess['population']}</div>
            <div class="clue-detail">Target country compared with {guess['country']}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<p class="tiny-note">SAMPLE ROUND · COUNTRY DATA AND COMPARISON VALUES ARE PLACEHOLDERS FOR THIS VISUAL MOCK</p>',
    unsafe_allow_html=True,
)
