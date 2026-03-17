####################### Pythonic Way #########################
##############################################################

import json
from collections import namedtuple
from functools import reduce

city = namedtuple("city", ["name", "country", "coordinates", "continent"])

with open('cities.json') as json_file:
    data = json.load(json_file) 

# Using map to create the cities list
cities = map(lambda x: city(x["name"], x["country"], x["coordinates"], x["continent"]), data["city"])

# Using filter to get all cities in Asia
asia = filter(lambda i: i.continent == "Asia", cities)

# Using reduce to find the westernmost city
west = reduce(lambda x, y: x if x.coordinates[1] < y.coordinates[1] else y, asia)

print(west)