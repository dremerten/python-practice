""" 
def squared(x):
  return x * x

def cubed(x):
  return x*x*x
"""

def odd_or_even(n):
    square = lambda x: x*x
    cube = lambda x: x*x*x
    return square(n) if n % 2 == 0 else cube(n)