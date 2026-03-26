"""
test_recommender.py

Unit tests for recommender.py
"""

import pytest
from goout.recommender import filter_places, get_all_categories, shuffle_recommendations

SAMPLE_PLACES = [
    {"id": 1, "name": "Kölner Dom",    "category": "Kultur", "city": "Köln",    "latitude": 50.9413, "longitude": 6.9583, "description": ""},
    {"id": 2, "name": "Baldeneysee",   "category": "Natur",  "city": "Essen",   "latitude": 51.3950, "longitude": 7.0233, "description": ""},
    {"id": 3, "name": "Grugapark",     "category": "Park",   "city": "Essen",   "latitude": 51.4289, "longitude": 6.9983, "description": ""},
    {"id": 4, "name": "Phantasialand", "category": "Freizeitpark", "city": "Brühl", "latitude": 50.7986, "longitude": 6.8797, "description": ""},
    {"id": 5, "name": "Zoo Köln",      "category": "Tiere",  "city": "Köln",    "latitude": 50.9594, "longitude": 6.9736, "description": ""},
]

# Essen coordinates as user location
USER_LAT, USER_LON = 51.4508, 7.0131


class TestFilterPlaces:
    def test_returns_places_within_distance(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 20)
        names = [p["name"] for p in result]
        assert "Baldeneysee" in names
        assert "Grugapark" in names

    def test_excludes_places_outside_distance(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 10)
        names = [p["name"] for p in result]
        assert "Kölner Dom" not in names
        assert "Phantasialand" not in names

    def test_filters_by_category(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 200, ["Natur"])
        assert all(p["category"] == "Natur" for p in result)

    def test_multiple_categories(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 200, ["Natur", "Park"])
        categories = {p["category"] for p in result}
        assert categories == {"Natur", "Park"}

    def test_no_category_filter_returns_all(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 999)
        assert len(result) == len(SAMPLE_PLACES)

    def test_results_sorted_by_distance(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 999)
        distances = [p["distance_km"] for p in result]
        assert distances == sorted(distances)

    def test_distance_km_field_added(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 999)
        assert all("distance_km" in p for p in result)

    def test_empty_input_returns_empty(self):
        result = filter_places([], USER_LAT, USER_LON, 100)
        assert result == []

    def test_no_places_in_range_returns_empty(self):
        result = filter_places(SAMPLE_PLACES, USER_LAT, USER_LON, 1)
        assert result == []


class TestGetAllCategories:
    def test_returns_sorted_unique_categories(self):
        cats = get_all_categories(SAMPLE_PLACES)
        assert cats == sorted(set(p["category"] for p in SAMPLE_PLACES))

    def test_no_duplicates(self):
        cats = get_all_categories(SAMPLE_PLACES)
        assert len(cats) == len(set(cats))

    def test_empty_list(self):
        assert get_all_categories([]) == []


class TestShuffleRecommendations:
    def test_returns_same_length(self):
        result = shuffle_recommendations(SAMPLE_PLACES)
        assert len(result) == len(SAMPLE_PLACES)

    def test_same_seed_same_result(self):
        r1 = shuffle_recommendations(SAMPLE_PLACES, seed=42)
        r2 = shuffle_recommendations(SAMPLE_PLACES, seed=42)
        assert [p["id"] for p in r1] == [p["id"] for p in r2]

    def test_contains_all_places(self):
        result = shuffle_recommendations(SAMPLE_PLACES)
        ids_in = {p["id"] for p in result}
        ids_orig = {p["id"] for p in SAMPLE_PLACES}
        assert ids_in == ids_orig
