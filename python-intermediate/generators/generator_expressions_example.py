"""
Generator expressions allow for a clean, single-line definition and creation of an iterator. 
By using a generator expression, there is no need to define a full generator function as we covered in the previous exercises.

Generator expressions resemble the syntax of list comprehensions. However, they do differ in the following ways:

Generator Expressions 	           |        List Comprehensions
-----------------------------------------------------------------
Returns a newly defined iterator   |	    Returns a new list
Uses parentheses 	               |        Uses brackets

"""

# List comprehension
a_list = [i*i for i in range(20)]

# Generator comprehension
a_generator = (i*i for i in range(20))

'''
[0, 1, 4, 9]
<generator object <genexpr> at 0x7f82e0e4d4c0>
'''
print(a_list)
print(a_generator)

"""
Since our generator expression returns an iterator object, we can loop through to obtain the values within it:
"""
for i in a_generator:
    print(i)

def cs_generator():
  for i in range(1,5):
    yield "Computer Science " + str(i)

# generator object
cs_courses = cs_generator()
for course in cs_courses:
  print(course)

# generator comprehension (expression)
cs_generator_exp = ("Computer Science " + str(i) for i in range(1, 5))

for course in cs_generator_exp:
  print(course)