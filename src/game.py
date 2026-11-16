from comparing import check_all_parameters
from hints import create_hints_pool, mark_guessed_categories, try_unlock_hint

MAX_ATTEMPTS = 10

def _get_country_name(row):
    """Returns the primary English country name from a DataFrame row."""
    if "eng_name" in row:
        return row["eng_name"]
    return row.get("name", "Unknown")


def find_country(df, query):
    """Searches for a country in the DataFrame by name (case-insensitive)."""
    clean_query = str(query).strip().lower()
    if not clean_query:
        return None
    search_cols = [col for col in ("eng_name", "ukr_name", "name") if col in df.columns]
    mask = False
    for col in search_cols:
        mask = mask | (df[col].astype(str).str.lower() == clean_query)
    match = df[mask]
    return None if match.empty else match.iloc[0]

def create_new_game(df):
    """Initializes and returns a clean game state dictionary for a new round."""
    secret = df.sample(1).iloc[0]
    return {
        "secret": secret,
        "all_hints": create_hints_pool(secret),
        "guessed_params": set(),
        "used_hint_keys": set(),
        "attempt": 1,
        "max_attempts": MAX_ATTEMPTS,
        "status": "playing",  # "playing", "won", "lost"
        "history": [],
        "unlocked_hints": [],
        "error": None,
    }


def process_guess(state, df, user_input):
    """
    Processes a single player guess, updates the game state, and returns it.
    Uses only return values so the UI layer can render the output.
    """
    if state["status"] != "playing":
        return state
    guess = find_country(df, user_input)
    if guess is None:
        state["error"] = "Country not found among European countries."
        return state
    state["error"] = None
    secret = state["secret"]
    comparison = check_all_parameters(secret, guess)
    # Record any hint categories matched during this guess
    mark_guessed_categories(state["guessed_params"], secret, guess)
    # Save attempt details to history
    state["history"].append({
        "attempt": state["attempt"],
        "country": _get_country_name(guess),
        "comparison": comparison,
    })
    # Check win condition
    if _get_country_name(guess) == _get_country_name(secret):
        state["status"] = "won"
        return state
    # Unlock a hint on attempts 5, 7, or 9 for an unguessed category
    hint_text = try_unlock_hint(state["attempt"], state["all_hints"], state["guessed_params"], state["used_hint_keys"])
    if hint_text:
        state["unlocked_hints"].append(hint_text)
    # Advance turn or end game on max attempts
    if state["attempt"] >= state["max_attempts"]:
        state["status"] = "lost"
    else:
        state["attempt"] += 1

    return state

