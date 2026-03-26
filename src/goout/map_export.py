from __future__ import annotations
"""
Generates an interactive HTML map of liked places.
Uses folium if installed, otherwise falls back to plain Leaflet.js HTML.
"""

from pathlib import Path

OUTPUT_PATH = Path.home() / "goout_favorites_map.html"


def _make_folium_map(places: list, output: Path) -> None:
    import folium

    center_lat = sum(p["latitude"] for p in places) / len(places)
    center_lon = sum(p["longitude"] for p in places) / len(places)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=9)

    colors = {
        "Kultur": "red", "Natur": "green", "Park": "darkgreen",
        "Freizeitpark": "orange", "Radweg": "blue",
        "Tiere": "purple", "Shopping": "pink", "Wellness": "cadetblue",
    }

    for place in places:
        color = colors.get(place["category"], "gray")
        desc = place.get("description", "")
        popup_html = (
            f"<b>{place['name']}</b><br>"
            f"📍 {place['city']}<br>"
            f"🏷️ {place['category']}<br>"
            f"📏 {place.get('distance_km', '?')} km"
            + (f"<br>{desc}" if desc else "")
        )
        folium.Marker(
            location=[place["latitude"], place["longitude"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=place["name"],
            icon=folium.Icon(color=color, icon="info-sign"),
        ).add_to(m)

    m.save(str(output))


def _make_leaflet_map(places: list, output: Path) -> None:
    if places:
        center_lat = sum(p["latitude"] for p in places) / len(places)
        center_lon = sum(p["longitude"] for p in places) / len(places)
    else:
        center_lat, center_lon = 51.4, 7.0

    markers = []
    for p in places:
        name = p["name"].replace("'", "\\'")
        city = p["city"].replace("'", "\\'")
        cat  = p["category"].replace("'", "\\'")
        dist = p.get("distance_km", "?")
        desc = p.get("description", "").replace("'", "\\'")
        popup = f"<b>{name}</b><br>{city} · {cat}<br>{dist} km"
        if desc:
            popup += f"<br>{desc}"
        markers.append(
            f"L.marker([{p['latitude']}, {p['longitude']}])"
            f".addTo(map).bindPopup('{popup}').bindTooltip('{name}');"
        )

    markers_js = "\n    ".join(markers)

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>GoOut NRW – Meine Favoriten</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    body {{ margin: 0; font-family: sans-serif; }}
    #map {{ height: 100vh; width: 100%; }}
    #title {{
      position: absolute; top: 10px; left: 50%;
      transform: translateX(-50%);
      background: white; padding: 8px 20px;
      border-radius: 20px; font-weight: bold;
      box-shadow: 0 2px 8px rgba(0,0,0,0.25);
      z-index: 1000; font-size: 15px; white-space: nowrap;
    }}
  </style>
</head>
<body>
  <div id="title">🗺️ GoOut NRW &ndash; {len(places)} Favoriten</div>
  <div id="map"></div>
  <script>
    var map = L.map('map').setView([{center_lat}, {center_lon}], 9);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);
    {markers_js}
  </script>
</body>
</html>"""

    output.write_text(html, encoding="utf-8")


def export_map(places: list, output: Path = OUTPUT_PATH) -> Path:
    try:
        _make_folium_map(places, output)
    except ImportError:
        _make_leaflet_map(places, output)
    return output
