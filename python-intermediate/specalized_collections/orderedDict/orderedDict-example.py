"""
Dictionary that **preserves insertion order explicitly**.

Note:
Python 3.7+ dict already preserves order, but OrderedDict
still provides additional order-related methods.

Example:
from collections import OrderedDict

od = OrderedDict()

od["first"] = 1
od["second"] = 2
od["third"] = 3

for k, v in od.items():
    print(k, v)

Move element:
od.move_to_end("first")

Remove last inserted item:
od.popitem()

Use when:
- strict order control
- LRU caches
- order manipulation
"""

from collections import OrderedDict

order_data = [['Order: 1', 'purchased'],
              ['Order: 2', 'purchased'],
              ['Order: 3', 'purchased'],
              ['Order: 4', 'returned'],
              ['Order: 5', 'purchased'],
              ['Order: 6', 'canceled'],
              ['Order: 7', 'returned'],
              ['Order: 8', 'purchased'],
              ['Order: 9', 'returned'],
              ['Order: 10', 'canceled'],
              ['Order: 11', 'purchased'],
              ['Order: 12', 'returned'],
              ['Order: 13', 'purchased'],
              ['Order: 14', 'canceled'],
              ['Order: 15', 'purchased']]

orders = OrderedDict(order_data)

def organize_orders(orders: OrderedDict):
    to_remove = []
    to_move = []

    for order, status in orders.items():
        if status == "returned":
            to_move.append(order)
        elif status == "canceled":
            to_remove.append(order)

    for order in to_remove:
        orders.pop(order)

    for order in to_move:
        orders.move_to_end(order)

    return orders

result = organize_orders(orders)
print(result)