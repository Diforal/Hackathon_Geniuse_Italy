from collections import defaultdict
import csv


NAME_ALIASES = {
    "Slovenian": "Slovene",
    "Norwegian Nynorsk": "Norwegian",
}


def load_language_groups(csv_path: str = "europe_languages.csv"):
  groups = defaultdict(list)

  with open(csv_path, mode="r", encoding="utf-8") as file:
    for row in csv.DictReader(file):
      groups[row["branch"]].append(row["name"])

  return dict(groups)


def check_exact_language(secret_country: dict, guess_country: dict) -> bool:
  s_lang = NAME_ALIASES.get(
      secret_country["languages"], secret_country["languages"]
  )
  g_lang = NAME_ALIASES.get(
      guess_country["languages"], guess_country["languages"]
  )
  return s_lang == g_lang


def check_language_group(
    secret_country: dict, guess_country: dict, language_groups: dict
):
  s_lang = NAME_ALIASES.get(
      secret_country["languages"], secret_country["languages"]
  )
  g_lang = NAME_ALIASES.get(
      guess_country["languages"], guess_country["languages"]
  )

  for group, langs in language_groups.items():
    if s_lang in langs and g_lang in langs:
      return True, group

  return False, None