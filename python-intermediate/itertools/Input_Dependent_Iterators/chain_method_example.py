"""
An input-dependent iterator will terminate based on the length of one or more input values.
They are great for working with and modifying existing iterators.

A useful itertool that is an input-dependent iterator is the chain() itertool.
chain() takes in one or more iterables and combine them into a single iterator.
Here is what the base syntax looks like:

chain(*iterables)

The input value of chain() is one or more iterables of the same or varying iterable types.
For example, we could use the chain() itertool to combine a list and a set into one iterator.

To show how it’s used in a scenario, suppose we want to combine a list containing odd numbers
and a set containing even numbers:

import itertools

odd = [5, 7, 9]
even = {6, 8, 10}

all_numbers = itertools.chain(odd, even)

for number in all_numbers:
    print(number)

The above example:
- Imports the itertools module.
- Sets all_numbers to the iterator returned by the itertool chain().
- Uses the list iterable odd and the set iterable even as the arguments to chain().
- Implements a for loop using the iterator in all_numbers.
- Prints the results, which will be:

5
7
9
8
10
6

The output is finite since the input iterables, odd and even are also finite.
Note that Python sets are not ordered, so the last 3 numbers in this example’s
output will not always be in the initialized order.
"""

import itertools

great_dane_foods = [2439176, 3174521, 3560031]
min_pin_pup_foods = [6821904, 3302083]
pawsome_pup_foods = [9664865]

all_skus_iterator = itertools.chain(great_dane_foods, min_pin_pup_foods, pawsome_pup_foods)

for sku in all_skus_iterator:
  print(sku)