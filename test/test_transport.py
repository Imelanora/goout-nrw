"""
tests/test_transport.py
~~~~~~~~~~~~~~~~~~~~~~~
Unit tests for transport-aware travel time logic (distance.py)
and the updated filter_places() in recommender.py.

Run with:
    pytest tests/test_transport.py -v
"""

from __future__ import annotations

import pytest

from goout.distance import (
    SPEEDS_KMH,
    format_travel_time,
    haversine,
    max_travel_time_minutes,
    travel_time_minutes,
)
from goout.recommender import filter_places, shuffle_recommendations


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def sample_places() -> list[dict]:
    """Small synthetic dataset; uses latitude/longitude keys like the real data."""
    return [
        {
            "id": "p1", "name": "Naher Park",
            "city": "Duisburg", "category": "Park",
            "latitude": 51.45, "longitude": 6.78,     # ~1.5 km from origin
        },
        {
            "id": "p2", "name": "Mittleres Museum",
            "city": "Essen", "category": "Kultur",
            "latitude": 51.46, "longitude": 6.95,     # ~12 km from origin
        },
        {
            "id": "p3", "name": "Weiter Freizeitpark",
            "city": "Köln", "category": "Freizeitpark",
            "latitude": 50.93, "longitude": 6.95,     # ~56 km from origin
        },
    ]


# Duisburg city centre as user location
USER_LAT = 51.4344
USER_LON = 6.7623


# ---------------------------------------------------------------------------
# SPEEDS_KMH constants
# ---------------------------------------------------------------------------

class TestSpeedsConstant:
    def test_walking_speed(self):
        assert SPEEDS_KMH["walking"] == 5.0

    def test_bike_speed(self):
        assert SPEEDS_KMH["bike"] == 15.0

    def test_car_speed(self):
        assert SPEEDS_KMH["car"] == 50.0


# ---------------------------------------------------------------------------
# travel_time_minutes
# ---------------------------------------------------------------------------

class TestTravelTimeMinutes:
    def test_car_10km(self):
        assert travel_time_minutes(10, "car") == pytest.approx(12.0)

    def test_bike_15km(self):
        assert travel_time_minutes(15, "bike") == pytest.approx(60.0)

    def test_walking_5km(self):
        assert travel_time_minutes(5, "walking") == pytest.approx(60.0)

    def test_zero_distance(self):
        assert travel_time_minutes(0, "car") == pytest.approx(0.0)

    def test_unknown_transport_falls_back_to_car(self):
        assert travel_time_minutes(50, "hovercraft") == pytest.approx(
            travel_time_minutes(50, "car")
        )

    def test_walking_slower_than_car(self):
        dist = 20.0
        assert travel_time_minutes(dist, "walking") > travel_time_minutes(dist, "car")

    def test_bike_slower_than_car(self):
        dist = 20.0
        assert travel_time_minutes(dist, "bike") > travel_time_minutes(dist, "car")


# ---------------------------------------------------------------------------
# max_travel_time_minutes
# ---------------------------------------------------------------------------

class TestMaxTravelTimeMinutes:
    def test_equals_travel_time_minutes_car(self):
        assert max_travel_time_minutes(30, "car") == pytest.approx(
            travel_time_minutes(30, "car")
        )

    def test_equals_travel_time_minutes_walking(self):
        assert max_travel_time_minutes(5, "walking") == pytest.approx(
            travel_time_minutes(5, "walking")
        )


# ---------------------------------------------------------------------------
# format_travel_time
# ---------------------------------------------------------------------------

class TestFormatTravelTime:
    @pytest.mark.parametrize("minutes, expected", [
        (0,   "0 min"),
        (1,   "1 min"),
        (59,  "59 min"),
        (60,  "1 h"),
        (90,  "1 h 30 min"),
        (120, "2 h"),
        (135, "2 h 15 min"),
    ])
    def test_format(self, minutes, expected):
        assert format_travel_time(minutes) == expected


# ---------------------------------------------------------------------------
# haversine (sanity checks)
# ---------------------------------------------------------------------------

class TestHaversine:
    def test_zero_distance(self):
        assert haversine(51.0, 7.0, 51.0, 7.0) == pytest.approx(0.0, abs=1e-6)

    def test_duisburg_koeln(self):
        # ~55–60 km as the crow flies
        d = haversine(51.4344, 6.7623, 50.9333, 6.9500)
        assert 50 < d < 65

    def test_symmetry(self):
        a = haversine(51.4344, 6.7623, 51.9625, 7.6253)
        b = haversine(51.9625, 7.6253, 51.4344, 6.7623)
        assert a == pytest.approx(b)


# ---------------------------------------------------------------------------
# filter_places
# ---------------------------------------------------------------------------

class TestFilterPlaces:
    ALL_CATS = ["Park", "Kultur", "Freizeitpark"]

    def test_max_km_excludes_far_places(self, sample_places):
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=20, categories=self.ALL_CATS, transport="car",
        )
        names = [p["name"] for p in result]
        assert "Naher Park" in names
        assert "Mittleres Museum" in names
        assert "Weiter Freizeitpark" not in names

    def test_max_minutes_walking_excludes_distant_places(self, sample_places):
        # Walking to Cologne (>56 km) would take >670 min
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=self.ALL_CATS,
            transport="walking", max_minutes=60,
        )
        names = [p["name"] for p in result]
        assert "Weiter Freizeitpark" not in names

    def test_car_includes_more_than_walking_for_same_time(self, sample_places):
        car_result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=self.ALL_CATS,
            transport="car", max_minutes=60,
        )
        walk_result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=self.ALL_CATS,
            transport="walking", max_minutes=60,
        )
        assert len(car_result) >= len(walk_result)

    def test_both_constraints_combined(self, sample_places):
        # max_km=20 AND max_minutes=5 → only the nearest place qualifies
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=20, categories=self.ALL_CATS,
            transport="car", max_minutes=5,
        )
        names = [p["name"] for p in result]
        assert "Naher Park" in names
        assert "Mittleres Museum" not in names

    def test_category_filter(self, sample_places):
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=["Park"], transport="car",
        )
        assert all(p["category"] == "Park" for p in result)

    def test_results_sorted_by_travel_time(self, sample_places):
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=self.ALL_CATS, transport="car",
        )
        times = [p["travel_minutes"] for p in result]
        assert times == sorted(times)

    def test_travel_minutes_annotated(self, sample_places):
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=self.ALL_CATS, transport="car",
        )
        for place in result:
            assert "travel_minutes" in place
            assert "distance_km" in place
            assert place["travel_minutes"] >= 0

    def test_no_results_returns_empty_list(self, sample_places):
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=0.1, categories=self.ALL_CATS, transport="car",
        )
        assert result == []

    def test_none_constraints_returns_all_categories(self, sample_places):
        result = filter_places(
            sample_places, USER_LAT, USER_LON,
            max_distance_km=None, categories=self.ALL_CATS, transport="car",
        )
        assert len(result) == len(sample_places)


# ---------------------------------------------------------------------------
# shuffle_recommendations
# ---------------------------------------------------------------------------

class TestShuffleRecommendations:
    def test_same_length(self, sample_places):
        assert len(shuffle_recommendations(sample_places)) == len(sample_places)

    def test_same_elements(self, sample_places):
        shuffled = shuffle_recommendations(sample_places)
        assert {p["id"] for p in shuffled} == {p["id"] for p in sample_places}

    def test_empty_input(self):
        assert shuffle_recommendations([]) == []

    def test_single_element(self):
        places = [{"id": "x", "travel_minutes": 10}]
        assert shuffle_recommendations(places) == places

    def test_seed_is_reproducible(self, sample_places):
        a = shuffle_recommendations(sample_places * 4, seed=42)
        b = shuffle_recommendations(sample_places * 4, seed=42)
        assert [p["id"] for p in a] == [p["id"] for p in b]