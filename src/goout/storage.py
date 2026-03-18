from __future__ import annotations
"""
storage.py

Handles persistence of user favourites to a local JSON file.
"""

import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".goout_favorites.json"


class FavoritesStorage:
    """Load and save the user's liked places."""

    def __init__(self, path: Path = DEFAULT_PATH) -> None:
        self.path = path
        self._data: list[dict] = self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, place: dict) -> None:
        """Add a place to favourites (deduplicated by id)."""
        ids = {p["id"] for p in self._data}
        if place["id"] not in ids:
            self._data.append(place)
            self._save()

    def remove(self, place_id: int) -> bool:
        """Remove a place by id. Returns True if it was present."""
        before = len(self._data)
        self._data = [p for p in self._data if p["id"] != place_id]
        if len(self._data) < before:
            self._save()
            return True
        return False

    def all(self) -> list[dict]:
        return list(self._data)

    def count(self) -> int:
        return len(self._data)

    def contains(self, place_id: int) -> bool:
        return any(p["id"] == place_id for p in self._data)

    def clear(self) -> None:
        """Remove all favourites."""
        self._data = []
        self._save()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self) -> list[dict]:
        if self.path.exists():
            try:
                with open(self.path, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)