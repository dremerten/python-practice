# 🐍 Python 3 — 1 Page MUST MEMORIZE (DevOps Edition)

---

# 🔹 CORE BUILT-INS

| Function | Why It Matters |
|-----------|----------------|
| `len(x)` | Count items |
| `type(x)` | Know your data |
| `isinstance(x, t)` | Safe type checks |
| `sorted(x)` | Sort iterable |
| `min(x)` / `max(x)` | Boundaries |
| `sum(x)` | Totals |
| `any(x)` | Any True? |
| `all(x)` | All True? |
| `enumerate(x)` | Index + value |
| `zip(a, b)` | Parallel iteration |
| `range(n)` | Controlled loops |

---

# 🔹 STRING (`str`)

```python
s = "hello world"
```

| Method | Use Case |
|---------|----------|
| `s.strip()` | Clean input/log lines |
| `s.split()` | Parse data |
| `" ".join(lst)` | Build strings |
| `s.replace(a, b)` | Normalize text |
| `s.startswith(x)` | Log filtering |
| `s.endswith(x)` | Extension checks |
| `s.count(x)` | Frequency check |

---

# 🔹 LIST (`list`)

```python
lst = [1, 2, 3]
```

| Method | Use Case |
|---------|----------|
| `append(x)` | Add item |
| `extend(iterable)` | Merge lists |
| `pop()` | Remove last |
| `remove(x)` | Remove value |
| `sort()` | Sort in place |
| `reverse()` | Reverse order |
| `copy()` | Avoid mutation bugs |

---

# 🔹 DICTIONARY (`dict`) ⭐ MOST IMPORTANT

```python
d = {"a": 1}
```

| Method | DevOps Use |
|---------|-------------|
| `d.get(k)` | Safe access |
| `d.get(k, default)` | Avoid KeyError |
| `d.setdefault(k, v)` | Nested counting |
| `d.update(other)` | Merge configs |
| `d.items()` | Loop key/value |
| `d.keys()` | Iterate keys |
| `d.values()` | Iterate values |
| `d.pop(k)` | Remove key |

🔥 If you can’t confidently use `setdefault()` — fix that.

---

# 🔹 SET (`set`)

```python
s = {1, 2, 3}
```

| Method | Use Case |
|---------|----------|
| `add(x)` | Insert |
| `remove(x)` | Remove |
| `discard(x)` | Safe remove |
| `union(other)` | Combine |
| `intersection(other)` | Overlap |
| `difference(other)` | Compare lists |

---

# 🔹 FILE HANDLING (Interview Mandatory)

```python
with open("file.txt", "r") as f:
    for line in f:
        line = line.strip()
```

Modes:
- `"r"` read
- `"w"` overwrite
- `"a"` append

---

# 🔹 COMPREHENSIONS (Must Know)

List:
```python
[x for x in data if x > 0]
```

Dict:
```python
{k: v for k, v in pairs}
```

Set:
```python
{x for x in data}
```

---

# 🔹 EXCEPTION HANDLING

```python
try:
    risky()
except Exception as e:
    print(e)
```

---

# 🔹 TYPE MEMORY

| Type | Mutable? |
|------|----------|
| `str` | ❌ |
| `list` | ✅ |
| `dict` | ✅ |
| `set` | ✅ |
| `tuple` | ❌ |
| `int/float` | ❌ |

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

If you hesitate on any of these — drill it.

