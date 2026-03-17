## Functional Python Helpers and Comprehensions

### Quick Reference Links
- [Functional helpers overview](#functional-helpers-overview)
- [map()](#map)
- [filter()](#filter)
- [reduce()](#reduce)
- [max / min](#max-min)
- [Functional helpers comparison matrix](#functional-helpers-comparison)
- [Chaining map → filter → reduce](#map-filter-reduce-chain)
- [Comprehensions overview](#comprehensions-overview)
- [List comprehension](#list-comprehension)
- [Dictionary comprehension](#dictionary-comprehension)
- [Set comprehension](#set-comprehension)
- [Generator expression](#generator-expression)
- [Tuple comprehension note](#tuple-comprehension)
- [Comprehension comparison matrix](#comprehension-comparison)
- [List vs generator](#list-vs-generator)
- [Functional helpers vs comprehensions](#helpers-vs-comprehensions)
- [Fruit example](#fruit-example)
- [Fast copy section](#fast-copy)

---

## Functional helpers overview
<a id="functional-helpers-overview"></a>

Functional helpers are built-in tools or standard-library tools that help you:
- transform data
- filter data
- combine data
- find best or smallest values

Included here:
- `map()`
- `filter()`
- `reduce()`
- `max()`
- `min()`

---

## map()
<a id="map"></a>

### What it does
`map()` applies a function to every item in an iterable and returns a lazy map object.

### Syntax
```python
map(FUNCTION, ITERABLE)

map(lambda ARG: EXPRESSION, ITERABLE)

map(lambda x, y: EXPRESSION, ITERABLE_1, ITERABLE_2)

map(lambda x: VALUE_IF_TRUE if CONDITION else VALUE_IF_FALSE, ITERABLE)
```

### Example
```python
numbers = [1,2,3,4]
doubled = map(lambda x: x*2, numbers)
print(list(doubled))  # [2,4,6,8]
```

---

## filter()
<a id="filter"></a>

### Syntax
```python
filter(lambda ARG: CONDITION, ITERABLE)
```

### Example
```python
numbers = [1,2,3,4]

evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))  # [2,4]
```

---

## reduce()
<a id="reduce"></a>

### Syntax
```python
from functools import reduce

reduce(lambda ACC, ITEM: EXPRESSION, ITERABLE)
reduce(lambda ACC, ITEM: EXPRESSION, ITERABLE, INITIAL_VALUE)
```

### Example
```python
from functools import reduce

numbers = [1,2,3,4]
total = reduce(lambda x,y: x+y, numbers)

print(total)  # 10

# basic
reduce(FUNCTION, ITERABLE)

# lambda form
reduce(lambda ACC, ITEM: EXPRESSION, ITERABLE)

# with initializer
reduce(lambda ACC, ITEM: EXPRESSION, ITERABLE, INITIAL_VALUE)

# with condition
reduce(lambda acc, x: acc + x if CONDITION else acc, ITERABLE, INITIAL_VALUE)
```

---

## max / min
<a id="max-min"></a>

### Syntax
```python
max(ITERABLE)
min(ITERABLE)

max(ITERABLE, key=FUNCTION)
min(ITERABLE, key=FUNCTION)
```

### Example
```python
words = ["apple","banana","kiwi"]

print(max(words, key=len))  # banana
print(min(words, key=len))  # kiwi
```

---

## Comprehensions overview
<a id="comprehensions-overview"></a>

Comprehensions are compact syntax for creating collections.

Types:

- list comprehension
- dictionary comprehension
- set comprehension
- generator expression
- tuple construction

---

## List comprehension
<a id="list-comprehension"></a>

### Syntax
```python
[EXPRESSION for ITEM in ITERABLE]

[EXPRESSION for ITEM in ITERABLE if CONDITION]

[VALUE_IF_TRUE if CONDITION else VALUE_IF_FALSE for ITEM in ITERABLE]
```

### Example
```python
numbers = [1,2,3,4]

doubled = [x*2 for x in numbers]
print(doubled)  # [2,4,6,8]
```

---

## Dictionary comprehension
<a id="dictionary-comprehension"></a>

### Syntax
```python
{KEY: VALUE for ITEM in ITERABLE}

{KEY: VALUE for ITEM in ITERABLE if CONDITION}
```

### Example
```python
numbers = [1,2,3,4]

squares = {x: x**2 for x in numbers}
print(squares)
```

---

## Set comprehension
<a id="set-comprehension"></a>

### Syntax
```python
{EXPRESSION for ITEM in ITERABLE}
```

### Example
```python
numbers = [1,2,2,3]

unique = {x for x in numbers}
print(unique)  # {1,2,3}
```

---

## Generator expression
<a id="generator-expression"></a>

### Syntax
```python
(EXPRESSION for ITEM in ITERABLE)
```

### Example
```python
numbers = [1,2,3]

gen = (x*2 for x in numbers)

print(list(gen))  # [2,4,6]
```

---

## Tuple comprehension note
<a id="tuple-comprehension"></a>

Python **does not support true tuple comprehensions**.

To build a tuple:

```python
tuple(EXPRESSION for ITEM in ITERABLE)
```

Example:

```python
numbers = [1,2,3]

t = tuple(x*2 for x in numbers)
print(t)  # (2,4,6)
```

---

## Fast copy
<a id="fast-copy"></a>

```python
# map
map(lambda x: x*2, items)

# filter
filter(lambda x: x>0, items)

# reduce
from functools import reduce
reduce(lambda acc,x: acc+x, items)

# list comprehension
[x for x in items]

# dictionary comprehension
{k:v for k,v in items}

# set comprehension
{x for x in items}

# generator
(x for x in items)

# tuple
tuple(x for x in items)
```