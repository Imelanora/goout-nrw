from __future__ import annotations

import sys

from goout.plz_data import lookup_plz
from goout.distance import format_travel_time, travel_time_minutes
from goout.recommender import (
    filter_places,
    get_all_categories,
    load_places,
    shuffle_recommendations,
)
from goout.storage import FavoritesStorage


RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"


def c(text: str, colour: str) -> str:
    return f"{colour}{text}{RESET}"


def bold(text: str) -> str:
    return f"{BOLD}{text}{RESET}"


# Banner

BANNER = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════╗
║  🗺️   GoOut NRW  –  Freizeit entdecken       ║
║       Discover leisure in North Rhine-WP     ║
╚══════════════════════════════════════════════╝{RESET}
"""

TRANSPORT_EMOJI = {"walking": "🚶", "bike": "🚴", "car": "🚗"}
CATEGORY_EMOJI = {
    "Kultur":       "🏛️",
    "Natur":        "🌿",
    "Park":         "🌳",
    "Freizeitpark": "🎢",
    "Radweg":       "🚴",
    "Tiere":        "🦁",
    "Shopping":     "🛍️",
    "Wellness":     "🧖",
}


def cat_icon(category: str) -> str:
    return CATEGORY_EMOJI.get(category, "📍")


# Input helpers

def prompt(msg: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{CYAN}▶{RESET} {msg}{suffix}: ").strip()
        return value if value else default
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def prompt_int(msg: str, default: int, min_val: int = 1, max_val: int = 9999) -> int:
    while True:
        raw = prompt(msg, str(default))
        try:
            val = int(raw)
            if min_val <= val <= max_val:
                return val
            print(c(f"  Bitte eine Zahl zwischen {min_val} und {max_val} eingeben.", YELLOW))
        except ValueError:
            print(c("  Ungültige Eingabe – bitte eine ganze Zahl eingeben.", YELLOW))


def prompt_float(msg: str, default: float) -> float:
    while True:
        raw = prompt(msg, str(default))
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print(c("  Ungültige Eingabe – bitte eine Dezimalzahl eingeben.", YELLOW))


def choose_from_list(
    options: list[str],
    msg: str,
    multi: bool = False,
    default_all: bool = False,
) -> list[str]:
    """
    Display a numbered list and let the user pick one or more entries.
    Returns the selected values.
    """
    print()
    for i, opt in enumerate(options, start=1):
        icon = cat_icon(opt)
        print(f"  {DIM}{i:>2}.{RESET}  {icon}  {opt}")
    print()

    if multi:
        raw = prompt(msg, "alle" if default_all else "")
        if not raw or raw.lower() in ("alle", "all", "a"):
            return list(options)
        indices = []
        for part in raw.split(","):
            part = part.strip()
            try:
                idx = int(part) - 1
                if 0 <= idx < len(options):
                    indices.append(idx)
            except ValueError:
                pass
        return [options[i] for i in indices] if indices else list(options)
    else:
        while True:
            raw = prompt(msg)
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(options):
                    return [options[idx]]
            except ValueError:
                pass
            print(c("  Ungültige Auswahl.", YELLOW))


# NRW city coordinates

NRW_CITIES: dict[str, tuple[float, float]] = {
    "Köln":          (50.9333, 6.9500),
    "Düsseldorf":    (51.2217, 6.7762),
    "Dortmund":      (51.5136, 7.4653),
    "Essen":         (51.4508, 7.0131),
    "Duisburg":      (51.4344, 6.7623),
    "Bonn":          (50.7374, 7.0982),
    "Münster":       (51.9625, 7.6253),
    "Aachen":        (50.7753, 6.0839),
    "Bielefeld":     (52.0211, 8.5311),
    "Bochum":        (51.4819, 7.2197),
    "Wuppertal":     (51.2562, 7.1508),
    "Gelsenkirchen": (51.5177, 7.0857),
    "Oberhausen":    (51.4878, 6.8617),
    "Krefeld":       (51.3331, 6.5583),
    "Mönchengladbach":(51.1805, 6.4428),
    "Solingen":      (51.1607, 7.0837),
    "Paderborn":     (51.7189, 8.7575),
    "Siegen":        (50.8747, 8.0243),
}


def choose_location() -> tuple[float, float, str]:
    """Ask the user to enter a PLZ or pick a city."""
    print(f"\n{bold('Dein Startort')}")
    print(
        f"  {c('1', CYAN)} Postleitzahl eingeben  "
        f"{c('2', CYAN)} Stadt aus Liste wählen"
    )
    print()

    mode = prompt("Wie möchtest du deinen Standort angeben? [1/2]", "1")

    if mode.strip() == "2":
        # City list
        cities = list(NRW_CITIES.keys())
        for i, city in enumerate(cities, start=1):
            print(f"  {DIM}{i:>2}.{RESET}  {city}")
        print()
        raw = prompt("Stadtnummer wählen", "1")
        try:
            idx = max(1, min(int(raw), len(cities))) - 1
        except ValueError:
            idx = 0
        city = cities[idx]
        lat, lon = NRW_CITIES[city]
        return lat, lon, city

    # PLZ input
    while True:
        plz = prompt("Postleitzahl eingeben (z.B. 47051)")
        result = lookup_plz(plz)
        if result:
            lat, lon, city = result
            print(c(f"\n  ✓ {city} gefunden", GREEN))
            return lat, lon, city
        print(c(
            f"  PLZ '{plz}' nicht gefunden. "
            "Bitte eine gültige NRW-Postleitzahl eingeben.",
            YELLOW
        ))


# Place card

def print_place_card(place: dict, transport: str, index: int, total: int) -> None:
    dist   = place["distance_km"]
    mins   = travel_time_minutes(dist, transport)
    ttime  = format_travel_time(mins)
    icon   = cat_icon(place["category"])
    t_icon = TRANSPORT_EMOJI.get(transport, "🚗")

    print(f"\n  {'─' * 46}")
    print(f"  {DIM}[{index}/{total}]{RESET}  {bold(place['name'])}  {icon}")
    print(f"  {DIM}Ort:{RESET}         {place['city']}")
    print(f"  {DIM}Kategorie:{RESET}   {place['category']}")
    print(f"  {DIM}Entfernung:{RESET}  {c(f'{dist} km', CYAN)}   {t_icon} {c(ttime, YELLOW)}")
    if place.get("description"):
        desc = place["description"]
        if len(desc) > 80:
            desc = desc[:77] + "…"
        print(f"  {DIM}Info:{RESET}        {desc}")
    print(f"  {'─' * 46}")


# Browse loop

def browse(places: list[dict], transport: str, storage: FavoritesStorage) -> None:
    total   = len(places)
    index   = 0
    liked   = 0
    skipped = 0

    print(f"\n{bold('Orte durchsuchen')}")
    print(
        f"  {c('L', GREEN)} Gefällt mir   "
        f"{c('S / ENTER', DIM)} Überspringen   "
        f"{c('F', MAGENTA)} Favoriten   "
        f"{c('Q', RED)} Beenden"
    )

    while index < total:
        place = places[index]
        print_place_card(place, transport, index + 1, total)
        print(
            f"  {c('L', GREEN)} Gefällt mir   "
            f"{c('S / ENTER', DIM)} Überspringen   "
            f"{c('F', MAGENTA)} Favoriten   "
            f"{c('Q', RED)} Beenden"
        )

        already = storage.contains(place["id"])
        if already:
            print(c("  ★ Bereits in deinen Favoriten gespeichert.", YELLOW))

        try:
            choice = input(f"\n{CYAN}▶{RESET} Aktion [L/s/f/q]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice in ("q", "quit", "exit", "beenden"):
            print(c("\n  Auf Wiedersehen! 👋", CYAN))
            break
        elif choice == "f":
            show_favorites(storage, transport)
            continue  # don't advance index
        elif choice == "l":
            if not already:
                storage.add(place)
                liked += 1
                print(c("  ❤️  Gespeichert!", GREEN))
            else:
                print(c("  Bereits in deinen Favoriten.", DIM))
        else:
            skipped += 1
            print(c("  ⏭  Übersprungen.", DIM))

        index += 1

    if index >= total:
        print(f"\n{c('  Alle Orte wurden angezeigt! 🎉', YELLOW)}")

    print(
        f"\n  {bold('Zusammenfassung:')}  "
        f"{c(str(liked), GREEN)} geliked  ·  "
        f"{c(str(skipped), DIM)} übersprungen  ·  "
        f"{c(str(storage.count()), MAGENTA)} Favoriten gesamt"
    )


# Favorites view

def show_favorites(storage: FavoritesStorage, transport: str = "car") -> None:
    favs = storage.all()
    if not favs:
        print(c("\n  Noch keine Favoriten gespeichert.", DIM))
        return

    print(f"\n  {bold('Deine Favoriten')} ({len(favs)} {'Ort' if len(favs) == 1 else 'Orte'})")
    print(f"  {'─' * 44}")
    for i, place in enumerate(favs, start=1):
        icon = cat_icon(place["category"])
        dist = place.get("distance_km", "?")
        print(
            f"  {DIM}{i:>2}.{RESET}  {icon}  {bold(place['name'])}"
            f"  {DIM}({place['city']} · {place['category']} · {dist} km){RESET}"
        )
    print(f"  {'─' * 44}")

    print()
    raw = prompt("Favorit entfernen? (Nummer eingeben oder ENTER zum Fortfahren)", "")
    if raw:
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(favs):
                removed = storage.remove(favs[idx]["id"])
                if removed:
                    print(c(f"  '{favs[idx]['name']}' wurde entfernt.", YELLOW))
        except ValueError:
            pass


# Main session

def run() -> None:
    print(BANNER)

    # Load data
    try:
        places = load_places()
    except FileNotFoundError as exc:
        print(c(str(exc), RED))
        sys.exit(1)

    storage = FavoritesStorage()

    # Location
    user_lat, user_lon, user_city = choose_location()
    print(c(f"\n  Standort gesetzt: {user_city} ({user_lat:.4f}°N, {user_lon:.4f}°E)", DIM))

    # Max distance
    print(f"\n{bold('Maximale Entfernung')}")
    max_km = prompt_int(
        "Wie weit möchtest du fahren? (km)", default=50, min_val=1, max_val=500
    )

    # Transport
    print(f"\n{bold('Verkehrsmittel')}")
    transport_options = ["walking", "bike", "car"]
    transport_labels  = {
        "walking": "🚶 Zu Fuß",
        "bike":    "🚴 Fahrrad",
        "car":     "🚗 Auto",
    }
    print()
    for i, t in enumerate(transport_options, start=1):
        print(f"  {DIM}{i:>2}.{RESET}  {transport_labels[t]}")
    print()
    raw = prompt("Verkehrsmittel wählen", "3")
    try:
        t_idx = int(raw) - 1
        if not (0 <= t_idx < len(transport_options)):
            t_idx = 2
    except ValueError:
        t_idx = 2
    transport = transport_options[t_idx]
    print(c(f"\n  Verkehrsmittel: {transport_labels[transport]}", DIM))

    # Categories
    print(f"\n{bold('Aktivitätskategorien')}")
    all_cats = get_all_categories(places)
    selected_cats = choose_from_list(
        all_cats,
        "Kategorien wählen (Kommagetrennt oder ENTER für alle)",
        multi=True,
        default_all=True,
    )
    print(c(f"\n  Ausgewählt: {', '.join(selected_cats)}", DIM))

    # Filter and recommend
    filtered = filter_places(places, user_lat, user_lon, max_km, selected_cats)
    filtered = shuffle_recommendations(filtered)

    if not filtered:
        print(c(
            f"\n  Keine Orte gefunden in {max_km} km mit den gewählten Kategorien.",
            YELLOW,
        ))
        print(c("  Tipp: Erhöhe die Entfernung oder wähle mehr Kategorien.", DIM))
        sys.exit(0)

    print(c(f"\n  {len(filtered)} Orte gefunden – viel Spaß beim Entdecken! 🎉", GREEN))
    input(f"\n{CYAN}▶{RESET} ENTER drücken um zu starten …")

    browse(filtered, transport, storage)

    # Final favorites summary
    if storage.count() > 0:
        raw = prompt("\nFavoriten zum Abschluss anzeigen? [j/N]", "n")
        if raw.lower() in ("j", "ja", "y", "yes"):
            show_favorites(storage, transport)

    print(c(f"\n  Favoriten gespeichert unter: {storage.path}", DIM))
    print(c("  Bis zum nächsten Mal! 🗺️\n", CYAN))

# Map export
    if storage.count() > 0:
        raw = prompt("\nFavoriten als Karte im Browser öffnen? [j/N]", "n")
        if raw.lower() in ("j", "ja", "y", "yes"):
            from goout.map_export import export_map
            import webbrowser
            map_path = export_map(storage.all())
            print(c(f"\n  🗺️  Karte gespeichert: {map_path}", GREEN))
            webbrowser.open(map_path.as_uri())
 
    print(c(f"\n  Favoriten gespeichert unter: {storage.path}", DIM))
    print(c("  Bis zum nächsten Mal! 🗺️\n", CYAN))