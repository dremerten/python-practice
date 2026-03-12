# Python `collections` Module — Advanced Containers Guide

Python’s **`collections`** module provides specialized container datatypes that extend the functionality of Python’s built-in types (`list`, `dict`, `tuple`, `str`). These containers help make programs **cleaner, more efficient, and more organized**.

Below is a practical overview of the most commonly used advanced containers and when to use them.

---

# Advanced Containers Overview

## `deque`

**Double-ended queue**

A `deque` (pronounced *deck*) is an advanced container optimized for **fast appending and popping from both ends**.

It is much faster than a list when working with the **front of a collection**.

### Best Use Cases

- Queues
- Stacks
- Sliding window algorithms
- Task processing pipelines

### Example

```python
from collections import deque

dq = deque([1, 2, 3])

dq.append(4)        # add to the right
dq.appendleft(0)    # add to the left

dq.pop()            # remove from the right
dq.popleft()        # remove from the left

print(dq)
```

---

# `namedtuple`

A `namedtuple` creates an **immutable tuple-like object with named fields**.

Instead of accessing elements using indexes like a normal tuple, you can access them using **attribute names**.

### Benefits

- More readable than tuples
- Lightweight and fast
- Immutable (cannot be changed after creation)

### Example

```python
from collections import namedtuple

Person = namedtuple("Person", ["name", "age", "role"])

p = Person("Alice", 30, "Engineer")

print(p.name)
print(p.age)
print(p.role)
```

---

# `Counter`

`Counter` is a dictionary subclass used for **counting hashable objects automatically**.

It counts occurrences and stores them as:

```
{element: count}
```

### Example

```python
from collections import Counter

items = ["apple", "banana", "apple", "orange", "banana", "apple"]

counts = Counter(items)

print(counts)
print(counts["apple"])
```

### Output

```
Counter({'apple': 3, 'banana': 2, 'orange': 1})
3
```

### Useful Methods

```python
counts.most_common(2)
counts.elements()
```

---

# `defaultdict`

A `defaultdict` behaves like a normal dictionary, **except it automatically creates values for missing keys**.

Instead of raising a `KeyError`, it initializes the value using a **default factory**.

### Example

```python
from collections import defaultdict

d = defaultdict(int)

d["apples"] += 1
d["apples"] += 1
d["oranges"] += 1

print(d)
```

### Output

```
defaultdict(<class 'int'>, {'apples': 2, 'oranges': 1})
```

### Common Default Factories

| Factory | Use Case |
|------|------|
| `int` | counting |
| `list` | grouping values |
| `set` | unique collections |

### Grouping Example

```python
from collections import defaultdict

groups = defaultdict(list)

groups["fruit"].append("apple")
groups["fruit"].append("banana")

print(groups)
```

---

# `OrderedDict`

`OrderedDict` combines the functionality of a **dictionary and a list** by preserving the **insertion order of keys**.

This allows you to access values by **key** while still maintaining the **order items were added**.

### Example

```python
from collections import OrderedDict

d = OrderedDict()

d["a"] = 1
d["b"] = 2
d["c"] = 3

print(d)
```

### Reordering Example

```python
d.move_to_end("a")

print(d)
```

---

# `ChainMap`

`ChainMap` allows you to **combine multiple dictionaries into a single view**.

When a key is accessed, Python searches each mapping **in order until a match is found**.

### Example

```python
from collections import ChainMap

defaults = {"color": "blue", "user": "guest"}
user_settings = {"user": "admin"}

settings = ChainMap(user_settings, defaults)

print(settings["user"])
print(settings["color"])
```

### Output

```
admin
blue
```

### Useful For

- Configuration systems
- Layered settings
- Environment overrides

---

# Container Wrappers

Python also provides wrapper classes that allow you to **create custom versions of built-in containers**.

These wrappers make it easier to **extend or modify container behavior**.

---

# `UserDict`

A wrapper around dictionaries that allows you to **create custom dictionary behavior**.

### Example

```python
from collections import UserDict

class MyDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, str(value).upper())

d = MyDict()

d["name"] = "alice"

print(d)
```

---

# `UserList`

A wrapper around lists that allows you to **extend list functionality safely**.

### Example

```python
from collections import UserList

class MyList(UserList):
    def append(self, item):
        print("Adding item:", item)
        super().append(item)

l = MyList()

l.append(10)
l.append(20)

print(l)
```

---

# `UserString`

A wrapper around strings that allows you to **extend or modify string behavior**.

### Example

```python
from collections import UserString

class MyString(UserString):
    def shout(self):
        return self.data.upper() + "!"

s = MyString("hello")

print(s.shout())
```

---

# Quick Summary Table

| Container | Purpose |
|------|------|
| `deque` | Fast append/pop from both ends |
| `namedtuple` | Immutable tuple with named fields |
| `Counter` | Count occurrences of elements |
| `defaultdict` | Dictionary with automatic default values |
| `OrderedDict` | Dictionary that preserves insertion order |
| `ChainMap` | Combine multiple dictionaries into one view |
| `UserDict` | Create custom dictionaries |
| `UserList` | Create custom lists |
| `UserString` | Create custom string behavior |

---

# TLDR

Use the **`collections` module** when you want more specialized containers than Python’s built-in data structures provide.

- **deque** → fast queue operations  
- **namedtuple** → readable immutable records  
- **Counter** → counting objects  
- **defaultdict** → automatic dictionary defaults  
- **OrderedDict** → maintain order with dictionary behavior  
- **ChainMap** → combine multiple dictionaries  
- **UserDict / UserList / UserString** → build custom containers
