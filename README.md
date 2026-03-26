# GoOut NRW
 
GoOut NRW is a Python command-line application that recommends leisure
activities and places in North Rhine-Westphalia (NRW), Germany.
The application suggests places based on user preferences such as
distance, transport mode and activity categories. Users can browse
suggested locations and mark places they find interesting.
The idea is conceptually similar to a simple swipe-based recommendation
system for discovering nearby activities.
 
------------------------------------------------------------------------
 
## Features
 
-   discover leisure activities in NRW
-   filter by maximum distance
-   choose transport mode (walking, bike, car)
-   select activity categories
-   interactively browse suggested places
-   save favourite locations
 
------------------------------------------------------------------------
 
## Data Source
 
The project uses open datasets from **Open Data NRW**.
 
Examples of included data:
 
-   tourist attractions
-   points of interest
-   leisure activities
-   cultural sites
-   parks and nature locations
 
The datasets contain information such as:
 
-   place name
-   category
-   city
-   geographic coordinates (latitude, longitude)
 
The data is processed and stored locally in JSON format for efficient
use within the application.
 
------------------------------------------------------------------------
 
## Installation
 
Clone the repository:
 
```bash
git clone https://github.com/Imelanora/goout-nrw.git
cd goout-nrw
```
 
Install dependencies:
 
```bash
pip install pandas numpy
```
 
------------------------------------------------------------------------
 
## Usage
 
Start the application with:
 
```bash
PYTHONPATH=src python -m goout
```
 
Example workflow:
 
1.  Enter your location
2.  Select maximum distance
3.  Choose transport mode
4.  Select activity categories
5.  Browse suggested places
6.  Like or skip locations
 
------------------------------------------------------------------------
 
## Project Structure
 
```
goout-nrw
│
├── README.md
├── pyproject.toml
├── .gitignore
│
├── data/
│   ├── raw/                    # original Open Data NRW datasets
│   │   └── open_data_nrw.csv
│   │
│   └── processed/              # cleaned and standardized dataset
│       └── places.json
│
├── scripts/
│   └── prepare_data.py         # Python script to preprocess and unify datasets
│
└── src/
    └── goout/
        ├── __init__.py
        ├── __main__.py         # CLI entry point
        ├── app.py              # main application logic
        ├── recommender.py      # place recommendation logic
        ├── distance.py         # geographic distance calculation
        └── storage.py          # save user favorites
│
└── test/
    └── test_distance.py
    └── test_recommender.py
    └── test_storage.py 

```
 
### Structure Explanation
 
**data/raw/**  
Contains the original datasets downloaded from Open Data NRW.
 
**data/processed/**  
Contains the standardized dataset (`places.json`) used by the application.
 
**scripts/**  
Contains Python scripts used for preprocessing and preparing the datasets.
 
**src/goout/**  
Contains the main application source code.
 
------------------------------------------------------------------------
 
## Technologies
 
-   Python 3.9+
-   pandas
-   numpy
-   JSON data processing
 
------------------------------------------------------------------------
 
## Future Improvements
 
Possible extensions include:
 
-   map visualizations
-   smarter recommendation algorithms
-   integration of additional open datasets
-   location-based filtering using real GPS coordinates
