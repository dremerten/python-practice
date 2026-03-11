# Python Data Structures — One Page Cheat Sheet

==================================================
1. LIST
==================================================
Ordered, mutable collection that allows duplicates.

Example:
nums = [1, 2, 3]

nums.append(4)
nums.insert(1, 10)
nums.remove(2)
nums.pop()
nums.pop(0)

len(nums)
sorted(nums)
sum(nums)
min(nums)
max(nums)

List comprehension:
squares = [x**2 for x in range(10)]

Use when:
- order matters
- indexing is needed
- general purpose storage


==================================================
2. TUPLE
==================================================
Ordered, immutable collection.

Example:
coords = (10, 20)

x = coords[0]

Returning multiple values:
def get_user():
    return ("Alice", 30)

name, age = get_user()

Use when:
- fixed data
- dictionary keys
- safe read-only values


==================================================
3. DICTIONARY
==================================================
Key → Value mapping with fast lookups.

Example:
user = {
    "name": "Alice",
    "age": 30
}

Access:
user["name"]
user.get("age")

Modify:
user["age"] = 31
user["city"] = "NY"

Delete:
del user["age"]

Iteration:
for key, value in user.items():
    print(key, value)

Use when:
- structured data
- configuration
- JSON-like objects


==================================================
4. ORDEREDDICT
==================================================
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


==================================================
5. SET
==================================================
Unordered collection of unique values.

Example:
nums = {1, 2, 3, 3}

nums.add(4)
nums.remove(2)

Membership test:
3 in nums

--------------------------------------------------
SET OPERATIONS
--------------------------------------------------

Create sets:
a = {1,2,3}
b = {3,4,5}

Union (all elements)
a.union(b)
a | b

Result:
{1,2,3,4,5}

Intersection (common elements)
a.intersection(b)
a & b

Result:
{3}

Difference (in a but not b)
a.difference(b)
a - b

Result:
{1,2}

Symmetric Difference (in one set but not both)
a.symmetric_difference(b)
a ^ b

Result:
{1,2,4,5}

Subset (all elements contained in another set)
a = {1,2}
b = {1,2,3}

a.issubset(b)
a <= b

Proper Subset
a < b

Superset
b.issuperset(a)
b >= a

Proper Superset
b > a

Disjoint (no shared elements)
a = {1,2}
b = {3,4}

a.isdisjoint(b)

--------------------------------------------------
SET MODIFICATION
--------------------------------------------------

Add element
s.add(4)

Remove element (raises error if missing)
s.remove(2)

Remove element safely
s.discard(5)

Pop random element
s.pop()

Clear set
s.clear()


==================================================
6. DEQUE
==================================================
Double-ended queue from collections.

Example:
from collections import deque

q = deque([1,2,3])

q.append(4)
q.appendleft(0)

q.pop()
q.popleft()

Use when:
- queue
- stack
- BFS algorithms
- sliding window problems


==================================================
7. HEAP (PRIORITY QUEUE)
==================================================
Smallest element always accessible.

Example:
import heapq

nums = [5,2,8,1]

heapq.heapify(nums)

heapq.heappush(nums, 3)
heapq.heappop(nums)

Use when:
- priority scheduling
- task ordering
- retrieving smallest values quickly


==================================================
8. COUNTER
==================================================
Counts frequency of elements.

Example:
from collections import Counter

data = ["a","b","a","c","a"]

counts = Counter(data)

counts["a"]
counts.most_common(1)

Use when:
- counting items
- frequency analysis
- log analysis


==================================================
9. DEFAULTDICT
==================================================
Dictionary that auto-creates missing keys.

Example:
from collections import defaultdict

d = defaultdict(list)

d["a"].append(1)
d["a"].append(2)

Result:
{'a': [1, 2]}

Use when:
- grouping data
- building adjacency lists
- avoiding KeyError


==================================================
TLDR (MUST MEMORIZE)
==================================================

list        -> ordered mutable collection
tuple       -> ordered immutable collection
dict        -> key/value mapping
OrderedDict -> ordered dictionary with order control
set         -> unique values + set operations
deque       -> fast queue operations
heapq       -> priority queue
Counter     -> frequency counter
defaultdict -> dictionary with automatic initialization