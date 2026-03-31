from __future__ import annotations
"""
recommender.py

Filters and ranks places based on user preferences.
"""


import json
import random
from pathlib import Path
from typing import Optional

from goout.distance import haversine, travel_time_minutes

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
    max_distance_km: Optional[float],
    categories: Optional[list] = None,
    transport: str = "car",
    max_minutes: Optional[float] = None,
) -> list:
    """
    Return places within *max_distance_km* that belong to one of the
    requested *categories*. Each returned dict gets an extra
    ``distance_km`` field.
    """
    result = []
    for place in places:
        if categories and place["category"] not in categories:
            continue

        dist = haversine(user_lat, user_lon, place["latitude"], place["longitude"])
        if max_distance_km is not None and dist > max_distance_km:
            continue

        mins = travel_time_minutes(dist, transport)
 
        if max_minutes is not None and mins > max_minutes:
            continue

        result.append({
            **place,
            "distance_km":    round(dist, 1),
            "travel_minutes": round(mins, 1),
        })

    result.sort(key=lambda p: p["travel_minutes"])
    return result


def shuffle_recommendations(
    places: list, seed: Optional[int] = None
) -> list:
    if len(places) < 4:
        shuffled = list(places)
        random.Random(seed).shuffle(shuffled)
        return shuffled
    
    rng   = random.Random(seed)
    third = len(places) // 3
    near, mid, far = places[:third], places[third:2 * third], places[2 * third:]
    for bucket in (near, mid, far):
        rng.shuffle(bucket)
    return near + mid + far