"""
There are some cases where it is useful to connect multiple
generators
Preview: Docs Loading link description
into one. This allows us to delegate the operations of one generator to another sub-generator. Connecting generators is similar to using the itertools chain() function to combine
iterators
Preview: Docs Loading link description
into a single iterator.

In order to connect generators, we use the yield from statement. An example of how it is used is below:
"""

# def cs_courses():
#     yield 'Computer Science'
#     yield 'Artificial Intelligence'

# def art_courses():
#     yield 'Intro to Art'
#     yield 'Selecting Mediums'


# def all_courses():
#     yield from cs_courses()
#     yield from art_courses()

# combined_generator = all_courses()

def science_students(x):
  for i in range(1,x+1):
    yield i

def non_science_students(x,y):
  for i in range(x,y+1):
    yield i
  
# Write your code below
def combined_students():
  yield from science_students(5)
  yield from non_science_students(10, 15)
  yield from non_science_students(25, 30)

student_generator = combined_students()
for student in student_generator:
  print(student)