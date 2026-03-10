"""
Generator Pipeline

A generator pipeline is a chain of generators where the output of one feeds into the next, similar to Unix pipes.

Visual
Data Source
     │
     ▼
Generator A  (filter)
     │
     ▼
Generator B  (transform)
     │
     ▼
Generator C  (aggregate)
     │
     ▼
Final Output
"""

def read_numbers():
    for i in range(30):
        yield i

def filter_even(nums):
    for n in nums:
        if n % 2 == 0:
            yield n

def square(nums):
    for n in nums:
        yield n * n

pipeline = square(filter_even(read_numbers()))

for x in pipeline:
    print(x)