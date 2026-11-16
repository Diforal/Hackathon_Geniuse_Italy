import requests
import json


API_URL = "https://api.restcountries.com/countries/v5"
API_KEY = "rc_live_be1ed5c500f54b25b818f0e24cad4dd3"


def get_json(url, key):
    params = {
        "region": "Europe",
        "limit": 50,
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

def parse_country(country):
    pass



raw_countries_info = get_json(API_URL, API_KEY)
with open("raw_country_data.json", 'w', encoding="utf-8") as f:
    json.dump(raw_countries_info, f, ensure_ascii=False, indent=2)
