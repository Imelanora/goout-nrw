#!/usr/bin/env python3
"""
prepare_data.py

Preprocesses the raw Open Data NRW CSV and writes a clean
places.json used by the GoOut application.

Usage:
    python scripts/prepare_data.py [--input PATH] [--output PATH]
"""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

RAW_CSV     = Path(__file__).parent.parent / "data" / "raw"   / "open_data_nrw.csv"
OUTPUT_JSON = Path(__file__).parent.parent / "data" / "processed" / "places.json"

REQUIRED_COLUMNS = {"name", "category", "city", "latitude", "longitude"}

# NRW bounding box (loose)
LAT_MIN, LAT_MAX =  50.2,  52.7
LON_MIN, LON_MAX =   5.8,   9.6


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare GoOut NRW dataset")
    p.add_argument("--input",  default=str(RAW_CSV),     help="Path to raw CSV")
    p.add_argument("--output", default=str(OUTPUT_JSON), help="Path to output JSON")
    return p.parse_args()


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    print(f"  Loaded {len(df)} rows, columns: {list(df.columns)}")
    return df


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        print(f"[ERROR] Missing columns in CSV: {missing}", file=sys.stderr)
        print(f"        Found columns: {list(df.columns)}", file=sys.stderr)
        sys.exit(1)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)

    # Drop rows missing required fields
    df = df.dropna(subset=list(REQUIRED_COLUMNS))

    # Parse numeric coordinates
    df["latitude"]  = pd.to_numeric(df["latitude"],  errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])

    # Clamp to NRW bounding box
    df = df[
        df["latitude"].between(LAT_MIN, LAT_MAX)
        & df["longitude"].between(LON_MIN, LON_MAX)
    ]

    # Strip whitespace
    df["name"]     = df["name"].str.strip()
    df["city"]     = df["city"].str.strip()
    df["category"] = df["category"].str.strip()

    # Optional description column
    if "description" in df.columns:
        df["description"] = df["description"].fillna("").str.strip()
    else:
        df["description"] = ""

    # Remove exact duplicates on (name, city)
    df = df.drop_duplicates(subset=["name", "city"])
    df = df.reset_index(drop=True)
    df["id"] = (df.index + 1).astype(int)

    after = len(df)
    print(f"  Cleaned: {before} → {after} rows ({before - after} removed)")
    return df


def to_records(df: pd.DataFrame) -> list[dict]:
    cols = ["id", "name", "category", "city", "latitude", "longitude", "description"]
    cols = [c for c in cols if c in df.columns]
    records = df[cols].to_dict(orient="records")
    # Ensure native Python types (not numpy)
    for r in records:
        r["id"]        = int(r["id"])
        r["latitude"]  = float(r["latitude"])
        r["longitude"] = float(r["longitude"])
    return records


def main() -> None:
    args   = parse_args()
    raw    = Path(args.input)
    output = Path(args.output)

    print(f"\nReading  {raw}")
    df = load_csv(raw)
    validate_columns(df)
    df = clean(df)
    records = to_records(df)

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    categories = sorted({r["category"] for r in records})
    print(f"\nWritten  {output}")
    print(f"  {len(records)} places across {len(categories)} categories")
    print(f"  Categories: {', '.join(categories)}\n")


if __name__ == "__main__":
    main()
