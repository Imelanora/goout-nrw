def print_unique_cities():
    cities = set()

    for _, (_, _, name) in NRW_PLZ.items():
        city = name.split("-")[0]  # Ortsteil abschneiden
        cities.add(city)

    for city in sorted(cities):
        print(city) 

if __name__ == "__main__":
    print_unique_cities()    