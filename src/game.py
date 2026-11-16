import random

from src.clues import (
    create_hints_pool,
    load_language_groups,
    mark_guessed_categories,
    try_unlock_hint,
)

MAX_ATTEMPTS = 10


def check_all_parameters(secret, guess):
    """Compare numeric and categorical country data."""
    results = {}

    for field, label in (("population", "Population"), ("area", "Area")):
        try:
            ratio = secret[field] / guess[field]
            if 0.9 <= ratio <= 1.1:
                results[field] = f"{label}: approximately right!"
            elif ratio > 1.1:
                results[field] = f"{label}: ⏫ should be higher"
            else:
                results[field] = f"{label}: ⏬ should be lower"
        except (KeyError, TypeError, ZeroDivisionError):
            results[field] = f"{label}: data unavailable"

    for field, label in (("subregion", "Subregion"), ("landlocked", "Sea access")):
        if secret.get(field) == guess.get(field):
            results[field] = f"{label}: RIGHT!"
        else:
            results[field] = f"{label}: wrong :("

    return results


def find_country(countries, name):
    name = str(name).strip().casefold()

    for country in countries:
        if country.get("name", "").casefold() == name:
            return country

    return None


def create_new_game(countries):
    language_groups = load_language_groups()
    secret = random.choice(countries)

    return {
        "secret": secret,
        "all_hints": create_hints_pool(secret, language_groups),
        "language_groups": language_groups,
        "guessed_params": set(),
        "used_hint_keys": set(),
        "attempt": 1,
        "status": "playing",
        "history": [],
        "unlocked_hints": [],
        "error": None,
    }


def process_guess(state, countries, user_input):
    if state["status"] != "playing":
        return state

    guess = find_country(countries, user_input)
    if guess is None:
        state["error"] = "Country not found."
        return state

    state["error"] = None
    secret = state["secret"]
    comparison = check_all_parameters(secret, guess)

    state["history"].append({
        "attempt": state["attempt"],
        "country": guess["name"],
        "comparison": comparison,
    })

    if guess["name"] == secret["name"]:
        state["status"] = "won"
        return state

    mark_guessed_categories(
        state["guessed_params"],
        secret,
        guess,
        state["language_groups"],
    )

    hint = try_unlock_hint(
        state["attempt"],
        state["all_hints"],
        state["guessed_params"],
        state["used_hint_keys"],
    )
    if hint:
        state["unlocked_hints"].append(hint)

    if state["attempt"] == MAX_ATTEMPTS:
        state["status"] = "lost"
    else:
        state["attempt"] += 1

    return state