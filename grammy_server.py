#!/usr/bin/env python3
"""
Lightweight Flask API to serve Grammy chart payloads in-memory.

Usage:
  - Set Kaggle credentials via env vars: KAGGLE_USERNAME and KAGGLE_KEY (or configure kaggle.json)
  - Install requirements: pip install -r requirements.txt
  - Run: python grammy_server.py

The server will fetch the Kaggle dataset into memory (using kagglehub if available,
or the Kaggle REST API as a fallback), build chart-friendly JSON, and expose
`/api/grammy` for the browser to fetch. No files are written to disk.
"""
import os
import io
import zipfile
import json
from functools import lru_cache
from typing import Any, Dict, List

from flask import Flask, jsonify, make_response
from flask import current_app

import pandas as pd

app = Flask(__name__)


def try_kagglehub_df() -> pd.DataFrame:
    try:
        import kagglehub
        from kagglehub import KaggleDatasetAdapter
        owner_slug = "johnpendenque/grammy-winners-and-nominees-from-1965-to-2024"
        df = kagglehub.load_dataset(KaggleDatasetAdapter.PANDAS, owner_slug, file_path="")
        return df
    except Exception:
        raise


def try_kaggle_zip_in_memory() -> pd.DataFrame:
    import requests
    owner = "johnpendenque"
    slug = "grammy-winners-and-nominees-from-1965-to-2024"
    user = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")
    if not user or not key:
        raise RuntimeError("KAGGLE_USERNAME and KAGGLE_KEY environment variables required for Kaggle REST fallback.")
    url = f"https://www.kaggle.com/api/v1/datasets/download/{owner}/{slug}"
    resp = requests.get(url, auth=(user, key), stream=True, timeout=60)
    resp.raise_for_status()
    bio = io.BytesIO(resp.content)
    z = zipfile.ZipFile(bio)
    csv_name = None
    for name in z.namelist():
        if name.lower().endswith('.csv'):
            csv_name = name
            break
    if not csv_name:
        raise RuntimeError("No CSV inside Kaggle dataset ZIP")
    with z.open(csv_name) as fh:
        return pd.read_csv(io.TextIOWrapper(fh, encoding='utf-8', errors='replace'))


@lru_cache(maxsize=1)
def load_grammy_dataframe() -> pd.DataFrame:
    # Try kagglehub first for convenience, then fallback to REST in-memory ZIP
    try:
        return try_kagglehub_df()
    except Exception:
        return try_kaggle_zip_in_memory()


def build_payload(df: pd.DataFrame) -> Dict[str, Any]:
    # Basic heuristics to find columns
    cols = [c for c in df.columns]
    year_col = next((c for c in cols if 'year' in c.lower() or 'date' in c.lower()), None)
    genre_col = next((c for c in cols if 'genre' in c.lower() or 'category' in c.lower()), None)
    artist_col = next((c for c in cols if 'artist' in c.lower() or 'performer' in c.lower() or 'name' in c.lower()), None)
    winner_col = next((c for c in cols if 'winner' in c.lower() or 'result' in c.lower() or 'won' in c.lower()), None)

    # Polar: genre counts
    gcol = genre_col or genre_col
    if gcol and gcol in df.columns:
        polar_series = df[gcol].fillna('Unknown').astype(str)
    else:
        polar_series = pd.Series(['Unknown'] * len(df))
    polar_counts = polar_series.value_counts().to_dict()
    polar = {"labels": list(polar_counts.keys()), "data": list(polar_counts.values())}

    # Evolution by year x genre
    if year_col and year_col in df.columns:
        try:
            years = pd.to_datetime(df[year_col], errors='coerce').dt.year.fillna(df[year_col]).astype('Int64')
        except Exception:
            years = pd.to_numeric(df[year_col], errors='coerce').astype('Int64')
        df['_GRAMMY_YEAR'] = years
    else:
        df['_GRAMMY_YEAR'] = pd.NA
    gcol = genre_col if genre_col and genre_col in df.columns else (cols[0] if cols else None)
    if gcol:
        pivot = pd.crosstab(df['_GRAMMY_YEAR'], df[gcol].fillna('Unknown').astype(str))
        pivot = pivot.sort_index()
        labels = [str(int(y)) for y in pivot.index if pd.notna(y)]
        datasets = []
        palette = ["#ec4899","#3b82f6","#6366f1","#10b981","#f97316","#a78bfa"]
        for i, g in enumerate(pivot.columns):
            datasets.append({"label": g, "data": [int(x) for x in pivot[g].tolist()], "backgroundColor": palette[i % len(palette)], "borderColor": palette[i % len(palette)]})
        evolution = {"labels": labels, "datasets": datasets}
    else:
        evolution = {"labels": [], "datasets": []}

    # Scatter: win efficiency per artist
    stats = {}
    for _, row in df.iterrows():
        artist = str(row[artist_col]) if artist_col and pd.notna(row.get(artist_col, None)) else 'Unknown'
        rec = stats.setdefault(artist, {"wins": 0, "noms": 0})
        rec['noms'] += 1
        if winner_col and pd.notna(row.get(winner_col, None)):
            v = row[winner_col]
            if isinstance(v, str):
                is_win = 'win' in v.lower() or 'winner' in v.lower() or v.strip().lower() in ('yes','y','true','1')
            else:
                is_win = bool(v)
            if is_win:
                rec['wins'] += 1
    points = []
    for a, st in stats.items():
        noms = st['noms']
        wins = st['wins']
        eff = (wins / noms * 100) if noms else 0.0
        points.append({"artist": a, "x": max(1, noms), "y": round(eff, 2), "r": max(4, min(40, wins*4))})
    scatter = {"datasets": [{"label": "Win Efficiency", "data": points}]}

    # Big4 counts
    big4_keywords = ['record of the year', 'album of the year', 'song of the year', 'best new artist']
    cat_col = next((c for c in cols if 'category' in c.lower() or 'award' in c.lower()), None)
    big4_counts = {}
    if cat_col and artist_col:
        for _, row in df.iterrows():
            cat = str(row.get(cat_col, '')).lower()
            if any(k in cat for k in big4_keywords):
                artist = str(row.get(artist_col, 'Unknown'))
                is_win = False
                if winner_col and pd.notna(row.get(winner_col, None)):
                    v = row[winner_col]
                    if isinstance(v, str):
                        is_win = 'win' in v.lower() or 'winner' in v.lower() or v.strip().lower() in ('yes','y','true','1')
                    else:
                        is_win = bool(v)
                if is_win:
                    big4_counts[artist] = big4_counts.get(artist, 0) + 1
    big4_labels = list(big4_counts.keys())[:12] or ['No Data']
    big4_data = [big4_counts.get(l, 0) for l in big4_labels]

    payload = {
        "polar": polar,
        "evolution": evolution,
        "scatter": scatter,
        "big4": {"labels": big4_labels, "data": big4_data},
        "meta": {"rows": int(len(df)), "columns": cols}
    }
    return payload


@app.route('/api/grammy')
def api_grammy():
    try:
        df = load_grammy_dataframe()
        payload = build_payload(df)
        resp = make_response(jsonify(payload))
        # allow local pages to fetch
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
