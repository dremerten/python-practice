"""
TUPLES vs NAMEDTUPLES — TLDR

A tuple is an immutable, ordered container used to group data that should
not change.

Example:
    actor_data = ('Leonardo DiCaprio', 1974, 'Titanic', 1997)

Problem:
Accessing values requires numeric indexes, which can make code unclear.

    actor_data[3]   # What does index 3 represent?

To make tuple data self-documenting, Python provides namedtuple
from the collections module.

namedtuple allows you to:
- Keep tuple immutability and order
- Access values by descriptive field names instead of indexes
- Use less memory than dictionaries

Example:

    from collections import namedtuple

    ActorData = namedtuple(
        'ActorData',
        ['name', 'birth_year', 'movie', 'movie_release_date']
    )

    actor = ActorData('Leonardo DiCaprio', 1974, 'Titanic', 1997)

    actor.name   # 'Leonardo DiCaprio'

Key points:
- namedtuple creates a lightweight immutable class-like object
- Fields can be accessed with dot notation (actor.name)
- Field names can be passed as a list or a string
- Convention uses CapWords because it creates a class
- Uses less memory than dictionaries while remaining readable

Useful features:
- Convert to dictionary: _asdict()
- Replace fields: _replace()
- Support default values
"""

from collections import namedtuple

clothes = [('t-shirt', 'green', 'large', 9.99),
           ('jeans', 'blue', 'medium', 14.99),
           ('jacket', 'black', 'x-large', 19.99),
           ('t-shirt', 'grey', 'small', 8.99),
           ('shoes', 'white', '12', 24.99),
           ('t-shirt', 'grey', 'small', 8.99)]

# create a subclass 'ClothingItem' with lables type, color, size, price
ClothingItem = namedtuple("ClothingItem", ['type', 'color', 'size', 'price'])

# create a ClothingItem object and check the price
new_coat = ClothingItem('coat', 'black', 'small', 14.99)
coat_cost = new_coat.price

# loop through clothes list of tuples and unpack each tuple into ClothingItem subclass
updated_clothes_data = [ClothingItem(*item) for item in clothes]
print(updated_clothes_data)