import json
from collections import namedtuple
from functools import reduce

# Define the city namedtuple
city = namedtuple("city", ["name", "country", "coordinates", "continent"])

# Load the city data from the JSON file
with open('cities.json') as json_file:
    data = json.load(json_file) 

# Step 1: Create `cities` as a tuple of city namedtuples
cities = tuple(city(c['name'], c['country'], c['coordinates'], c['continent']) for c in data['city'])

# Step 2: Filter the cities that are in Asia
asia = tuple(c for c in cities if c.continent == "Asia")

# Step 3: Find the westernmost city in Asia using reduce
west = reduce(lambda x, y: x if x.coordinates[1] < y.coordinates[1] else y, asia)

# Print the result
print(west)