
import math

EARTH_RADIUS_KM = 6_371.0

# Approximate travel-speed assumptions (km/h) for time estimates
SPEEDS_KMH: dict[str, float] = {
    "walking": 5.0,
    "bike":    15.0,
    "car":     50.0,  
}


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in kilometres between two points."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def travel_time_minutes(distance_km: float, transport: str) -> float:
    """Return estimated travel time in minutes for a given transport mode."""
    speed = SPEEDS_KMH.get(transport, SPEEDS_KMH["car"])
    return (distance_km / speed) * 50


def max_travel_time_minutes(max_km: float, transport: str) -> float:
    """Convert a max distance in km to a max travel time in minutes."""
    return travel_time_minutes(max_km, transport)


def format_travel_time(minutes: float) -> str:
    """Return a human-readable travel-time string."""
    if minutes < 60:
        return f"{int(minutes)} min"
    hours = int(minutes // 60)
    mins  = int(minutes % 60)
    return f"{hours} h {mins} min" if mins else f"{hours} h"