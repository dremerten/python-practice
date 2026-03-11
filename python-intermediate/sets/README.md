# Python Sets & Frozensets — Detailed Reference

---

# Creating a `set` or `frozenset`

## `set`
A **set** is an unordered collection of **unique elements**.

Properties:
- Unordered (no indexing or guaranteed order)
- Mutable (items can be added or removed)
- Stores **only unique values**
- Elements must be **hashable** (immutable types like `int`, `str`, `tuple`)

Example:

```python
numbers = {1, 2, 3, 4}
```

Duplicates are automatically removed:

```python
numbers = {1, 2, 2, 3}
print(numbers)
# {1, 2, 3}
```

### Ways to Create a `set`

#### 1. Curly Braces `{}`

```python
my_set = {1, 2, 3}
```

⚠️ Note:

```python
{}       # creates a dictionary
set()    # creates an empty set
```

Example:

```python
empty_set = set()
```

---

#### 2. `set()` Constructor

Used when converting other iterables into sets.

```python
numbers = set([1, 2, 3, 3])
print(numbers)

# {1, 2, 3}
```

Examples:

```python
set("hello")      # {'h','e','l','o'}
set(range(5))     # {0,1,2,3,4}
```

---

#### 3. Set Comprehension

Works similar to list comprehension.

```python
squares = {x**2 for x in range(5)}
print(squares)

# {0,1,4,9,16}
```

Useful for generating unique computed values.

---

## `frozenset`

A **frozenset** is an **immutable version of a set**.

Properties:

- Immutable (cannot add/remove elements)
- Hashable
- Can be used as dictionary keys
- Still supports mathematical operations (union, intersection, etc.)

Creation:

```python
f = frozenset([1, 2, 3])
print(f)

# frozenset({1,2,3})
```

Mutation is not allowed:

```python
f.add(4)
# AttributeError
```

---

# Adding Items to a Set

Only **regular sets** support adding elements.

`frozenset` does **not** allow modification.

---

## `.add()`

Adds **one element** to a set.

Example:

```python
my_set = {1,2,3}

my_set.add(4)

print(my_set)

# {1,2,3,4}
```

If the element already exists, nothing changes:

```python
my_set.add(4)
print(my_set)

# {1,2,3,4}
```

---

## `.update()`

Adds **multiple elements** at once from an iterable.

Example:

```python
my_set = {1,2}

my_set.update([3,4,5])

print(my_set)

# {1,2,3,4,5}
```

Works with many iterable types:

```python
my_set.update((6,7))
my_set.update({8,9})
my_set.update("ab")
```

Result might look like:

```
{1,2,3,4,5,6,7,8,9,'a','b'}
```

---

# Removing Items from a Set

---

## `.remove()`

Removes a specific element.

Example:

```python
my_set = {1,2,3}

my_set.remove(2)

print(my_set)

# {1,3}
```

⚠️ Raises an error if the element does not exist.

```python
my_set.remove(10)

# KeyError
```

---

## `.discard()`

Removes an element **without throwing an error** if it doesn't exist.

Example:

```python
my_set = {1,2,3}

my_set.discard(10)

print(my_set)

# {1,2,3}
```

This makes `.discard()` safer when you aren't sure if the item exists.

---

# Finding Elements

The `in` keyword checks membership.

Example:

```python
my_set = {1,2,3}

if 2 in my_set:
    print("Element found")
```

Output:

```
Element found
```

Membership checks in sets are **very fast (O(1) average)** because sets use a **hash table** internally.

---

# Union

Union combines **all unique elements from both sets**.

Example sets:

```python
set1 = {1,2,3}
set2 = {3,4,5}
```

---

## `.union()` Method

```python
result = set1.union(set2)

print(result)

# {1,2,3,4,5}
```

---

## `|` Operator

Shorthand operator:

```python
result = set1 | set2
```

Both methods return a **new set**.

---

# Intersection

Intersection returns **only elements present in both sets**.

Example:

```python
set1 = {1,2,3}
set2 = {2,3,4}
```

---

## `.intersection()` Method

```python
result = set1.intersection(set2)

print(result)

# {2,3}
```

---

## `&` Operator

Short syntax:

```python
result = set1 & set2
```

---

# Difference

Difference returns elements **in the first set but not the second**.

Example:

```python
set1 = {1,2,3}
set2 = {2,3,4}
```

---

## `.difference()` Method

```python
result = set1.difference(set2)

print(result)

# {1}
```

---

## `-` Operator

Short syntax:

```python
result = set1 - set2
```

Meaning:

```
elements in set1 but not in set2
```

---

# Symmetric Difference

Returns elements **that exist in one set OR the other but not both**.

Example:

```python
set1 = {1,2,3}
set2 = {3,4,5}
```

---

## `.symmetric_difference()` Method

```python
result = set1.symmetric_difference(set2)

print(result)

# {1,2,4,5}
```

---

## `^` Operator

Short syntax:

```python
result = set1 ^ set2
```

Meaning:

```
(all elements from both sets) minus (their intersection)
```

---

# Quick Mental Model

```
Union                  → everything
Intersection           → overlap
Difference             → what A has but B doesn't
Symmetric Difference   → non-overlapping elements
```

Example:

```
A = {1,2,3}
B = {3,4,5}

A | B  → {1,2,3,4,5}
A & B  → {3}
A - B  → {1,2}
A ^ B  → {1,2,4,5}
```

---

# Summary

| Operation | Method | Operator | Description |
|-----------|--------|---------|-------------|
| Union | `set1.union(set2)` | `set1 \| set2` | Combine all unique elements |
| Intersection | `set1.intersection(set2)` | `set1 & set2` | Elements in both sets |
| Difference | `set1.difference(set2)` | `set1 - set2` | Elements only in first set |
| Symmetric Difference | `set1.symmetric_difference(set2)` | `set1 ^ set2` | Elements in either set but not both |

---

# Key Takeaways

- Sets store **unique unordered values**
- Membership testing is **very fast**
- Sets are **mutable**, `frozenset` is **immutable**
- Set math operations are highly optimized
- Common operators:

```
|  union
&  intersection
-  difference
^  symmetric difference
```