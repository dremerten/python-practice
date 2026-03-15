"""
This code defines a times3() function 
that multiplies the result of an add or subtract (sub) function by three and returns the value. 
The times3() function also allows the passing 
of any other function that accepts two parameters and returns an integer.
"""

# def add(x, y):
#   return x + y

# def sub(x, y):
#   return x - y

# def times3(a, b, function):
#   return 3 * function(a, b)

# result_add = add_then_times3 = times3(2, 4, add) # 18
# result_sub = sub_then_times3 = times3(2, 4, sub) # -6
# print(result_add)
# print(result_sub)

"""
Functional programming promotes the concept of brevity 
when writing code. It is important to be concise and write functions 
in as few lines as possible as long as readability is maintained. 
We can also pass a function to another function by writing it in the argument using a lambda.

We can shorten the previous code using a lambda like so:
"""

def times3(a, b, function):
  return 3 * function(a, b)

add_then_times3 = times3(2, 4, lambda x, y: x + y) # 18
sub_then_times3 = times3(2, 4, lambda x, y: x - y) # -6

"""
This will output the same result as the verbose implementation from earlier. 
Lambdas are a great tool as they allow a programmer to write a function 
while maintaining the flow of ideas. A programmer is no longer required to stop, 
write a function elsewhere, and then resume work. 
A drawback of lambdas is that they are only suitable for implementing simple functions; 
it is not possible to write all functions as lambdas!
"""