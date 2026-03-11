"""
collections.Counter — Quick Summary
-----------------------------------
Counter is a subclass of dict used for counting hashable objects.
It stores elements as keys and their counts as values.

Think of it as a frequency table.

Import
------
from collections import Counter


Basic Example
-------------
Count occurrences in a list.

from collections import Counter

items = ["apple", "banana", "apple", "orange", "banana", "apple"]
counts = Counter(items)

print(counts)
# Counter({'apple': 3, 'banana': 2, 'orange': 1})


Access Counts
-------------
counts["apple"]
# 3

counts["grape"]
# 0   (missing keys return 0 instead of raising KeyError)


Most Common Elements
--------------------
counts.most_common(2)

# [('apple', 3), ('banana', 2)]


Update Counts
-------------
Adds new counts to existing ones.

counts.update(["apple", "grape"])

print(counts)
# Counter({'apple': 4, 'banana': 2, 'orange': 1, 'grape': 1})


Subtract Counts
---------------
counts.subtract(["apple", "banana"])

print(counts)
# Counter({'apple': 3, 'banana': 1, 'orange': 1, 'grape': 1})


Elements Iterator
-----------------
Returns elements repeated by their count.

list(counts.elements())

# ['apple', 'apple', 'apple', 'banana', 'orange', 'grape']


Counter Math Operations
-----------------------
Counters support arithmetic operations.

c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

Addition:
c1 + c2
# Counter({'a': 4, 'b': 3})

Subtraction:
c1 - c2
# Counter({'a': 2})

Intersection (min counts):
c1 & c2
# Counter({'a': 1, 'b': 1})

Union (max counts):
c1 | c2
# Counter({'a': 3, 'b': 2})


Common Use Cases
----------------
• Count word frequencies in text
• Count log events or errors
• Histogram-like statistics
• Fast frequency analysis


TLDR
----
Counter = a dictionary optimized for counting things.
Keys = items
Values = number of occurrences
"""


from collections import Counter
opening_inventory = ['shoes', 'shoes', 'skirt', 'jeans', 'blouse', 'shoes', 't-shirt', 'dress', 'jeans', 'blouse', 'skirt', 'skirt', 'shorts', 'jeans', 'dress', 't-shirt', 'dress', 'blouse', 't-shirt', 'dress', 'dress', 'dress', 'jeans', 'dress', 'blouse']

closing_inventory = ['shoes', 'skirt', 'jeans', 'blouse', 'dress', 'skirt', 'shorts', 'jeans', 'dress', 'dress', 'jeans', 'dress', 'blouse']

# Write your code below!
def find_amount_sold(opening, closing, item):
  opening_count = Counter(opening)
  closing_count = Counter(closing)
  opening_count.subtract(closing_count)
  return opening_count[item]

tshirts_sold = find_amount_sold(opening_inventory, closing_inventory, 't-shirt')
print(tshirts_sold)