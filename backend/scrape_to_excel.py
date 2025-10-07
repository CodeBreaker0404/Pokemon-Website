import time
import requests
import pandas as pd
from pathlib import Path

OUT_PATH = Path(__file__).parent / "data" / "pokemon.xlsx"
SHEET = "pokemon"
LIST_URL = "https://pokemondb.net/pokedex/all"
POKEAPI = "https://pokeapi.co/api/v2/pokemon/{id}"  # 1..1025+

# Dex → region
def region_for_id(n: int) -> str:
    if   1 <= n <= 151:   return "Kanto"
    if 152 <= n <= 251:   return "Johto"
    if 252 <= n <= 386:   return "Hoenn"
    if 387 <= n <= 493:   return "Sinnoh"
    if 494 <= n <= 649:   return "Unova"
    if 650 <= n <= 721:   return "Kalos"
    if 722 <= n <= 809:   return "Alola"
    if 810 <= n <= 898:   return "Galar"
    if 899 <= n <= 905:   return "Hisui"
    if 906 <= n <= 1025:  return "Paldea"
    return "Unknown"

def fetch_abilities(pid: int) -> str:
    """Return comma-separated ability names for a given Pokédex id."""
    try:
        r = requests.get(POKEAPI.format(id=pid), timeout=20)
        r.raise_for_status()
        js = r.json()
        # abilities is a list of {"ability":{"name":...},"is_hidden":...}
        names = [a["ability"]["name"].replace("-", " ").title() for a in js.get("abilities", [])]
        return ",".join(names)
    except Exception:
        return ""  # fallback empty if not found / out of range

def main():
    # 1) scrape base table (id, name, types)
    html = requests.get(LIST_URL, timeout=30).text
    df = pd.read_html(html)[0].rename(columns={"#": "id", "Name": "name", "Type": "types"})
    df = df[["id", "name", "types"]].copy()
    df["types"] = df["types"].astype(str).str.replace(r"\s+", ",", regex=True)
    df["region"] = df["id"].apply(region_for_id)

    # 2) enrich abilities from PokeAPI (rate-limit friendly)
    abilities = []
    for i, pid in enumerate(df["id"].astype(int).tolist(), start=1):
        abilities.append(fetch_abilities(pid))
        # simple throttle to be nice to the API (adjust if needed)
        if i % 50 == 0:
            print(f"fetched abilities for {i} Pokémon...")
            time.sleep(1)  # brief pause

    df["abilities"] = abilities

    # 3) reorder to our schema and write Excel
    df = df[["id", "name", "types", "abilities", "region"]]
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUT_PATH, engine="openpyxl", mode="w") as xw:
        df.to_excel(xw, index=False, sheet_name=SHEET)

    print(f"Wrote {len(df)} rows with abilities → {OUT_PATH}")

if __name__ == "__main__":
    main()
