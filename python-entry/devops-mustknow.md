# Python 3.14

---

# 🔹 CORE BUILT-INS

| Function | Why It Matters | Example |
|-----------|----------------|---------|
| `len(x)` | Count items | `len([1, 2, 3])  # 3` |
| `type(x)` | Know your data | `type("abc")  # str` |
| `isinstance(x, t)` | Safe type checks | `isinstance(5, int)  # True` |
| `sorted(x)` | Sort iterable | `sorted([3, 1, 2])  # [1, 2, 3]` |
| `min(x)` / `max(x)` | Boundaries | `min([5, 2, 9])  # 2` |
| `sum(x)` | Totals | `sum([1, 2, 3])  # 6` |
| `any(x)` | Any True? | `any([False, False, True])  # True` |
| `all(x)` | All True? | `all([True, True, False])  # False` |
| `enumerate(x)` | Index + value | `for i, v in enumerate(["a", "b"]): print(i, v)` |
| `zip(a, b)` | Parallel iteration | `for x, y in zip([1, 2], ["a", "b"]): print(x, y)` |
| `range(n)` | Controlled loops | `for i in range(3): print(i)` |

### Examples
```python
len([1, 2, 3])                   # count items -> 3
type({"a": 1})                   # get type -> dict
isinstance("hello", str)         # safe type check -> True
sorted([3, 1, 2])                # returns new sorted list -> [1, 2, 3]
min([8, 2, 5])                   # smallest value -> 2
max([8, 2, 5])                   # largest value -> 8
sum([10, 20, 30])                # total -> 60
any([False, False, True])        # True if at least one item is truthy
all([True, True, True])          # True only if all items are truthy

for i, value in enumerate(["a", "b", "c"]):   # access index + value together
    print(i, value)

for num, letter in zip([1, 2, 3], ["a", "b", "c"]):   # pair values from 2 iterables
    print(num, letter)

for i in range(5):                # loop from 0 up to 4
    print(i)
```

---

# 🔹 STRING (`str`)

```python
s = "hello world"
```

| Method | Use Case | Example |
|---------|----------|---------|
| `s.strip()` | Clean input/log lines | `"  hi  ".strip()  # 'hi'` |
| `s.split()` | Parse data | `"a,b,c".split(",")  # ['a', 'b', 'c']` |
| `" ".join(lst)` | Build strings | `" ".join(["hi", "there"])  # 'hi there'` |
| `s.replace(a, b)` | Normalize text | `"a-b-c".replace("-", ":")` |
| `s.startswith(x)` | Log filtering | `"error.log".startswith("err")  # True` |
| `s.endswith(x)` | Extension checks | `"app.log".endswith(".log")  # True` |
| `s.count(x)` | Frequency check | `"banana".count("a")  # 3` |

### Examples
```python
s = "  hello world  "

s.strip()                         # remove leading/trailing whitespace -> "hello world"
s.split()                         # split on whitespace -> ["hello", "world"]
"one,two,three".split(",")        # split by delimiter -> ["one", "two", "three"]

" ".join(["devops", "engineer"])  # join list into string -> "devops engineer"
"-".join(["2026", "03", "12"])    # join with custom separator -> "2026-03-12"

"error: disk full".replace("disk", "memory")   # replace text -> "error: memory full"

"log.txt".startswith("log")       # check prefix -> True
"log.txt".endswith(".txt")        # check suffix -> True

"banana".count("a")               # count occurrences -> 3

s[0]                              # access character by index
s.lower()                         # lowercase copy
s.upper()                         # uppercase copy
```

---

# 🔹 LIST (`list`)

```python
lst = [1, 2, 3]
```

| Method | Use Case | Example |
|---------|----------|---------|
| `append(x)` | Add item | `lst.append(4)` |
| `extend(iterable)` | Merge lists | `lst.extend([4, 5])` |
| `pop()` | Remove last | `lst.pop()` |
| `remove(x)` | Remove value | `lst.remove(2)` |
| `sort()` | Sort in place | `lst.sort()` |
| `reverse()` | Reverse order | `lst.reverse()` |
| `copy()` | Avoid mutation bugs | `new_lst = lst.copy()` |

### Examples
```python
lst = [1, 2, 3]

lst.append(4)                     # add one item to end -> [1, 2, 3, 4]
lst.extend([5, 6])                # add multiple items -> [1, 2, 3, 4, 5, 6]

lst[0]                            # access first item
lst[-1]                           # access last item

lst[1] = 200                      # update value by index

lst.pop()                         # remove and return last item
lst.pop(0)                        # remove and return item at index 0

lst.remove(200)                   # remove first matching value

lst.sort()                        # sort in place
lst.reverse()                     # reverse in place

new_lst = lst.copy()              # shallow copy
len(lst)                          # number of items

for item in lst:                  # iterate values
    print(item)

for i, item in enumerate(lst):    # iterate with index
    print(i, item)
```

---

# 🔹 DICTIONARY (`dict`) ⭐ MOST IMPORTANT

```python
d = {"a": 1}
```

| Method | DevOps Use | Example |
|---------|-------------|---------|
| `d.get(k)` | Safe access | `d.get("a")` |
| `d.get(k, default)` | Avoid KeyError | `d.get("x", 0)` |
| `d.setdefault(k, v)` | Nested counting | `d.setdefault("errors", [])` |
| `d.update(other)` | Merge configs | `d.update({"b": 2})` |
| `d.items()` | Loop key/value | `for k, v in d.items(): ...` |
| `d.keys()` | Iterate keys | `for k in d.keys(): ...` |
| `d.values()` | Iterate values | `for v in d.values(): ...` |
| `d.pop(k)` | Remove key | `d.pop("a")` |

### Examples
```python
d = {"a": 1, "b": 2}

d["a"]                            # direct access by key -> 1
d.get("b")                        # safe access -> 2
d.get("missing")                  # returns None if key missing
d.get("missing", 0)               # returns default -> 0

d["a"] = 100                      # update existing key
d["c"] = 3                        # add new key/value pair

d.setdefault("logs", [])          # create key with default only if missing
d["logs"].append("started")       # now safe to append

d.update({"b": 200, "d": 4})      # merge/update multiple key/value pairs

"a" in d                          # check if key exists -> True
len(d)                            # number of key/value pairs

d.pop("d")                        # remove key and return its value
del d["c"]                        # delete key/value directly

for key, value in d.items():      # iterate key/value pairs
    print(key, value)

for key in d.keys():              # iterate keys
    print(key)

for value in d.values():          # iterate values
    print(value)
```

---

# 🔹 SET (`set`)

```python
s = {1, 2, 3}
```

| Method | Use Case | Example |
|---------|----------|---------|
| `add(x)` | Insert | `s.add(4)` |
| `remove(x)` | Remove | `s.remove(2)` |
| `discard(x)` | Safe remove | `s.discard(99)` |
| `union(other)` | Combine | `s.union({4, 5})` |
| `intersection(other)` | Overlap | `s.intersection({2, 3, 4})` |
| `difference(other)` | Compare lists | `s.difference({2})` |

### Examples
```python
s = {1, 2, 3}

s.add(4)                          # add value -> {1, 2, 3, 4}
s.remove(2)                       # remove value, error if missing
s.discard(99)                     # remove safely, no error if missing

3 in s                            # membership test -> True
len(s)                            # count items

s.union({5, 6})                   # combine sets -> all unique values
s | {5, 6}                        # same as union

s.intersection({3, 4, 5})         # shared values only
s & {3, 4, 5}                     # same as intersection

s.difference({1, 4})              # values in s but not other set
s - {1, 4}                        # same as difference

for item in s:                    # iterate values
    print(item)
```

---

# 🔹 FILE HANDLING (Interview Mandatory)

```python
with open("file.txt", "r") as f:
    for line in f:
        line = line.strip()
```

### Modes
- `"r"` read
- `"w"` overwrite
- `"a"` append

### Examples
```python
with open("file.txt", "r") as f:          # open file for reading
    content = f.read()                    # read entire file into one string

with open("file.txt", "r") as f:
    lines = f.readlines()                 # read all lines into list

with open("file.txt", "r") as f:
    for line in f:                        # iterate line by line
        line = line.strip()               # remove newline/whitespace
        print(line)

with open("output.txt", "w") as f:        # overwrite file
    f.write("hello\n")                    # write one string

with open("output.txt", "a") as f:        # append to file
    f.write("new log line\n")
```

---

# 🔹 COMPREHENSIONS (Must Know)

### Matrix

| Type | Syntax | Example | What It Does |
|------|--------|---------|--------------|
| List | `[expr for x in data]` | `[x * 2 for x in [1, 2, 3]]` | build a new list |
| List + filter | `[expr for x in data if cond]` | `[x for x in [1, -1, 2] if x > 0]` | build filtered list |
| Dict | `{k: v for k, v in pairs}` | `{k: v for k, v in [("a", 1), ("b", 2)]}` | build dictionary |
| Dict + filter | `{k: v for k, v in pairs if v > 1}` | `{k: v for k, v in [("a", 1), ("b", 2)] if v > 1}` | filtered dict |
| Set | `{x for x in data}` | `{x for x in [1, 1, 2, 3]}` | build unique-value set |

### Examples
```python
[x for x in [1, 2, 3]]                    # copy values into new list
[x * 2 for x in [1, 2, 3]]                # transform each item -> [2, 4, 6]
[x for x in [1, -1, 2, -2] if x > 0]      # filter positives -> [1, 2]

{k: v for k, v in [("a", 1), ("b", 2)]}   # build dict -> {"a": 1, "b": 2}
{k: v * 10 for k, v in {"a": 1, "b": 2}.items()}  # transform dict values
{k: v for k, v in {"a": 1, "b": 2}.items() if v > 1}  # filter dict

{x for x in [1, 1, 2, 2, 3]}              # build set of unique values -> {1, 2, 3}
{x * 2 for x in [1, 2, 3]}                # transformed set -> {2, 4, 6}
```

---

# 🔹 EXCEPTION HANDLING

```python
try:
    risky()
except Exception as e:
    print(e)
```

### Examples
```python
try:
    x = int("123")                        # code that may fail
except ValueError as e:
    print(e)                              # handle specific error

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(e)                              # handle divide-by-zero

try:
    data = {"a": 1}
    print(data["missing"])
except KeyError as e:
    print(e)                              # handle missing dict key

try:
    risky()
except Exception as e:
    print(e)                              # catch broad exception as fallback
```

---

# 🔹 TYPE MEMORY

| Type | Mutable? | Example Update? |
|------|----------|-----------------|
| `str` | ❌ | `s.replace("a", "b")` returns new string |
| `list` | ✅ | `lst.append(1)` changes original list |
| `dict` | ✅ | `d["x"] = 1` changes original dict |
| `set` | ✅ | `s.add(1)` changes original set |
| `tuple` | ❌ | cannot change item after creation |
| `int/float` | ❌ | `x += 1` creates new value |

### Examples
```python
s = "abc"
s.replace("a", "z")                # returns new string, original unchanged unless reassigned

lst = [1, 2]
lst.append(3)                      # mutable -> original list changes

d = {"a": 1}
d["b"] = 2                         # mutable -> original dict changes

st = {1, 2}
st.add(3)                          # mutable -> original set changes

t = (1, 2, 3)                      # immutable -> cannot do t[0] = 99

x = 5
x += 1                             # new integer value is assigned to x
```

---

# 🔥 MUST-INSTANTLY-KNOW EXAMPLES

```python
# Count frequencies using dict
freq = {}
for item in ["a", "b", "a"]:
    freq[item] = freq.get(item, 0) + 1

# Parse a log file
with open("app.log", "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("ERROR"):
            print(line)

# Merge two dicts
a = {"host": "localhost"}
b = {"port": 8080}
a.update(b)

# Remove duplicates using set
unique_ips = list(set(["1.1.1.1", "1.1.1.1", "2.2.2.2"]))

# Loop with enumerate
for i, value in enumerate(["cpu", "mem", "disk"]):
    print(i, value)

# Loop two lists with zip
for host, ip in zip(["web1", "web2"], ["10.0.0.1", "10.0.0.2"]):
    print(host, ip)

# Sort by value using sorted
pairs = [("cpu", 70), ("mem", 40), ("disk", 90)]
sorted_pairs = sorted(pairs, key=lambda x: x[1])

# Handle missing keys safely
config = {"timeout": 30}
retries = config.get("retries", 3)

# Use list comprehension
evens = [x for x in range(10) if x % 2 == 0]

# Use dict comprehension
squares = {x: x**2 for x in range(5)}

# Read a file line-by-line
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())
```

---

You should instantly know how to:

- Count frequencies using dict
- Parse a log file
- Merge two dicts
- Remove duplicates using set
- Loop with enumerate
- Loop two lists with zip
- Sort by value using sorted
- Handle missing keys safely
- Use list/dict comprehensions
- Read a file line-by-line
