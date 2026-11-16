import csv
import random

HINT_STEPS = (5, 7, 9)


def load_language_groups(csv_path="europe_languages.csv"):
    groups = {}

    try:
        with open(csv_path, encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                groups.setdefault(row["branch"], []).append(row["name"])
    except FileNotFoundError:
        pass

    return groups


def get_language_group(country, language_groups):
    language = country.get("languages", "Unknown")

    for group, languages in language_groups.items():
        if language in languages:
            return group

    return country.get("language_group", "Unknown")


def create_hints_pool(secret, language_groups):
    sea_access = (
        "No sea access" if secret.get("landlocked") else "Has sea access"
    )

    return {
        "landlocked": f"Sea access — {sea_access}",
        "subregion": f"Subregion — {secret.get('subregion', 'Unknown')}",
        "language_group": (
            f"Language group — {get_language_group(secret, language_groups)}"
        ),
    }


def mark_guessed_categories(guessed_params, secret, guess, language_groups):
    if secret.get("landlocked") == guess.get("landlocked"):
        guessed_params.add("landlocked")

    if secret.get("subregion") == guess.get("subregion"):
        guessed_params.add("subregion")

    if get_language_group(secret, language_groups) == get_language_group(
        guess, language_groups
    ):
        guessed_params.add("language_group")

    return guessed_params


def try_unlock_hint(attempt, all_hints, guessed_params, used_hint_keys):
    if attempt not in HINT_STEPS:
        return None

    available = [
        key for key in all_hints
        if key not in guessed_params and key not in used_hint_keys
    ]

    if not available:
        return None

    key = random.choice(available)
    used_hint_keys.add(key)
    return f"Hint (after attempt {attempt}): {all_hints[key]}"