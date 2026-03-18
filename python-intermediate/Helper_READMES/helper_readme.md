# Functional Python Helpers & Comprehensions

---

## Quick Jump
- [map](#map)
- [filter](#filter)
- [reduce](#reduce)
- [max / min](#max--min)
- [Comprehensions](#comprehensions)
- [Comparison](#comparison)
- [Pipeline Pattern](#pipeline-pattern)
- [Fast Copy](#fast-copy)

---

## map
<a id="map"></a>

### Use when:
Transform every item

### Syntax
```python
map(lambda x: EXPRESSION, iterable)
map(lambda x, y: EXPRESSION, iter1, iter2)
map(lambda x: A if cond else B, iterable)
```

### Example
```python
nums = [1,2,3,4]
print(list(map(lambda x: x*2, nums)))  # [2,4,6,8]
```

---

## filter
<a id="filter"></a>

### Use when:
Keep items matching a condition

### Syntax
```python
filter(lambda x: CONDITION, iterable)
```

### Example
```python
nums = [1,2,3,4]
print(list(filter(lambda x: x%2==0, nums)))  # [2,4]
```

---

## reduce
<a id="reduce"></a>

### Use when:
Collapse iterable → single value

### Syntax
```python
from functools import reduce

reduce(lambda acc, x: EXPRESSION, iterable)
reduce(lambda acc, x: EXPRESSION, iterable, initial)
```

### Example
```python
from functools import reduce

nums = [1,2,3,4]
print(reduce(lambda x,y: x+y, nums))  # 10
```

---

## max / min
<a id="max--min"></a>

### Use when:
Find best item

### Syntax
```python
max(iterable)
min(iterable)

max(iterable, key=func)
min(iterable, key=func)
```

### Example
```python
words = ["a","abc","ab"]
print(max(words, key=len))  # "abc"
```

---

## Comprehensions
<a id="comprehensions"></a>

### List
```python
[x for x in items]
[x for x in items if cond]
[a if cond else b for x in items]
```

```python
nums = [1,2,3,4]
print([x*2 for x in nums])  # [2,4,6,8]
```

---

### Dictionary
```python
{k:v for x in items}
{k:v for x in items if cond}
```

```python
nums = [1,2,3]
print({x:x**2 for x in nums})
```

---

### Set
```python
{x for x in items}
{x for x in items if cond}
```

```python
nums = [1,2,2,3]
print({x for x in nums})  # {1,2,3}
```

---

### Generator (lazy)
```python
(x for x in items)
(x for x in items if cond)
```

```python
nums = [1,2,3]
gen = (x*2 for x in nums)
print(list(gen))  # [2,4,6]
```

---

### Tuple (pattern)
```python
tuple(x for x in items)
```

```python
nums = [1,2,3]
print(tuple(x*2 for x in nums))  # (2,4,6)
```

---

## Comparison
<a id="comparison"></a>

| Tool | Purpose | Lazy |
|---|---|---|
| map | transform | Yes |
| filter | select | Yes |
| reduce | combine | No |
| list comp | build list | No |
| generator | stream values | Yes |

---

## Pipeline Pattern
<a id="pipeline-pattern"></a>

```python
reduce(
    lambda acc, x: acc + x,
    filter(
        lambda x: x % 2 == 0,
        map(lambda x: x * 10, data)
    )
)
```

Flow:
```
map → filter → reduce
```

---

## Fast Copy
<a id="fast-copy"></a>

```python
# map
map(lambda x: x*2, items)

# filter
filter(lambda x: x>0, items)

# reduce
from functools import reduce
reduce(lambda acc,x: acc+x, items)

# max/min
max(items)
min(items)
max(items, key=len)

# list
[x for x in items]

# dict
{k:v for k,v in items}

# set
{x for x in items}

# generator
(x for x in items)

# tuple
tuple(x for x in items)
```