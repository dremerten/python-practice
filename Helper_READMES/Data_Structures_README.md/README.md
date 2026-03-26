# Python Data Structures — One Page Cheat Sheet

---

# 1. LIST
Ordered, mutable collection that allows duplicates.

### Example
```python
nums = [1, 2, 3]        # create list

nums.append(4)          # add element to end
nums.insert(1, 10)      # insert element at index

nums.remove(2)          # remove first occurrence of value
nums.pop()              # remove last element
nums.pop(0)             # remove element at index

nums[0]                 # access element by index
nums[-1]                # access last element

len(nums)               # number of elements
sorted(nums)            # return sorted copy
sum(nums)               # sum numeric values
min(nums)               # smallest value
max(nums)               # largest value

for n in nums:          # iterate through list
    print(n)
```

### List Comprehension
```python
squares = [x**2 for x in range(10)]  # create list using expression and loop
```

### Use When
- order matters  
- indexing is needed  
- general purpose storage

---

# 2. TUPLE
Ordered, immutable collection.

### Example
```python
coords = (10, 20)      # create tuple

coords[0]              # access value by index
coords[-1]             # access last value

x, y = coords          # unpack tuple values into variables

def get_user():
    return ("Alice", 30)   # returning multiple values as tuple

name, age = get_user()     # unpack returned tuple
```

### Use When
- fixed data  
- dictionary keys  
- safe read-only values  

---

# 3. DICTIONARY
Key → Value mapping with fast lookups.

### Example
```python
user = {
    "name": "Alice",
    "age": 30
}                         # create dictionary

user["name"]              # access value by key (raises error if missing)
user.get("age")           # safe access method (returns None if missing)

user["age"] = 31          # update existing key
user["city"] = "NY"       # add new key/value pair

del user["age"]           # delete key/value pair

"name" in user            # check if key exists

len(user)                 # number of key/value pairs

for key, value in user.items():   # iterate over key/value pairs
    print(key, value)
```

### Use When
- structured data  
- configuration  
- JSON-like objects  

---

# 4. ORDEREDDICT
Dictionary that **preserves insertion order explicitly**.

> Python 3.7+ dict already preserves order, but `OrderedDict` provides order manipulation utilities.

### Example
```python
from collections import OrderedDict

od = OrderedDict()      # create ordered dictionary

od["first"] = 1         # insert key/value
od["second"] = 2
od["third"] = 3

od["first"]             # access value by key

od["first"] = 10        # update value

od.move_to_end("first") # move key to end (change order)

od.popitem()            # remove last inserted key/value

for k, v in od.items(): # iterate through dictionary
    print(k, v)
```

### Use When
- strict order control  
- LRU caches  
- order manipulation  

---

# 5. SET
Unordered collection of unique values.

### Example
```python
nums = {1, 2, 3, 3}    # create set (duplicates automatically removed)

nums.add(4)            # add element
nums.remove(2)         # remove element (raises error if missing)

nums.discard(10)       # remove element safely (no error if missing)

3 in nums              # membership test

len(nums)              # number of elements

for n in nums:         # iterate through set
    print(n)
```

---

# SET OPERATIONS

### Create Sets
```python
a = {1,2,3}            # create set
b = {3,4,5}
```

### Union (all elements)
```python
a.union(b)             # combine sets
a | b                  # union operator
```

### Intersection (common elements)
```python
a.intersection(b)      # elements present in both sets
a & b
```

### Difference (in a but not b)
```python
a.difference(b)        # elements only in a
a - b
```

### Symmetric Difference
```python
a.symmetric_difference(b)  # elements not shared
a ^ b
```

### Subset
```python
a = {1,2}
b = {1,2,3}

a.issubset(b)          # check if a is subset of b
a <= b
```

### Proper Subset
```python
a < b                  # subset but not equal
```

### Superset
```python
b.issuperset(a)        # check if b contains a
b >= a
```

### Proper Superset
```python
b > a
```

### Disjoint
```python
a = {1,2}
b = {3,4}

a.isdisjoint(b)        # check if sets share no elements
```

---

# SET MODIFICATION

```python
s = {1,2,3}

s.add(4)               # add element
s.remove(2)            # remove element (error if missing)
s.discard(5)           # remove safely
s.pop()                # remove random element
s.clear()              # remove all elements
```

---

# 6. DEQUE
Double-ended queue from `collections`.

### Example
```python
from collections import deque

q = deque([1,2,3])     # create deque

q.append(4)            # add element to right side
q.appendleft(0)        # add element to left side

q.pop()                # remove element from right side
q.popleft()            # remove element from left side

q[0]                   # access element by index

len(q)                 # number of elements

for item in q:         # iterate through deque
    print(item)
```

### Use When
- queue  
- stack  
- BFS algorithms  
- sliding window problems  

---

# 7. HEAP (PRIORITY QUEUE)

Smallest element always accessible.

### Example
```python
import heapq

nums = [5,2,8,1]       # create list

heapq.heapify(nums)    # convert list to heap structure

heapq.heappush(nums, 3)  # insert element

smallest = heapq.heappop(nums)  # remove smallest element

nums[0]                # access smallest element without removing
```

### Use When
- priority scheduling  
- task ordering  
- retrieving smallest values quickly  

---

# 8. COUNTER

Counts frequency of elements.

### Example
```python
from collections import Counter

data = ["a","b","a","c","a"]

counts = Counter(data)      # create counter

counts["a"]                 # access frequency of element

counts["b"] += 1            # manually update count

counts.most_common(1)       # get most common element

for item, count in counts.items():  # iterate through counts
    print(item, count)
```

### Use When
- counting items  
- frequency analysis  
- log analysis  

---

# 9. DEFAULTDICT

Dictionary that auto-creates missing keys.

### Example
```python
from collections import defaultdict

d = defaultdict(list)   # create defaultdict with list as default

d["a"].append(1)        # key auto-created with empty list
d["a"].append(2)

d["a"]                  # access value

len(d)                  # number of keys

for key, value in d.items():  # iterate through dictionary
    print(key, value)
```

### Use When
- grouping data  
- building adjacency lists  
- avoiding KeyError  

---

# TLDR (MUST MEMORIZE)

| Structure | Purpose |
|-----------|--------|
| `list` | ordered mutable collection |
| `tuple` | ordered immutable collection |
| `dict` | key/value mapping |
| `OrderedDict` | ordered dictionary with order control |
| `set` | unique values + set operations |
| `deque` | fast queue operations |
| `heapq` | priority queue |
| `Counter` | frequency counter |
| `defaultdict` | dictionary with automatic initialization |