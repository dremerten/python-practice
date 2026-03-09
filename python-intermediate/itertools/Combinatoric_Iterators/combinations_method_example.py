"""
Combinatoric Iterator: Combinations

A combinatoric iterator will perform a set of statistical or mathematical
operations on an input iterable.

A useful itertool that is a combinatoric iterator is the combinations()
itertool. This itertool will produce an iterator of tuples that contain
combinations of all elements in the input.

Base syntax:

combinations(iterable, r)

The combinations() itertool takes two inputs:
- iterable: a collection of elements
- r: the length of each combination tuple

The return type of combinations() is an iterator that can be used in a
for loop or converted into another iterable type using list() or set().

Example:

import itertools

even = [2, 4, 6]
even_combinations = list(itertools.combinations(even, 2))
print(even_combinations)

Explanation:
- Import the itertools module.
- Create an iterator using combinations() with the list of even numbers
  as the first argument and 2 as the second argument.
- Convert the iterator to a list and store it in even_combinations.
- Print even_combinations.

Output:

[(2, 4), (2, 6), (4, 6)]

These tuples represent all possible combinations of 2 elements chosen
from the 3 elements in the list.

Think of the function like this
itertools.combinations(list, group_size)

first argument → the collection of items

second argument → the size of each combination

"""

import itertools

collars = ["Red-S","Red-M", "Blue-XS", "Green-L", "Green-XL", "Yellow-M"]

collar_combinations = list(itertools.combinations(collars, 3))

print(collar_combinations)
print("Total combinations:", len(collar_combinations))