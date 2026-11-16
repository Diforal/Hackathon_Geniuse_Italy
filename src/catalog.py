"""Load the playable country list and fetch facts for one country at a time."""

import csv
from pathlib import Path

import requests

API_URL = "https://api.restcountries.com/countries/v5"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = PROJECT_ROOT / "data" / "most-visited-countries-2026.csv"
RESPONSE_FIELDS = ",".join(
    [
        "codes.alpha_2",
        "names.common",
        "region",
        "subregion",
        "population",
        "area.kilometers",
        "landlocked",
        "languages",
    ]
)


def load_country_list(csv_path=DEFAULT_CSV):
    """Read playable names and ISO codes from the supplied CSV."""
    countries = []
    with open(csv_path, encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            code = (row.get("flagCode") or "").strip().upper()
            name = (row.get("country") or "").strip()
            if code and name:
                countries.append({"code": code, "name": name})

    return countries


def load_european_country_list(api_key, csv_path=DEFAULT_CSV):
    """Keep only CSV countries REST Countries classifies as Europe."""
    response = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        params={
            "region": "Europe",
            "limit": 100,
            "response_fields": "codes.alpha_2",
        },
        timeout=15,
    )
    response.raise_for_status()
    records = response.json().get("data", {}).get("objects", [])
    european_codes = {
        record.get("codes", {}).get("alpha_2", "").upper()
        for record in records
    }
    return [country for country in load_country_list(csv_path) if country["code"] in european_codes]



def parse_country(record):
    """Convert one REST Countries record to the game's small data shape."""
    raw_languages = record.get("languages") or []
    if isinstance(raw_languages, dict):
        languages = [item.get("name", "") for item in raw_languages.values()]
    else:
        languages = [item.get("name", "") for item in raw_languages]
    languages = [language for language in languages if language]

    area = record.get("area", {}).get("kilometers")
    return {
        "code": record.get("codes", {}).get("alpha_2", "").upper(),
        "name": record.get("names", {}).get("common", "Unknown"),
        "region": record.get("region") or "Unknown",
        "subregion": record.get("subregion") or "Unknown",
        "population": record.get("population"),
        "area": area,
        "landlocked": record.get("landlocked"),
        "languages": languages,
    }


def get_country_facts(code, api_key):
    """Fetch facts for one country; avoids bulk-downloading the API dataset."""
    response = requests.get(
        f"{API_URL}/codes.alpha_2/{code}",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"response_fields": RESPONSE_FIELDS},
        timeout=15,
    )
    response.raise_for_status()
    objects = response.json().get("data", {}).get("objects", [])
    if not objects:
        raise ValueError(f"REST Countries returned no record for {code}.")
    return parse_country(objects[0])
