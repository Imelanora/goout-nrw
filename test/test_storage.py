"""
test_storage.py

Unit tests for storage.py
"""

import json
import tempfile
from pathlib import Path

import pytest
from goout.storage import FavoritesStorage

PLACE_1 = {"id": 1, "name": "Kölner Dom",  "category": "Kultur", "city": "Köln",  "latitude": 50.94, "longitude": 6.96, "distance_km": 10.0, "description": ""}
PLACE_2 = {"id": 2, "name": "Baldeneysee", "category": "Natur",  "city": "Essen", "latitude": 51.40, "longitude": 7.02, "distance_km": 5.0,  "description": ""}
PLACE_3 = {"id": 3, "name": "Grugapark",   "category": "Park",   "city": "Essen", "latitude": 51.43, "longitude": 6.99, "distance_km": 3.0,  "description": ""}


@pytest.fixture
def storage(tmp_path):
    """Provide a fresh FavoritesStorage backed by a temp file."""
    return FavoritesStorage(tmp_path / "test_favorites.json")


class TestAdd:
    def test_add_single_place(self, storage):
        storage.add(PLACE_1)
        assert storage.count() == 1

    def test_add_multiple_places(self, storage):
        storage.add(PLACE_1)
        storage.add(PLACE_2)
        assert storage.count() == 2

    def test_add_duplicate_ignored(self, storage):
        storage.add(PLACE_1)
        storage.add(PLACE_1)
        assert storage.count() == 1

    def test_add_persists_to_file(self, tmp_path):
        path = tmp_path / "favs.json"
        storage = FavoritesStorage(path)
        storage.add(PLACE_1)
        assert path.exists()
        data = json.loads(path.read_text())
        assert len(data) == 1


class TestRemove:
    def test_remove_existing_place(self, storage):
        storage.add(PLACE_1)
        result = storage.remove(PLACE_1["id"])
        assert result is True
        assert storage.count() == 0

    def test_remove_nonexistent_returns_false(self, storage):
        result = storage.remove(999)
        assert result is False

    def test_remove_correct_place(self, storage):
        storage.add(PLACE_1)
        storage.add(PLACE_2)
        storage.remove(PLACE_1["id"])
        assert storage.contains(PLACE_1["id"]) is False
        assert storage.contains(PLACE_2["id"]) is True


class TestContains:
    def test_contains_added_place(self, storage):
        storage.add(PLACE_1)
        assert storage.contains(PLACE_1["id"]) is True

    def test_not_contains_missing_place(self, storage):
        assert storage.contains(999) is False

    def test_not_contains_after_remove(self, storage):
        storage.add(PLACE_1)
        storage.remove(PLACE_1["id"])
        assert storage.contains(PLACE_1["id"]) is False


class TestAll:
    def test_all_returns_list(self, storage):
        assert isinstance(storage.all(), list)

    def test_all_returns_added_places(self, storage):
        storage.add(PLACE_1)
        storage.add(PLACE_2)
        ids = {p["id"] for p in storage.all()}
        assert ids == {PLACE_1["id"], PLACE_2["id"]}


class TestCount:
    def test_count_empty(self, storage):
        assert storage.count() == 0

    def test_count_after_add(self, storage):
        storage.add(PLACE_1)
        storage.add(PLACE_2)
        assert storage.count() == 2


class TestPersistence:
    def test_data_survives_reload(self, tmp_path):
        path = tmp_path / "favs.json"
        s1 = FavoritesStorage(path)
        s1.add(PLACE_1)
        s1.add(PLACE_2)

        s2 = FavoritesStorage(path)
        assert s2.count() == 2
        assert s2.contains(PLACE_1["id"])
        assert s2.contains(PLACE_2["id"])

    def test_clear_removes_all(self, storage):
        storage.add(PLACE_1)
        storage.add(PLACE_2)
        storage.clear()
        assert storage.count() == 0
