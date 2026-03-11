from collections import defaultdict

"""
defaultdict — TLDR

defaultdict is a dictionary from the collections module that automatically
creates a default value for missing keys instead of raising a KeyError.

Normal dictionary behavior:

    d = {}
    d['a'] += 1

This fails because 'a' does not exist yet.

defaultdict behavior:

    from collections import defaultdict

    d = defaultdict(int)
    d['a'] += 1

Now it works because defaultdict automatically creates the key with
a default value.

-----------------------------------------------------

How it works

defaultdict(default_factory)

default_factory = function used to create the default value
when a missing key is accessed.

Common factories:

int     → 0
list    → []
set     → set()
str     → ""

-----------------------------------------------------

Example: counting items

from collections import defaultdict

counts = defaultdict(int)

for word in ["apple", "banana", "apple"]:
    counts[word] += 1

Result:
{'apple': 2, 'banana': 1}

-----------------------------------------------------

Example: grouping values

from collections import defaultdict

groups = defaultdict(list)

groups['fruit'].append('apple')
groups['fruit'].append('banana')

Result:
{'fruit': ['apple', 'banana']}

-----------------------------------------------------

Key idea

defaultdict automatically creates missing keys using the
factory function you provide.

This removes the need for patterns like:

if key not in dict:
    dict[key] = []

-----------------------------------------------------

Mental model

dict:
    "Key doesn't exist → error"

defaultdict:
    "Key doesn't exist → create it automatically"
"""

# We set the default value using a
# lambda expression.
# Any time we try to access a key that does not exist, 
# it automatically updates our defaultdict object by creating the new key-value pair 
# using the missing key and the default value.
validate_prices = defaultdict(lambda: 'No Price Assigned')

# Add new key:value pair to validate_prices dictionary
validate_prices['jeans'] = 19.99
validate_prices['shoes'] = 24.99
validate_prices['t-shirt'] = 9.99
validate_prices['blouse'] = 19.99

# Attempt to access non existing key
print(validate_prices['jacket'])
print(dict(validate_prices))
