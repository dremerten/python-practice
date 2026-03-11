from helper_functions import process_csv_supplies
from collections import deque

"""
Supply Queue Prioritization

This script processes supply records from a CSV source and organizes them
into a priority-based queue using a deque.

Steps performed:

1. Load CSV Data
   - Calls `process_csv_supplies()` to retrieve supply records.
   - The first row is skipped because it contains column headers.

2. Build Priority Queue
   - A deque (`supplies_deque`) is used to efficiently manage items
     from both ends.
   - Each row is converted to a tuple before insertion.
   - If the supply is marked "important" (column index 2):
        -> it is added to the *front* of the deque using `appendleft()`.
   - Otherwise:
        -> it is added to the *back* of the deque using `append()`.

3. Extract Important Supplies
   - Up to the first 25 items are removed from the *left* side of the deque
     using `popleft()`.
   - These items are stored in `ordered_important_supplies`.

4. Extract Unimportant Supplies
   - Up to the last 10 items are removed from the *right* side of the deque
     using `pop()`.
   - These items are stored in `ordered_unimportant_supplies`.

5. Output
   - Prints the deque containing the prioritized important supplies.
   - Prints the remaining supplies still in the queue.

Why deque?
`collections.deque` allows efficient O(1) insertion and removal from both
ends of the queue, making it ideal for priority-style processing where
items must be handled from both the front and back.
"""

# The first row is skipped since it only contains labels
csv_data = process_csv_supplies()[1:]

supplies_deque = deque()

for i in csv_data:
    if i[2] == "important":
        supplies_deque.appendleft(tuple(i))
    else:
        supplies_deque.append(tuple(i))

ordered_important_supplies = deque(
    supplies_deque.popleft()
    for _ in range(min(25, len(supplies_deque)))
)

ordered_unimportant_supplies = deque(
  supplies_deque.pop()
  for _ in range(min(10, len(supplies_deque)))
)

print(ordered_important_supplies)
print(supplies_deque)