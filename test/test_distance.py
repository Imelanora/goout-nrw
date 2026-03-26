"""
test_distance.py

Unit tests for distance.py
"""

import pytest
from goout.distance import haversine, travel_time_minutes, format_travel_time


class TestHaversine:
    def test_same_location_returns_zero(self):
        assert haversine(51.45, 7.01, 51.45, 7.01) == 0.0

    def test_essen_to_dortmund(self):
        # Known distance ~35 km
        dist = haversine(51.4508, 7.0131, 51.5136, 7.4653)
        assert 30 < dist < 40

    def test_duisburg_to_koeln(self):
        # Known distance ~55 km
        dist = haversine(51.4344, 6.7623, 50.9333, 6.9500)
        assert 50 < dist < 65

    def test_symmetry(self):
        d1 = haversine(51.45, 7.01, 51.51, 7.47)
        d2 = haversine(51.51, 7.47, 51.45, 7.01)
        assert abs(d1 - d2) < 0.001

    def test_returns_float(self):
        result = haversine(51.0, 7.0, 52.0, 8.0)
        assert isinstance(result, float)


class TestTravelTime:
    def test_walking_10km(self):
        minutes = travel_time_minutes(10.0, "walking")
        assert minutes == pytest.approx(120.0)

    def test_bike_15km(self):
        minutes = travel_time_minutes(15.0, "bike")
        assert minutes == pytest.approx(60.0)

    def test_car_60km(self):
        minutes = travel_time_minutes(60.0, "car")
        assert minutes == pytest.approx(60.0)

    def test_unknown_transport_defaults_to_car(self):
        minutes = travel_time_minutes(60.0, "rocket")
        assert minutes == pytest.approx(60.0)

    def test_zero_distance(self):
        assert travel_time_minutes(0.0, "car") == 0.0


class TestFormatTravelTime:
    def test_under_60_minutes(self):
        assert format_travel_time(45) == "45 min"

    def test_exactly_60_minutes(self):
        assert format_travel_time(60) == "1 h"

    def test_90_minutes(self):
        assert format_travel_time(90) == "1 h 30 min"

    def test_120_minutes(self):
        assert format_travel_time(120) == "2 h"

    def test_zero_minutes(self):
        assert format_travel_time(0) == "0 min"
