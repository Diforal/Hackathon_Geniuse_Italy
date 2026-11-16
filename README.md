# KrainaLe

A Streamlit country guessing game. The available countries come from `data/most-visited-countries-2026.csv`; REST Countries supplies the target and guess facts on demand.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The existing API key has been moved to `.streamlit/secrets.toml`, which is ignored by Git. If you set up another machine, create that file with:

```toml
RESTCOUNTRIES_API_KEY = "your-key-here"
```

For Streamlit Community Cloud, add the same setting under the app's **Settings → Secrets**.

## Game flow

The app randomly chooses a target from the CSV countries. Players get up to 10 guesses. After a wrong guess, the app compares population and land area with a 10% tolerance and gives region, subregion, and sea-access feedback. Additional hints may unlock after guesses 5, 7, and 9. Duplicate guesses are rejected without using an attempt.
