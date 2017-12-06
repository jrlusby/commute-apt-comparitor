#! /usr/bin/env python2
"""Configuration Constants for QueryCraigslist."""

BOUNDING_AREAS = {
    "bay_area": [
        [37.2025, -121.6406],
        [38.1826, -122.8102],
    ],
}

SITE = "sfbay"
AREA = "sfc"
CATEGORY = "apa"
FILTERS = {
    'min_price': 1000,
    'max_price': 3000,
    'min_bedrooms': 1,
    'cats_ok': 1,
    'min_bathrooms': 1,
}

OUTFILE = "search_results.json"
