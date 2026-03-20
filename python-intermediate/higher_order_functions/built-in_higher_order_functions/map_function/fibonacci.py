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
    # initialize first two Fibonacci numbers
    a, b = 0, 1
    for _ in range(n - 1):
        # simultaneously update a to b and b to a+b
        a, b = b, a + b
    return b

# generate the first n Fibonacci numbers by applying fib to 0..n-1
fibonacci_sequence = list(map(fib, range(n)))
print(fibonacci_sequence)