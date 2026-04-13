# 🐍 Python 3 Built-in Functions & Methods Cheat Sheet

---

# 🔹 1. UNIVERSAL BUILT-IN FUNCTIONS

| Function | Works On | What It Does |
|-----------|----------|--------------|
| `type(x)` | Any | Returns data type |
| `len(x)` | str, list, tuple, dict, set | Returns length |
| `print(x)` | Any | Prints to stdout |
| `input()` | — | Reads user input |
| `id(x)` | Any | Memory identity |
| `isinstance(x, t)` | Any | Type check |
| `sorted(x)` | iterable | Returns sorted list |
| `reversed(x)` | sequence | Reverse iterator |
| `enumerate(x)` | iterable | Index + value pairs |
| `zip(a, b)` | iterables | Combine iterables |
| `map(f, x)` | iterable | Apply function |
| `filter(f, x)` | iterable | Filter values |
| `any(x)` | iterable | True if any true |
| `all(x)` | iterable | True if all true |
| `sum(x)` | numbers | Sum values |
| `min(x)` | comparable | Minimum value |
| `max(x)` | comparable | Maximum value |
| `abs(x)` | numbers | Absolute value |
| `round(x)` | float | Round number |

---

# 🔹 2. STRING METHODS (`str`)

```python
s = "hello world"
```

### ⚡ Accessing Strings
```python
s = "hello world"

s[0]          # "h"          — first character
s[-1]         # "d"          — last character
s[0:5]        # "hello"      — slice (start:stop)
s[6:]         # "world"      — slice to end
s[:5]         # "hello"      — slice from start
s[::2]        # "hlowrd"     — every 2nd character
s[::-1]       # "dlrow olleh" — reversed

# Iterate
for char in s:
    print(char)

# Check membership
"hello" in s  # True
```

| Method | Description |
|---------|-------------|
| `s.lower()` | lowercase |
| `s.upper()` | uppercase |
| `s.title()` | Title Case |
| `s.strip()` | Remove whitespace |
| `s.split()` | Split into list |
| `" ".join(list)` | Join list into string |
| `s.replace(a, b)` | Replace substring |
| `s.find(x)` | Index or -1 |
| `s.count(x)` | Count occurrences |
| `s.startswith(x)` | Boolean |
| `s.endswith(x)` | Boolean |
| `s.isdigit()` | True if numeric |
| `s.isalpha()` | True if letters |
| `s.isalnum()` | Letters + numbers |

---

# 🔹 3. LIST METHODS (`list`)

```python
lst = [1, 2, 3]
```

### ⚡ Accessing Lists
```python
lst = ["a", "b", "c", "d"]

lst[0]        # "a"           — first item
lst[-1]       # "d"           — last item
lst[1:3]      # ["b", "c"]   — slice
lst[:2]       # ["a", "b"]   — first two
lst[2:]       # ["c", "d"]   — from index 2 onward
lst[::-1]     # ["d","c","b","a"] — reversed

# Iterate
for item in lst:
    print(item)

# Iterate with index
for i, item in enumerate(lst):
    print(i, item)

# Check membership
"a" in lst    # True

# Nested list access
matrix = [[1, 2], [3, 4]]
matrix[0][1]  # 2  — row 0, col 1
```

| Method | Description |
|---------|-------------|
| `lst.append(x)` | Add to end |
| `lst.extend(iterable)` | Add multiple |
| `lst.insert(i, x)` | Insert at index |
| `lst.remove(x)` | Remove first match |
| `lst.pop()` | Remove last |
| `lst.pop(i)` | Remove index |
| `lst.clear()` | Remove all |
| `lst.index(x)` | First index |
| `lst.count(x)` | Count value |
| `lst.sort()` | Sort in place |
| `lst.reverse()` | Reverse in place |
| `lst.copy()` | Shallow copy |

---

# 🔹 4. TUPLE (`tuple`)

```python
t = (1, 2, 3)
```

### ⚡ Accessing Tuples
```python
t = ("dev", "ops", "sre", "infra")

t[0]          # "dev"              — first item
t[-1]         # "infra"            — last item
t[1:3]        # ("ops", "sre")     — slice
t[::-1]       # ("infra","sre","ops","dev") — reversed

# Unpack
role, env, team = ("admin", "prod", "platform")
print(role)   # "admin"

# Unpack with wildcard
first, *rest = (1, 2, 3, 4)
# first = 1, rest = [2, 3, 4]

# Iterate
for item in t:
    print(item)

# Check membership
"ops" in t    # True
```

| Method | Description |
|---------|-------------|
| `t.count(x)` | Count value |
| `t.index(x)` | Find index |

---

# 🔹 5. DICTIONARY METHODS (`dict`)

```python
d = {"a": 1, "b": 2}
```

### ⚡ Accessing Dictionaries
```python
d = {"host": "server01", "port": 8080, "env": "prod"}

d["host"]             # "server01"     — direct key access
d.get("port")         # 8080           — safe access
d.get("timeout", 30)  # 30             — default if missing

# All keys / values / pairs
d.keys()              # dict_keys(["host", "port", "env"])
d.values()            # dict_values(["server01", 8080, "prod"])
d.items()             # dict_items([("host","server01"), ...])

# Iterate keys
for key in d:
    print(key)

# Iterate key-value pairs
for key, val in d.items():
    print(f"{key} = {val}")

# Check key existence
"host" in d           # True
"timeout" in d        # False

# Nested dict access
config = {"db": {"host": "db01", "port": 5432}}
config["db"]["host"]  # "db01"
config["db"].get("password", "n/a")  # "n/a"
```

| Method | Description |
|---------|-------------|
| `d.keys()` | All keys |
| `d.values()` | All values |
| `d.items()` | Key/value pairs |
| `d.get(k)` | Safe access |
| `d.get(k, default)` | Default fallback |
| `d.update(other)` | Merge dict |
| `d.pop(k)` | Remove key |
| `d.popitem()` | Remove last |
| `d.clear()` | Remove all |
| `d.setdefault(k, v)` | Set if missing |
| `d.copy()` | Shallow copy |

---

# 🔹 6. SET METHODS (`set`)

```python
s = {1, 2, 3}
```

### ⚡ Accessing Sets
```python
s = {"nginx", "apache", "caddy"}

# ⚠️ Sets are UNORDERED — no indexing or slicing

# Check membership (O(1) — very fast)
"nginx" in s          # True
"iis" in s            # False

# Iterate (order not guaranteed)
for item in s:
    print(item)

# Convert to sorted list when you need ordering
sorted(s)             # ["apache", "caddy", "nginx"]

# Get an arbitrary item
next(iter(s))         # e.g. "nginx" (not guaranteed)

# Safe version for empty set
next(iter(s), None)   # None if s is empty

# Common pattern: single-item set -> value
single = {"only"}
next(iter(single))    # "only"

# Set operations — great for comparing lists
active  = {"web01", "web02", "db01"}
healthy = {"web01", "db01"}

active - healthy      # {"web02"}         — unhealthy servers
active & healthy      # {"web01", "db01"} — intersection
active | healthy      # all unique servers — union
```

| Method | Description |
|---------|-------------|
| `s.add(x)` | Add element |
| `s.remove(x)` | Remove (error if missing) |
| `s.discard(x)` | Remove safely |
| `s.pop()` | Remove random |
| `s.clear()` | Remove all |
| `s.union(other)` | Combine |
| `s.intersection(other)` | Common items |
| `s.difference(other)` | Subtract |
| `s.issubset(other)` | Check subset |
| `s.issuperset(other)` | Check superset |

---

# 🔹 7. NUMERIC BUILT-INS

| Function | Description |
|-----------|-------------|
| `int(x)` | Convert to int |
| `float(x)` | Convert to float |
| `str(x)` | Convert to string |
| `pow(a, b)` | Exponent |
| `divmod(a, b)` | Quotient + remainder |

### ⚡ Quick Examples
```python
int("42")           # 42
int(3.9)            # 3      — truncates, does NOT round
float("3.14")       # 3.14
str(100)            # "100"
pow(2, 10)          # 1024
divmod(17, 5)       # (3, 2) — quotient=3, remainder=2
abs(-99)            # 99
round(3.14159, 2)   # 3.14
```

---

# 🔹 8. ITERATION HELPERS

| Function | Why It's Powerful |
|-----------|-------------------|
| `range()` | Loop control |
| `enumerate()` | Index + value |
| `zip()` | Parallel iteration |
| `dict()` | Build dict from tuples |
| `list()` | Convert iterable |
| `set()` | Remove duplicates |

### ⚡ Quick Examples
```python
# range
list(range(5))              # [0, 1, 2, 3, 4]
list(range(1, 6))           # [1, 2, 3, 4, 5]
list(range(0, 10, 2))       # [0, 2, 4, 6, 8]

# enumerate
hosts = ["web01", "web02", "db01"]
for i, host in enumerate(hosts):
    print(i, host)          # 0 web01 / 1 web02 / 2 db01

# zip — pair up two lists
names  = ["alice", "bob"]
roles  = ["admin", "viewer"]
for name, role in zip(names, roles):
    print(name, role)       # alice admin / bob viewer

# dict() from zipped pairs
dict(zip(names, roles))     # {"alice": "admin", "bob": "viewer"}

# list() / set() conversion
set([1, 2, 2, 3, 3])        # {1, 2, 3}  — removes duplicates
list({1, 2, 3})             # [1, 2, 3]  — set → list
```

---

# 🔹 9. FILE HANDLING

```python
with open("file.txt", "r") as f:
```

| Mode | Meaning |
|------|---------|
| `"r"` | Read |
| `"w"` | Write (overwrite) |
| `"a"` | Append |
| `"rb"` | Read binary |

### ⚡ Quick Examples
```python
# Read entire file
with open("config.txt", "r") as f:
    content = f.read()

# Read line by line (memory efficient)
with open("hosts.txt", "r") as f:
    for line in f:
        print(line.strip())

# Read all lines into a list
with open("hosts.txt", "r") as f:
    lines = f.readlines()   # ["\n" included]
    lines = f.read().splitlines()  # cleaner — no \n

# Write to file
with open("output.txt", "w") as f:
    f.write("server01\n")

# Append to file
with open("output.txt", "a") as f:
    f.write("server02\n")
```

---

# 🔹 10. TYPE QUICK REFERENCE

| Type | Mutable? |
|------|----------|
| `str` | ❌ No |
| `list` | ✅ Yes |
| `tuple` | ❌ No |
| `dict` | ✅ Yes |
| `set` | ✅ Yes |
| `int` | ❌ No |
| `float` | ❌ No |

### ⚡ Why Mutability Matters
```python
# Immutable — creates a NEW object
s = "hello"
s[0] = "H"      # ❌ TypeError

s = "H" + s[1:] # ✅ "Hello" — must reassign

# Mutable — modifies IN PLACE
lst = [1, 2, 3]
lst[0] = 99     # ✅ lst is now [99, 2, 3]

# Tuple as dict key (hashable) ✅
coords = {(0, 0): "origin", (1, 2): "point A"}

# List as dict key ❌ — TypeError: unhashable type
# {[0, 0]: "origin"}
```

---

# 🧠 DevOps Interview Power Moves

Know these cold:

- `dict.get()`
- `dict.setdefault()`
- `enumerate()`
- `zip()`
- `sorted()`
- `any()` / `all()`
- `with open()`
- `try/except`
- List comprehensions
- Dictionary comprehensions
- `next(iter())`

### ⚡ One-Liners Worth Memorizing
```python
# List comprehension
ports = [p for p in [22, 80, 443, 8080] if p > 100]
# [80, 443, 8080]

# Dict comprehension
env = {"HOST": "server01", "PORT": "8080"}
lowered = {k.lower(): v for k, v in env.items()}
# {"host": "server01", "port": "8080"}

# any / all — great for validation
ports = [80, 443, 8080]
any(p > 1024 for p in ports)   # True  (8080)
all(p > 0 for p in ports)      # True

# next(iter()) — grab one item from a set
services = {"nginx", "apache", "caddy"}
first = next(iter(services))   # arbitrary item

# safe default when set may be empty
maybe_item = next(iter(set()), None)   # None

# try/except
try:
    val = int("not_a_number")
except ValueError as e:
    print(f"Bad value: {e}")
```