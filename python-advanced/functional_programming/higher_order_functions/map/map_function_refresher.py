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