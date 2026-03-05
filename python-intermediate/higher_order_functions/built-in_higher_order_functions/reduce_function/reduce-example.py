"""
Lastly, we have the reduce() function, which has two distinct differences from the built-in higher-order functions that we have learned so far.
In contrast to the map() and filter() functions that are always available, 
the reduce() function must be imported from the functools module to use it.
Rather than returning a reduce object as might be expected after 
learning about map() and filter(), reduce() returns a single value. 
To get to this single value, reduce() cumulatively applies a passed function to each sequential pair of elements in an iterable.
"""

from functools import reduce
 
int_list = [3, 6, 9, 12]
reduced_int_list = reduce(lambda x,y: x*y, int_list) 
print(reduced_int_list)

'''

The reduce() function takes 2 arguments: a lambda function and a list of integers.
The lambda function takes 2 numbers, x and y and multiplies them together.
The reduce() function applies the lambda function to the first two elements in the list, 3 and 6, to get a product of 18.
Next, 18 was multiplied by the following element in the list, 9, to get 162.
Continuing on, 162 was multiplied by the next element, 12, to get 1944.
This last, final value—1944—is what was returned by reduce().

This process was essentially the same as multiplying 3*6*9*12. 
'''

'''
from functools import reduce

letters = ['r', 'e', 'd', 'u', 'c', 'e']

# your code below:
word = reduce(lambda x,y: str(x+y), letters )
# remember to import the reduce function
print(word)
'''