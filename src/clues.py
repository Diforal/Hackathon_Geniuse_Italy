import random
HINT_STEPS = (5, 7, 9)


def _format_sea_access(country):
    """Returns readable sea access status from 'water_access' or boolean 'landlocked'."""
    if "water_access" in country:
        return country["water_access"]
    if "landlocked" in country:
        return "Landlocked (no sea access)" if country["landlocked"] else "Has sea access"
    return "Unknown"


def _format_language_group(country):
    """Returns the language group prepared by the team, or falls back to raw languages."""
    if country.get("language_group"):
        return country["language_group"]

    langs = country.get("languages")
    if isinstance(langs, list) and langs:
        names = [item["name"] if isinstance(item, dict) else str(item) for item in langs]
        return ", ".join(names)
    if isinstance(langs, dict) and langs:
        return ", ".join(langs.values())
    return str(langs) if langs else "Unknown"


def create_hints_pool(secret):
    """Creates a dictionary of hints across 3 categories: sea access, subregion, language group."""
    subregion = secret.get("subregion") or "Unknown"
    return {
        "landlocked": f"Sea access — {_format_sea_access(secret)}",
        "subregion": f"Subregion of the secret country — {subregion}",
        "language_group": f"Language group of the secret country — {_format_language_group(secret)}",
    }


def mark_guessed_categories(guessed_params, secret, guess):
    """Records and returns the hint categories that the player has already matched."""
    if _format_sea_access(secret) == _format_sea_access(guess):
        guessed_params.add("landlocked")

    if secret.get("subregion") == guess.get("subregion"):
        guessed_params.add("subregion")

    if _format_language_group(secret) == _format_language_group(guess):
        guessed_params.add("language_group")

    return guessed_params


def try_unlock_hint(attempt, all_hints, guessed_params, used_hint_keys):
    """
    Checks whether a hint unlocks after the current attempt (5, 7, or 9).
    Returns the hint string only for an unguessed category, or None.
    """
    if attempt not in HINT_STEPS:
        return None
    available_keys = [key for key in all_hints if key not in guessed_params and key not in used_hint_keys]
    if available_keys:
        chosen_key = random.choice(available_keys)
        used_hint_keys.add(chosen_key)
        return f"💡 Hint (after attempt {attempt}): {all_hints[chosen_key]}"
    if "all_known" not in used_hint_keys:
        used_hint_keys.add("all_known")
        return f"💡 Hint (after attempt {attempt}): Sea access, subregion, and language group are already known! Focus on area and population."

    return None