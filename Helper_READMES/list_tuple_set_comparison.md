# Python Set vs List vs Tuple — Lookup Cheat Sheet

## Big-O (Membership Check)
- Set:    O(1) average  → fastest
- List:   O(n)          → linear scan
- Tuple:  O(n)          → same as list

---

## Mental Model
- Set   → "Jump directly to item using a hash"
- List  → "Scan items one by one"
- Tuple → "Read-only list (still scans)"

---

## Membership Check Examples
```python
x in my_set    # fast (O(1))
x in my_list   # slow (O(n))
x in my_tuple  # slow (O(n))
```

---

## Why Sets Are Fast (Hashing)
```python
my_set = {"apple", "banana", "cherry"}

# Conceptual behavior:
# hash("banana") → direct location → check → done
```

- Uses hash table
- Direct access instead of scanning

---

## Why Lists & Tuples Are O(n)
```python
my_list = ["apple", "banana", "cherry"]
my_tuple = ("apple", "banana", "cherry")

"cherry" in my_list
"cherry" in my_tuple
```

Steps (conceptual):
```text
"apple"   ❌
"banana"  ❌
"cherry"  ✅
```

- Must check each element sequentially

---

## Performance Example
```python
big_list = list(range(1_000_000))
big_tuple = tuple(big_list)
big_set = set(big_list)

999999 in big_list   # up to 1,000,000 checks
999999 in big_tuple  # same as list → O(n)
999999 in big_set    # ~1–2 operations → O(1)
```

---

## Common Use Cases

### Set
```python
# Remove duplicates
unique = set([1, 2, 2, 3])

# Fast lookup
if 2 in unique:
    print("Found")

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}

print(a & b)  # {2, 3}
print(a | b)  # {1, 2, 3, 4}
print(a - b)  # {1}
```

---

### List
```python
# Ordered, mutable
data = [1, 2, 3]
data.append(4)

# Indexing
print(data[0])  # 1
```

---

### Tuple
```python
# Immutable (cannot change)
point = (10, 20)

# Valid as dict key
d = {(1, 2): "value"}

# Membership check (still O(n))
3 in (1, 2, 3, 4)
```

---

## Trade-offs

### Use a SET when:
- You need fast membership checks
- You want unique values
- Order does NOT matter

### Use a LIST when:
- Order matters
- You need indexing
- You need to modify data

### Use a TUPLE when:
- Data should not change
- You want a lightweight, fixed structure
- You need hashable keys

---

## Key Limitations

### Set
- Unordered
- No indexing
- Only hashable items allowed

### Tuple
- Cannot modify after creation

---

## Comparison Table

| Feature            | Set            | List           | Tuple          |
|--------------------|----------------|----------------|----------------|
| Lookup speed       | O(1) avg       | O(n)           | O(n)           |
| Mutable            | ❌ No          | ✅ Yes         | ❌ No          |
| Ordered            | ❌ No          | ✅ Yes         | ✅ Yes         |
| Duplicates         | ❌ No          | ✅ Yes         | ✅ Yes         |
| Hashable           | ✅ Yes         | ❌ No          | ✅ Yes         |
| Indexing           | ❌ No          | ✅ Yes         | ✅ Yes         |

---

## One-line Rules
👉 If you're doing a lot of `x in collection` → use a SET  
👉 If you need order + editing → use a LIST  
👉 If data should never change → use a TUPLE