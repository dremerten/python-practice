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

| Method | Description |
|---------|-------------|
| `t.count(x)` | Count value |
| `t.index(x)` | Find index |

---

# 🔹 5. DICTIONARY METHODS (`dict`)

```python
d = {"a": 1, "b": 2}
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

---

# 🔹 8. ITERATION HELPERS

| Function | Why It’s Powerful |
|-----------|-------------------|
| `range()` | Loop control |
| `enumerate()` | Index + value |
| `zip()` | Parallel iteration |
| `dict()` | Build dict from tuples |
| `list()` | Convert iterable |
| `set()` | Remove duplicates |

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

