"""
An infinite iterator will repeat an infinite number of times
with
Preview: Docs Loading link description
no endpoint and no StopIteration exception raised. Infinite
iterators
Preview: Docs Loading link description
are useful when we have unbounded streams of data to process.

A useful itertool that is an infinite iterator is the
count()
Preview: Docs Loading link description
itertool. This infinite iterator will count
from
Preview: Docs Loading link description
a first value until we provide some type of stop condition. The base syntax of the function looks like this:

count(start,[step])


The first argument of count() is the value where we start counting from. The second argument is an optional step that will
return
Preview: Docs Loading link description
current value + step. The step value can be positive, negative, and an integer or float number. It will always default to 1 if not provided.

To show how it’s used in a scenario, suppose we want to quickly count up and print all even numbers from 0 to 20.
"""

# import itertools

# for i in itertools.count(start=0, step=2):
#   print(i)
#   if i >= 2000:
#     break

"""
We have several 13.5lb bags of dog food to display. 
Our single shelving unit however can only hold a maximum of 1,000lbs. 
Let’s figure out how many bags of food we can display! 
"""
import itertools

max_capacity = 1000
num_bags = 0

for bag in itertools.count(start=13.5, step=13.5):
  if bag >= max_capacity:
    break
  num_bags += 1

print(num_bags)