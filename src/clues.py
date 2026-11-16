"""Comparison feedback and milestone hints for KrainaLe."""

import random

HINT_STEPS = (5, 7, 9)


def _same_known_value(first, second):
    return first is not None and second is not None and first != "Unknown" and first == second


def create_hints_pool(secret):
    sea_access = "No sea access" if secret.get("landlocked") else "Has sea access"
    language = (secret.get("languages") or ["Unknown"])[0]
    return {
        "region": f"Region — {secret.get('region', 'Unknown')}",
        "subregion": f"Subregion — {secret.get('subregion', 'Unknown')}",
        "landlocked": f"Sea access — {sea_access}",
        "language": f"Language — {language}",
    }


def mark_guessed_categories(guessed_params, secret, guess):
    for field in ("region", "subregion"):
        if _same_known_value(secret.get(field), guess.get(field)):
            guessed_params.add(field)

    if secret.get("landlocked") is not None and secret.get("landlocked") == guess.get("landlocked"):
        guessed_params.add("landlocked")

    secret_languages = set(secret.get("languages") or [])
    guess_languages = set(guess.get("languages") or [])
    if secret_languages and guess_languages and secret_languages.intersection(guess_languages):
        guessed_params.add("language")

    return guessed_params


def try_unlock_hint(attempt, all_hints, guessed_params, used_hint_keys):
    if attempt not in HINT_STEPS:
        return None

    available = [
        key for key in all_hints
        if key not in guessed_params and key not in used_hint_keys
    ]

    if attempt == 7 and "subregion" not in used_hint_keys:
        key = "subregion"
    elif attempt == 9 and "language" in available:
        key = "language"
    else:
        # Hold both requested reveals for their scheduled milestones.
        earlier_hints = [
            key for key in available
            if key not in {"language", "subregion"}
        ]
        if not earlier_hints:
            return None
        key = random.choice(earlier_hints)

    used_hint_keys.add(key)
    return f"Hint (after attempt {attempt}): {all_hints[key]}"
