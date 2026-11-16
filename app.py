import streamlit as st

from src.catalog import get_country_facts, load_european_country_list
from src.clues import create_hints_pool
from src.game import MAX_ATTEMPTS, create_new_game, process_guess
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
      .clue-heading { display:flex; align-items:baseline; justify-content:space-between; gap:1rem; margin:2rem 0 .8rem; padding-bottom:.55rem; border-bottom:1px solid #d3d0c4; }
      .clue-heading strong { color:#1d2824; font:500 1.35rem 'Fraunces',Georgia,serif; }
      .clue-heading span { color:#707a70; font:500 .63rem 'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase; }
      .guess-row { padding:.8rem 0; border-bottom:1px solid #d3d0c4; }
      .guess-name { color:#1d2824; font:500 1.1rem 'Fraunces',Georgia,serif; }
      .comparison { color:#515d55; font-size:.86rem; line-height:1.5; margin:.4rem 0 0; }
      .tiny-note { margin:1rem 0 0; color:#707a70; font:400 .68rem 'DM Mono',monospace; }
      @media(max-width:600px){.game-intro{align-items:start;flex-direction:column}}
    </style>
    """,
    unsafe_allow_html=True,
)

render_masthead()

try:
    api_key = st.secrets["RESTCOUNTRIES_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("Add RESTCOUNTRIES_API_KEY to .streamlit/secrets.toml locally and to Streamlit Cloud Secrets before playing.")
    st.stop()

@st.cache_data(ttl=60 * 60 * 24 * 3, show_spinner=False)
def cached_country_facts(code, token):
    return get_country_facts(code, token)

@st.cache_data(ttl=60 * 60 * 24 * 3, show_spinner=False)
def cached_country_list(token):
    return load_european_country_list(token)

try:
    country_list = cached_country_list(api_key)
except Exception as error:
    st.error(f"Could not load the European country list: {error}")
    st.stop()

if not country_list:
    st.error("The country CSV has no playable countries with ISO codes.")
    st.stop()

if "game" not in st.session_state:
    st.session_state.game = create_new_game(country_list)

game = st.session_state.game
try:
    if "population" not in game["secret"]:
        game["secret"].update(cached_country_facts(game["secret"]["code"], api_key))
        game["all_hints"] = create_hints_pool(game["secret"])
except Exception as error:
    st.error(f"Could not load the mystery country data from REST Countries: {error}")
    if st.button("Try again"):
        st.rerun()
    st.stop()

st.markdown(
    f"""
    <div class="game-intro">
      <div>
        <h2>Mystery country</h2>
        <p>Use each comparison to narrow down the answer.</p>
      </div>
      <div class="round-chip">Attempt {min(game['attempt'], MAX_ATTEMPTS)} of {MAX_ATTEMPTS}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if game["status"] == "playing":
    guessed_codes = {item["code"] for item in game["history"]}
    remaining_countries = [country for country in country_list if country["code"] not in guessed_codes]
    options = {country["name"]: country for country in remaining_countries}

    with st.form("country-guess", clear_on_submit=True):
        country_col, button_col = st.columns([4, 1.35])
        with country_col:
            selected_name = st.selectbox("Choose a country", list(options), placeholder="Search countries…")
        with button_col:
            submitted = st.form_submit_button("Make guess", use_container_width=True)

    if submitted:
        selected_country = options[selected_name]
        try:
            guess_facts = cached_country_facts(selected_country["code"], api_key)
            process_guess(game, guess_facts)
        except Exception as error:
            game["error"] = f"Could not load {selected_name} from REST Countries: {error}"
        st.session_state.game = game
        st.rerun()

if game.get("error"):
    st.error(game["error"])

if game["status"] == "won":
    st.success(f"You found {game['secret']['name']} in {len(game['history'])} guesses!")
elif game["status"] == "lost":
    st.error(f"Out of guesses. The country was {game['secret']['name']}.")

if game["unlocked_hints"]:
    st.markdown("### Extra hints")
    for hint in game["unlocked_hints"]:
        st.info(hint)

if game["history"]:
    st.markdown(
        f"<div class=clue-heading><strong>Your guesses</strong><span>{len(game['history'])} total</span></div>",
        unsafe_allow_html=True,
    )
    for entry in reversed(game["history"]):
        with st.container(border=True):
            st.markdown(f"**{entry['attempt']:02d} · {entry['country']}**")
            for feedback in entry["comparison"].values():
                st.markdown(f"- {feedback}")
else:
    st.info("Choose a country to make your first guess. After each wrong guess, compare its area and population with the target.")

if game["status"] != "playing":
    if st.button("Start a new round"):
        st.session_state.game = create_new_game(country_list)
        st.rerun()

st.caption("Playable countries are the European entries in the supplied most-visited countries CSV. Country facts are provided by REST Countries.")
