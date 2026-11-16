import requests
import json


API_URL = "https://api.restcountries.com/countries/v5"
API_KEY = "rc_live_be1ed5c500f54b25b818f0e24cad4dd3"


def get_json(url, key):
    params = {
        "region": "Europe",
        "limit": 54,
        'response_fields': ",".join([
        "names.common",
        "subregion",
        "population",
        "area.kilometers",
        "landlocked",
        "languages"]),
    }
    headers = {f"Authorization": f"Bearer {key}"}
    response = requests.get(url, headers=headers, params=params)
    countries_data = response.json()
    return  countries_data



def get_languages(country):
    languages = []
    for lang in country["languages"]:
        languages.append(lang["name"])
    return languages
def parse_country(country):
    parsed_country = {
        "name": country["names"]["common"],
        "subregion": country["subregion"],
        "population": country["population"],
        "area": {"kilometers": country["area"]["kilometers"]},
        "landlocked": country["landlocked"],
        "languages": get_languages(country),
    }
    return parsed_country

def parse_all(data):
    countries = []
    for country in data["data"]["objects"]:
        countries.append(parse_country(country))
    return countries



raw_countries_info = get_json(API_URL, API_KEY)
edited_countries_info = parse_all(raw_countries_info)
with open("edited_country_data.json", 'w', encoding="utf-8") as f:
    json.dump(edited_countries_info, f, ensure_ascii=False, indent=2)
with open("raw_country_data.json", 'w', encoding="utf-8") as f:
    json.dump(raw_countries_info, f, ensure_ascii=False, indent=2)

