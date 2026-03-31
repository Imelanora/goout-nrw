# GoOut NRW

GoOut NRW is a Python command-line application that recommends leisure activities and places in North Rhine-Westphalia (NRW), Germany. The application suggests places based on user preferences such as distance, transport mode and activity categories. Users can browse suggested locations and mark places they find interesting. The idea is conceptually similar to a simple swipe-based recommendation system for discovering nearby activities.

NRW is one of the most densely populated regions in Europe – yet many people don't know what's right on their doorstep. GoOut NRW makes it easy to discover parks, cultural sites, nature spots and more, filtered to what's actually reachable for you today.

---
 
## Research Question
 
> **How can open geodata be used to generate location-based leisure recommendations for NRW?**
 
As a follow-up question: How can a CLI application for personalised leisure planning be implemented using Python and open data?
 
The project explores these questions by combining publicly available datasets from Open Data NRW with geographic distance calculation (Haversine formula) and user-defined filters. The result is a lightweight, offline-capable tool that requires no external APIs or map services to deliver relevant, personalised suggestions.

---

## How it works

The application filters places based on user input (location, distance, category) and calculates distances using the Haversine formula. Travel times are estimated based on the selected transport mode. Results are shuffled within distance bands so that nearby, mid-range and farther places are all represented.

---

## Features

- Discover leisure activities across NRW
- Enter your location via postcode (PLZ) or choose from a city list
- Filter by maximum distance (km), maximum travel time (minutes), or both combined
- Choose transport mode: walking, bike or car
- Select one or multiple activity categories
- Interactively browse suggested places (like / skip)
- Save favourite locations persistently across sessions
- Remove favourites from within the app
- Export favourites as an interactive map (opens in browser)

---

## Example Session

```
╔══════════════════════════════════════════════╗
║  🗺️   GoOut NRW  –  Freizeit entdecken        ║
║       Discover leisure in North Rhine-WP     ║
╚══════════════════════════════════════════════╝

▶ Wie möchtest du deinen Standort angeben? [1/2] (q=beenden): 1
▶ Postleitzahl eingeben (z.B. 47051) (q=beenden): 45127
  ✓ Essen gefunden

   1.  🚶 Zu Fuß   (~5 km/h)
   2.  🚴 Fahrrad  (~15 km/h)
   3.  🚗 Auto     (~50 km/h)

▶ Verkehrsmittel wählen [3]: 3

▶ Filtermodus wählen [1/2/3]: 1
▶ Maximale Entfernung (km) [50]: 30

  ──────────────────────────────────────────────
  [1/12]  Grugapark  🌳
  Ort:         Essen
  Kategorie:   Park
  Entfernung:  2.1 km   🚗 2 min
  ──────────────────────────────────────────────
▶ Aktion [L/s/f/q]: l
  ❤️  Gespeichert!
```

---

## Data Source

The project uses open datasets from [Open Data NRW](https://open.nrw/).

Examples of included data:
- Tourist attractions
- Points of interest
- Leisure activities
- Cultural sites
- Parks and nature locations

The datasets contain information such as place name, category, city and geographic coordinates (latitude, longitude). The data is preprocessed with `scripts/prepare_data.py` and stored locally in JSON format for efficient use within the application.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Imelanora/goout-nrw.git
cd goout-nrw
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pandas folium pytest
```

---

## Preparing the Dataset

Before running the app for the first time, preprocess the raw CSV:

```bash
python scripts/prepare_data.py
```

This reads `data/raw/open_data_nrw.csv`, cleans and validates the data, and writes the result to `data/processed/places.json`.

---

## Usage

Start the application with:

```bash
PYTHONPATH=src python -m goout
```

### Example workflow

1. Enter your location (postcode or city)
2. Choose your transport mode (walking / bike / car)
3. Set your maximum distance or travel time
4. Select activity categories
5. Browse suggested places – press `L` to like, `S` or `Enter` to skip
6. Press `F` at any time to view and manage your favourites
7. At the end of a session, optionally export your favourites as an interactive map

---

## Map Export

After a session, GoOut NRW can generate an interactive HTML map of your saved favourites and open it directly in your browser. The map uses [Folium](https://python-visualization.github.io/folium/) if installed, and falls back to a plain [Leaflet.js](https://leafletjs.com/) HTML file if Folium is not available – so the feature works even without the optional dependency.

---

## Running the Tests

The project includes unit tests for all core modules:

```bash
PYTHONPATH=src pytest tests/ -v
```

| Test file             | What it covers                                              |
|-----------------------|-------------------------------------------------------------|
| `test_distance.py`    | Haversine formula, travel time calculation, time formatting |
| `test_recommender.py` | Place filtering, category selection, shuffle logic          |
| `test_storage.py`     | Add, remove, persist and reload favourites                  |
| `test_transport.py`   | Transport-aware filtering, combined distance/time limits     |

---

## Project Structure

```
goout-nrw/
│
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── open_data_nrw.csv          # original Open Data NRW dataset
│   └── processed/
│       └── places.json                # cleaned, app-ready dataset
│
├── scripts/
│   └── prepare_data.py                # preprocessing pipeline
│
├── src/
│   └── goout/
│       ├── __init__.py
│       ├── __main__.py                # CLI entry point
│       ├── app.py                     # main application logic & UI
│       ├── recommender.py             # filtering and ranking logic
│       ├── distance.py                # Haversine formula & travel time
│       ├── storage.py                 # favourite places persistence
│       ├── map_export.py              # interactive HTML map export
│       └── plz_data.py                # postcode → coordinates lookup
│
└── tests/
    ├── test_distance.py
    ├── test_recommender.py
    ├── test_storage.py
    └── test_transport.py
```

---

## Technologies

- **Python 3.10+**
- **pandas** – data preprocessing and CSV handling
- **folium** – interactive map export (optional)
- **pytest** – unit testing

---

## Limitations

- Travel times are approximations based on average speeds – no real routing or traffic data
- The postcode (PLZ) database covers the main NRW cities and districts; very small municipalities may not be listed
- Dataset is limited to Open Data NRW sources; coverage varies by region
- Map export requires a browser and an internet connection for map tiles (OpenStreetMap)

---

## Author

Melanie Oraca
