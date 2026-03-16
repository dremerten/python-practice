## Functional Python Helper Examples

#### map() → transform items
```
numbers = [1, 2, 3, 4]
doubled = map(lambda x: x * 2, numbers)
print(list(doubled))  # [2, 4, 6, 8]
```
#### filter() → select items
```
numbers = [1, 2, 3, 4]
evens = filter(lambda x: x % 2 == 0, numbers)
print(list(evens))  # [2, 4]
```
#### max()/min() → find largest/smallest with key=
```
words = ["apple", "banana", "kiwi"]
longest_word = max(words, key=len)
shortest_word = min(words, key=len)
print(longest_word)  # "banana"
print(shortest_word) # "kiwi"
```
#### reduce() → combine items step by step
```
from functools import reduce
numbers = [1, 2, 3, 4]
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 10
```

#### Quick Comparison Matrix
| Function | Purpose | Takes key=? | Example |
|----------|---------|-------------|---------|
| map()    | Transform each item | ❌ | map(lambda x: x*2, [1,2,3]) → [2,4,6] |
| filter() | Keep items that meet a condition | ❌ | filter(lambda x: x>2, [1,2,3]) → [3] |
| max()/min() | Find largest/smallest | ✅ | max(["apple","banana"], key=len) → "banana" |
| reduce() | Combine items cumulatively | ❌ | reduce(lambda x,y: x+y, [1,2,3]) → 6 |


#### List Comprehension vs Generator Expression
| Feature | List Comprehension | Generator Expression |
|---|---|---|
| Syntax | `[x for x in items]` | `(x for x in items)` |
| Returns | list | generator |
| Memory | stores all values in memory | generates values one at a time |
| Speed | often faster for small datasets | better for very large datasets |


```
from functools import reduce

fruits = {"Grape": (4, 6, 2), 
          "Lemon": (7, 3, 1), 
          "Orange": (5, 8, 1), 
          "Apple": (2, 8, 10), 
          "Watermelon": (0, 9, 6)}

# 1 Original version using reduce + map
total_fruits_1 = reduce(lambda x, y: x + y, map(lambda key: fruits[key][0] + fruits[key][1] + fruits[key][2], fruits))
print("Original reduce+map:", total_fruits_1)

# 2 Generator comprehension version with reduce
total_fruits_2 = reduce(lambda x, y: x + y, (sum(fruits[key]) for key in fruits))
print("Generator comprehension + reduce:", total_fruits_2)

# 3 Pythonic version using just sum()
total_fruits_3 = sum(sum(fruits[key]) for key in fruits)
print("Pythonic sum():", total_fruits_3)
```