"""
plz_data.py

Postleitzahl (PLZ) to coordinates mapping for NRW.
"""

# PLZ -> (latitude, longitude, city_name)
NRW_PLZ: dict[str, tuple[float, float, str]] = {
    # Köln
    "50667": (50.9381, 6.9592, "Köln-Innenstadt"),
    "50668": (50.9431, 6.9623, "Köln-Neustadt-Nord"),
    "50676": (50.9267, 6.9478, "Köln-Neustadt-Süd"),
    "50679": (50.9364, 6.9867, "Köln-Deutz"),
    "50733": (50.9642, 6.9478, "Köln-Nippes"),
    "50823": (50.9522, 6.9167, "Köln-Ehrenfeld"),
    "50935": (50.9183, 6.9167, "Köln-Lindenthal"),
    "51103": (50.9319, 7.0131, "Köln-Kalk"),
    "51143": (50.8767, 7.0131, "Köln-Porz"),
    # Düsseldorf
    "40210": (51.2217, 6.7762, "Düsseldorf-Stadtmitte"),
    "40213": (51.2267, 6.7731, "Düsseldorf-Altstadt"),
    "40221": (51.2081, 6.7478, "Düsseldorf-Hafen"),
    "40233": (51.2217, 6.8050, "Düsseldorf-Flingern"),
    "40468": (51.2731, 6.7978, "Düsseldorf-Rath"),
    "40589": (51.1633, 6.8711, "Düsseldorf-Benrath"),
    "40625": (51.2367, 6.8450, "Düsseldorf-Gerresheim"),
    # Dortmund
    "44135": (51.5136, 7.4653, "Dortmund-Innenstadt"),
    "44137": (51.5081, 7.4731, "Dortmund-Innenstadt-West"),
    "44139": (51.5267, 7.4867, "Dortmund-Innenstadt-Nord"),
    "44227": (51.4867, 7.4131, "Dortmund-Eichlinghofen"),
    "44328": (51.5578, 7.5131, "Dortmund-Scharnhorst"),
    "44388": (51.5336, 7.3478, "Dortmund-Lütgendortmund"),
    # Essen
    "45127": (51.4508, 7.0131, "Essen-Innenstadt"),
    "45128": (51.4431, 7.0197, "Essen-Südviertel"),
    "45131": (51.4267, 7.0050, "Essen-Rüttenscheid"),
    "45219": (51.3950, 7.0233, "Essen-Kettwig"),
    "45239": (51.3831, 7.0450, "Essen-Werden"),
    "45355": (51.4731, 6.9478, "Essen-Borbeck"),
    # Duisburg
    "47051": (51.4344, 6.7623, "Duisburg-Innenstadt"),
    "47053": (51.4267, 6.7731, "Duisburg-Dellviertel"),
    "47055": (51.4178, 6.7867, "Duisburg-Hochfeld"),
    "47119": (51.4731, 6.7478, "Duisburg-Ruhrort"),
    "47166": (51.5050, 6.7867, "Duisburg-Meiderich"),
    "47229": (51.3731, 6.7267, "Duisburg-Rheinhausen"),
    # Bonn
    "53111": (50.7374, 7.0982, "Bonn-Innenstadt"),
    "53113": (50.7267, 7.1050, "Bonn-Südstadt"),
    "53115": (50.7178, 7.0867, "Bonn-Poppelsdorf"),
    "53117": (50.7478, 7.0731, "Bonn-Nordstadt"),
    "53119": (50.7578, 7.0867, "Bonn-Tannenbusch"),
    "53175": (50.6978, 7.1267, "Bonn-Bad Godesberg"),
    # Münster
    "48143": (51.9625, 7.6253, "Münster-Innenstadt"),
    "48145": (51.9578, 7.6450, "Münster-Mauritz"),
    "48147": (51.9731, 7.6131, "Münster-Handorf"),
    "48149": (51.9478, 7.6050, "Münster-Gievenbeck"),
    "48155": (51.9478, 7.6578, "Münster-Gremmendorf"),
    "48159": (51.9822, 7.5978, "Münster-Roxel"),
    # Aachen
    "52062": (50.7753, 6.0839, "Aachen-Innenstadt"),
    "52064": (50.7678, 6.0950, "Aachen-Mitte"),
    "52066": (50.7578, 6.1050, "Aachen-Burtscheid"),
    "52068": (50.7867, 6.0731, "Aachen-Nord"),
    "52072": (50.7922, 6.0478, "Aachen-Laurensberg"),
    "52074": (50.7578, 6.0478, "Aachen-Beverau"),
    # Bielefeld
    "33602": (52.0211, 8.5311, "Bielefeld-Innenstadt"),
    "33604": (52.0267, 8.5450, "Bielefeld-Mitte"),
    "33607": (52.0131, 8.5197, "Bielefeld-Sennestadt"),
    "33613": (52.0450, 8.5578, "Bielefeld-Brackwede"),
    "33619": (52.0578, 8.4978, "Bielefeld-Dornberg"),
    # Bochum
    "44787": (51.4819, 7.2197, "Bochum-Innenstadt"),
    "44789": (51.4731, 7.2131, "Bochum-Südwest"),
    "44791": (51.4922, 7.2450, "Bochum-Ost"),
    "44793": (51.4867, 7.1978, "Bochum-West"),
    "44795": (51.4678, 7.1867, "Bochum-Weitmar"),
    "44807": (51.5050, 7.2267, "Bochum-Hamme"),
    # Wuppertal
    "42103": (51.2562, 7.1508, "Wuppertal-Elberfeld"),
    "42105": (51.2478, 7.1450, "Wuppertal-Elberfeld-West"),
    "42107": (51.2578, 7.1678, "Wuppertal-Elberfeld-Ost"),
    "42275": (51.2731, 7.1978, "Wuppertal-Barmen"),
    "42277": (51.2822, 7.2131, "Wuppertal-Oberbarmen"),
    "42329": (51.2267, 7.0731, "Wuppertal-Cronenberg"),
    # Gelsenkirchen
    "45879": (51.5177, 7.0857, "Gelsenkirchen-Innenstadt"),
    "45881": (51.5267, 7.0978, "Gelsenkirchen-Schalke"),
    "45883": (51.5364, 7.1131, "Gelsenkirchen-Heßler"),
    "45891": (51.5578, 7.0731, "Gelsenkirchen-Buer"),
    # Oberhausen
    "46045": (51.4878, 6.8617, "Oberhausen-Innenstadt"),
    "46047": (51.4978, 6.8731, "Oberhausen-Alt-Oberhausen"),
    "46049": (51.5081, 6.8867, "Oberhausen-Osterfeld"),
    "46119": (51.5197, 6.8478, "Oberhausen-Sterkrade"),
    # Krefeld
    "47798": (51.3331, 6.5583, "Krefeld-Innenstadt"),
    "47799": (51.3267, 6.5450, "Krefeld-Südwest"),
    "47800": (51.3431, 6.5731, "Krefeld-Nord"),
    "47802": (51.3197, 6.5867, "Krefeld-Ost"),
    "47803": (51.3578, 6.5267, "Krefeld-Uerdingen"),
    # Mönchengladbach
    "41061": (51.1805, 6.4428, "Mönchengladbach-Innenstadt"),
    "41063": (51.1731, 6.4550, "Mönchengladbach-Stadtmitte"),
    "41065": (51.1867, 6.4678, "Mönchengladbach-Eicken"),
    "41069": (51.1578, 6.4267, "Mönchengladbach-Rheydt"),
    # Paderborn
    "33098": (51.7189, 8.7575, "Paderborn-Innenstadt"),
    "33100": (51.7267, 8.7731, "Paderborn-Nord"),
    "33102": (51.7081, 8.7450, "Paderborn-Süd"),
    # Siegen
    "57072": (50.8747, 8.0243, "Siegen-Innenstadt"),
    "57074": (50.8678, 8.0367, "Siegen-Mitte"),
    "57076": (50.8578, 8.0131, "Siegen-Weidenau"),
}


def lookup_plz(plz: str) -> tuple[float, float, str] | None:
    """Return (lat, lon, city) for a PLZ, or None if not found."""
    return NRW_PLZ.get(plz.strip())


def is_valid_plz(plz: str) -> bool:
    """Check if a PLZ is in the NRW database."""
    return plz.strip() in NRW_PLZ
