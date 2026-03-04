"""
map()

When called, map() applies the passed function to each and every element in the iterable and returns a map object. 
The returned map object holds the results from applying the mapping function to each element in the passed iterable. 
We will usually convert the map into a list to enable viewing and further use. 
"""

n = 15

def fib(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n -1):
        a, b = b, a + b
    return b

fibonacci_sequence = list(map(fib, range(n)))
print(fibonacci_sequence)