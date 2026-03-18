from __future__ import annotations
"""
recommender.py

Filters and ranks places based on user preferences.
"""


import json
import random
from pathlib import Path
from typing import Optional

from goout.distance import haversine

DATA_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "places.json"
)


def load_places(path: Path = DATA_PATH) -> list:
    """Load the processed places dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset nicht gefunden: {path}\n"
            "Bitte zuerst ausführen:  python scripts/prepare_data.py"
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_all_categories(places: list) -> list:
    """Return a sorted, deduplicated list of categories."""
    return sorted({p["category"] for p in places})


def filter_places(
    places: list,
    user_lat: float,
    user_lon: float,
    max_distance_km: float,
    categories: Optional[list] = None,
) -> list:
    """
    Return places within *max_distance_km* that belong to one of the
    requested *categories*. Each returned dict gets an extra
    ``distance_km`` field.
    """
    result = []
    for place in places:
        dist = haversine(user_lat, user_lon, place["latitude"], place["longitude"])
        if dist > max_distance_km:
            continue
        if categories and place["category"] not in categories:
            continue
        result.append({**place, "distance_km": round(dist, 1)})

    result.sort(key=lambda p: p["distance_km"])
    return result


def shuffle_recommendations(
    places: list, seed: Optional[int] = None
) -> list:
    """Return a lightly shuffled copy so every session feels fresh."""
    rng = random.Random(seed)
    pivot = max(1, len(places) // 3)
    head  = places[:pivot]
    tail  = list(places[pivot:])
    rng.shuffle(tail)
    return head + tail