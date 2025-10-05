# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from pathlib import Path
import pandas as pd

app = Flask(__name__)
CORS(app)

DATA_PATH = Path(__file__).parent / "data" / "pokemon.xlsx"

def safe_load():
    info = {
        "data_path": str(DATA_PATH),
        "exists": DATA_PATH.exists(),
        "sheet": "pokemon",
        "error": "",
        "rows": 0,
        "columns": [],
    }
    df = pd.DataFrame()
    try:
        if info["exists"]:
            # list sheets for debug
            try:
                xls = pd.ExcelFile(DATA_PATH)
                info["sheets_found"] = xls.sheet_names
            except Exception as e:
                info["sheets_found"] = []
                info["excelfile_error"] = str(e)

            df = pd.read_excel(DATA_PATH, sheet_name="pokemon")
            info["rows"] = len(df)
            info["columns"] = list(df.columns)
        else:
            info["error"] = "File not found"
    except Exception as e:
        info["error"] = str(e)
    return df, info

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    # ensure expected columns exist
    for col in ["id", "name", "types", "abilities", "region", "slug", "form_poke_id"]:
        if col not in df.columns:
            df[col] = pd.NA
    # types/abilities -> arrays
    df["types"] = df["types"].fillna("").apply(lambda s: [t.strip() for t in str(s).split(",") if t.strip()])
    df["abilities"] = df["abilities"].fillna("").apply(lambda s: [a.strip() for a in str(s).split(",") if a.strip()])
    df["region"] = df["region"].fillna("Unknown")
    df["slug"] = df["slug"].fillna("").astype(str)
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df["form_poke_id"] = pd.to_numeric(df["form_poke_id"], errors="coerce")
    df = df[df["id"].notna()]  # drop bad rows
    return df

def sprite_url(row) -> str:
    pid = int(row["form_poke_id"]) if pd.notna(row["form_poke_id"]) else int(row["id"])
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pid}.png"

# Load once at boot (with debug info)
DF_RAW, LOAD_INFO = safe_load()
DF = normalize(DF_RAW) if not LOAD_INFO.get("error") else pd.DataFrame()

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/pokemon")
def get_pokemon():
    if DF.empty:
        # Helpful message if we couldn't load data
        return jsonify({
            "error": "No data loaded",
            "why": LOAD_INFO,
            "hint": "Check `backend/data/pokemon.xlsx` exists and has a sheet named 'pokemon' with columns: id,name,types,abilities,region[,slug,form_poke_id]."
        }), 500
    items = []
    for _, r in DF.iterrows():
        items.append({
            "id": int(r["id"]),
            "name": r["name"],
            "types": r["types"],
            "abilities": r["abilities"],
            "region": r["region"],
            "slug": r["slug"],
            "sprite": sprite_url(r),
        })
    return jsonify(items)

# Debug endpoints
@app.get("/api/debug/meta")
def debug_meta():
    return jsonify(LOAD_INFO)

@app.get("/api/debug/sample")
def debug_sample():
    return jsonify(DF_RAW.head(5).to_dict(orient="records"))

if __name__ == "__main__":
    # Run: python app.py  (make sure venv has pandas + openpyxl)
    app.run(host="127.0.0.1", port=5000, debug=True)

# Update: refined comments on 2025-10-05
