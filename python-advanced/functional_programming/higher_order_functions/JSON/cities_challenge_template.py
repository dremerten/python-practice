import json
from collections import namedtuple
from functools import reduce

# Define the city namedtuple
city = namedtuple("city", ["name", "country", "coordinates", "continent"])

# Load the city data from the JSON file
with open('cities.json') as json_file:
    data = json.load(json_file) 

# Step 1: Create `cities` as a tuple of city namedtuples
# Hint: You'll need to extract the city data from `data['city']` and create namedtuples for each city.
# Use a loop or comprehension to make sure each city is in the right format.
# Remember, a city namedtuple has: name, country, coordinates, and continent.
# Example: (City(name='New York', country='United States of America', coordinates=[40.7128, -74.006], continent='North America')

cities = None

# Step 2: Filter the cities that are in Asia
# Hint: You will need to filter the `cities` tuple based on the continent.
# Use `if` conditions to check if the continent is "Asia" and build a new list or tuple with only those cities.

asia = None

# Step 3: Find the westernmost city in Asia using `reduce`
# Hint: Use `reduce` to compare cities based on their longitude (coordinates[1]).
# Compare each city's longitude and keep the one with the smallest longitude (i.e., most western city).

west = None

# Print the result
print(west)