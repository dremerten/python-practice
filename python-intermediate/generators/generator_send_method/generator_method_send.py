"""
This generator creates a counter that can optionally be reset using send().

How it works:

1. The generator starts with count = 0 and runs forever in a while True loop.

2. The line:
       n = yield count
   does two things:
   - It yields (returns) the current value of count.
   - When the generator resumes, it receives a value into n.

3. If the generator is resumed with next(), nothing is sent in,
   so n becomes None.

4. If the generator is resumed with send(value),
   that value is assigned to n.

5. If n is not None, the generator resets count to that value.

6. Then count is incremented by 1 before the next iteration.

Step-by-step execution:

my_generator = generator()

next(my_generator)
- Starts the generator
- count = 0
- yield count → returns 0

next(my_generator)
- Resume after yield
- n = None (because next() sends nothing)
- count += 1 → count = 1
- yield count → returns 1

my_generator.send(3)
- Resume after yield
- n = 3
- count = 3
- count += 1 → count = 4
- yield count → returns 4

next(my_generator)
- Resume after yield
- n = None
- count += 1 → count = 5
- yield count → returns 5

So the outputs are:
0, 1, 4, 5

Conceptually the counter behaves like:
0 → 1 → (jump to 3) → 4 → 5 → 6 ...
"""

def generator():
  count = 0
  while True:
    n = yield count
    if n is not None:
      count = n
    count += 1

my_generator = generator()
print(next(my_generator)) # Output: 0
print(next(my_generator)) # Output: 1
print(my_generator.send(3)) # Output: 4
print(next(my_generator)) # Output: 5

