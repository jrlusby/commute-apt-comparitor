#! /usr/bin/env python2
"""Tool to compare apartments based on commute information."""

import json
import pprint
from datetime import datetime
import googlemaps
import SearchConfig

PP = pprint.PrettyPrinter()

WORK = "Scale Computing, 360 Ritch St #300, San Francisco, CA 94107"
START_TIME = datetime(2017, 12, 11, 9)
SRC = "70 Renato Ct, Redwood City, CA 94061"
MAX_TIME = 10
MAX_FARE = 15
MAX_STEPS = 3

GMAPS = googlemaps.Client(key='AIzaSyBais7uoDT6b6sKKwjFTmnx11IM7LFDSK0')

# QUERY AND CACHE data from craigslist
# split craigslist data capture into a diff function

# TODO write monthly fare calculator
# Start with google maps fare
# Look for known transit providers
# if its a known transit provider, remove the expected cost of a single trip
# based on transit provider from total fare and add montly price to end price
# multiply leftover single direction fare by 20*2

# TODO also calculate commute to nearest davita, car, transit, and walk


def main():
    """Run main function."""
    # process_google(SRC)
    # QueryCraigslist.process_craigslist()
    with open(SearchConfig.OUTFILE, 'r') as infile:
        grouped_listings = json.load(infile)

        for area, listings in grouped_listings.iteritems():
            print area
            for listing in listings:
                geotag = listing["geotag"]
                valuation = process_google(geotag)
                if valuation:
                    print listing["name"]
                    print listing["price"]
                    print listing["url"]
                    print valuation
                    print


def process_google(source_addr):
    """Look things up on google's apis."""
    # Request directions via public transit
    directions_result = GMAPS.directions(source_addr,
                                         WORK,
                                         mode="transit",
                                         alternatives=True,
                                         arrival_time=START_TIME)
    options = []
    for route in directions_result:
        if "fare" in route.keys():
            fare = route_cost(route)
            total, extra = route_time(route)
            steps = route_steps(route)
            # print fare, total, extra, steps
            if extra <= MAX_TIME and fare <= MAX_FARE and steps <= MAX_STEPS:
                options.append({"total": total,
                                "extra": extra,
                                "fare": fare,
                                "steps": steps})

    options.sort(key=lambda option: option["fare"])

    if options:
        return options[0]
    return None


def route_steps(route):
    """Count number of steps between src and dest."""
    steps = 0
    for leg in route["legs"]:
        steps += len(leg["steps"])
    return steps


def route_cost(route):
    """Return cost of route."""
    return route['fare']['value']


def route_time(route):
    """Return the time spent not on transit."""
    legs = route["legs"]
    # PP.pprint(steps)

    # legs only matter if you're doing a multi stop trip, not sure if there can
    # be a gap between the end of one leg and the start of the next

    total_time = 0
    extra_time = 0

    for leg in legs:

        total_time += leg["duration"]["value"]
        extra_time += leg["duration"]["value"]

        for step in leg["steps"]:

            keys = step.keys()
            if "travel_mode" in keys and step["travel_mode"] == "TRANSIT":
                extra_time -= step["duration"]["value"]

    return total_time/60.0, extra_time/60.0


if __name__ == "__main__":
    main()
