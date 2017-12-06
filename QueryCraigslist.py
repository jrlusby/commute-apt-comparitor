#! /usr/bin/env python2
"""Tool to Query Apartment listings from craigslist and save the results."""

import json
import pprint
import SearchConfig

PP = pprint.PrettyPrinter()


def process_craigslist():
    """Pull data from craigslist."""
    from craigslist import CraigslistHousing

    cl_housing = CraigslistHousing(site=SearchConfig.SITE,
                                   area=SearchConfig.AREA,
                                   category=SearchConfig.CATEGORY,
                                   filters=SearchConfig.FILTERS)

    results = cl_housing.get_results(sort_by='newest',
                                     geotagged=True,
                                     limit=20)

    valid_results = {}

    for result in results:
        geotag = result["geotag"]

        for location, coords in SearchConfig.BOUNDING_AREAS.items():

            # make sure theres a list to append to
            if location not in valid_results.keys():
                valid_results[location] = []

            if geotag and in_box(geotag, coords):
                valid_results[location].append(result)
                break

    with open(SearchConfig.OUTFILE, 'w') as outfile:
        json.dump(valid_results, outfile, indent=2)


def in_box(coords, box):
    """Return true if coordinates are in box."""
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False

if __name__ == "__main__":
    process_craigslist()
