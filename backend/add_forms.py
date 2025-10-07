import pandas as pd
import requests
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "pokemon.xlsx"
SHEET = "pokemon"
POKEAPI = "https://pokeapi.co/api/v2/pokemon/{}"

# Base-Dex → Region (for non-regional forms)
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

def region_from_slug(base_id: int, slug: str) -> str:
    s = slug.lower()
    if "alola" in s:  return "Alola"
    if "galar" in s:  return "Galar"
    if "hisui" in s:  return "Hisui"
    if "paldea" in s: return "Paldea"
    # Megas keep base region
    return region_for_id(base_id)

# Forms to add (you can extend this list any time)
FORMS = [
    # Charizard
    {"id": 6,  "name": "Charizard", "slug": "charizard-mega-x"},
    {"id": 6,  "name": "Charizard", "slug": "charizard-mega-y"},
    # Raichu
    {"id": 26, "name": "Raichu",    "slug": "raichu-alola"},
    # Meowth examples (both regions)
    {"id": 52, "name": "Meowth",    "slug": "meowth-alola"},
    {"id": 52, "name": "Meowth",    "slug": "meowth-galar"},
    # Add more here, e.g. {"id": ???, "name":"???", "slug":"pikachu-rock-star"}
]

def fetch_types_abilities(slug: str):
    r = requests.get(POKEAPI.format(slug), timeout=20)
    r.raise_for_status()
    js = r.json()
    types = [t["type"]["name"].replace("-", " ").title() for t in js.get("types", [])]
    abilities = [a["ability"]["name"].replace("-", " ").title() for a in js.get("abilities", [])]
    return types, abilities

def main():
    # Load current sheet
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET)
    cols = df.columns.str.lower().tolist()

    # Ensure required columns exist
    if "slug" not in cols:
        df["slug"] = ""
    if "types" not in cols:
        df["types"] = ""
    if "abilities" not in cols:
        df["abilities"] = ""
    if "region" not in cols:
        df["region"] = "Unknown"

    # Normalize
    df["slug"] = df["slug"].fillna("").astype(str)
    existing_slugs = set(s.lower() for s in df["slug"].tolist() if isinstance(s, str))

    new_rows = []
    for item in FORMS:
        slug = item["slug"].lower()
        if slug in existing_slugs:
            print(f"skip (exists): {slug}")
            continue
        try:
            types, abilities = fetch_types_abilities(slug)
            region = region_from_slug(item["id"], slug)
            new_rows.append({
                "id": int(item["id"]),
                "name": item["name"],
                "types": ",".join(types),
                "abilities": ",".join(abilities),
                "region": region,
                "slug": slug
            })
            print(f"add: {slug}  types={types}  abilities={abilities}  region={region}")
        except Exception as e:
            print(f"fail: {slug} -> {e}")

    if not new_rows:
        print("No new forms to add.")
        return

    df_out = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    # Write back
    with pd.ExcelWriter(DATA_PATH, engine="openpyxl", mode="w") as xw:
        df_out.to_excel(xw, index=False, sheet_name=SHEET)

    print(f"Wrote {len(new_rows)} new form rows. Total rows: {len(df_out)}")

if __name__ == "__main__":
    main()
