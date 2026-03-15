"""
A lambda function is a short
anonymous function that can accept several parameters but only returns one value. 
Lambdas can be stored as a variable or defined inline in the accepting function.
"""


###### Example without using lambda #####
"""
def rectangle(base, height):
  return base * height

def triangle(base, height):
  return 0.5 * (base * height)

# price: price per square meter
# dimension: dimensions tuple
def total_cost(price: float, dimension: tuple, area):
  return float(price) * area(dimension[0], dimension[1])

print(total_cost(3, (5, 5), rectangle)) 
print(total_cost(4, (6, 7), triangle)) 
"""

##### Example using lambda #####

# price: price per square meter
# dimension: dimensions tuple
def total_cost(price: float, dimension: tuple, area):
 return float(price) * area(dimension[0], dimension[1])

# print(total_cost(3.50, (5, 5), lambda base, height: base*height)) 
# print(total_cost(4, (6, 7), lambda base, height: 0.5 * base*height)) 

# Lambda functions can be stored in a variable like so:
rectangle = lambda x, y: x * y
triangle = lambda x, y: 0.5 * x * y

print(rectangle(5, 6))