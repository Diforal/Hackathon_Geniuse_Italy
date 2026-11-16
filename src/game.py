"""Game rules. This module is independent of Streamlit and network access."""

import random

from src.clues import create_hints_pool, mark_guessed_categories, try_unlock_hint

MAX_ATTEMPTS = 10


def check_all_parameters(secret, guess):
    """Return feedback for numeric and categorical country properties."""
    results = {}
    for field, label in (("population", "Population"), ("area", "Land area")):
        target_value = secret.get(field)
        guessed_value = guess.get(field)
        if not isinstance(target_value, (int, float)) or not isinstance(guessed_value, (int, float)) or target_value <= 0 or guessed_value <= 0:
            results[field] = f"{label}: comparison data unavailable."
            continue

        ratio = target_value / guessed_value
        if 0.9 <= ratio <= 1.1:
            results[field] = f"{label}: within 10% of the target."
        elif ratio > 1.1:
            results[field] = f"{label}: the target is larger; try a higher value."
        else:
            results[field] = f"{label}: the target is smaller; try a lower value."

    for field, label in (("region", "Region"), ("subregion", "Subregion")):
        target_value = secret.get(field)
        guessed_value = guess.get(field)
        if target_value in (None, "Unknown") or guessed_value in (None, "Unknown"):
            results[field] = f"{label}: comparison data unavailable."
        elif target_value == guessed_value:
            results[field] = f"{label}: matches the target."
        else:
            results[field] = f"{label}: different from the target."

    if secret.get("landlocked") is None or guess.get("landlocked") is None:
        results["landlocked"] = "Sea access: comparison data unavailable."
    elif secret["landlocked"] == guess["landlocked"]:
        results["landlocked"] = "Sea access: same as the target."
    else:
        results["landlocked"] = "Sea access: different from the target."

    return results


def find_country(countries, name):
    normalized_name = str(name).strip().casefold()
    return next(
        (country for country in countries if country.get("name", "").strip().casefold() == normalized_name),
        None,
    )


def create_new_game(countries):
    if not countries:
        raise ValueError("The country list is empty.")

    secret = dict(random.choice(countries))
    return {
        "secret": secret,
        "all_hints": create_hints_pool(secret),
        "guessed_params": set(),
        "used_hint_keys": set(),
        "attempt": 1,
        "status": "playing",
        "history": [],
        "unlocked_hints": [],
        "error": None,
    }


def process_guess(state, guess):
    """Record a valid guess, reject duplicates, compare it, and advance the round."""
    if state["status"] != "playing":
        return state

    if any(item["code"] == guess.get("code") for item in state["history"]):
        state["error"] = "You already guessed that country. Choose another one."
        return state

    state["error"] = None
    comparison = check_all_parameters(state["secret"], guess)
    state["history"].append({
        "attempt": state["attempt"],
        "code": guess.get("code"),
        "country": guess["name"],
        "comparison": comparison,
    })

    if guess.get("code") == state["secret"].get("code"):
        state["status"] = "won"
        return state

    mark_guessed_categories(state["guessed_params"], state["secret"], guess)
    hint = try_unlock_hint(
        state["attempt"],
        state["all_hints"],
        state["guessed_params"],
        state["used_hint_keys"],
    )
    if hint:
        state["unlocked_hints"].append(hint)

    if state["attempt"] >= MAX_ATTEMPTS:
        state["status"] = "lost"
    else:
        state["attempt"] += 1

    return state
