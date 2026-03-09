"""
We have a collection of 5,000 students.

We only want to retrieve information on the first 100 students. 
Use the throw() method to throw a ValueError of “Invalid student ID” if the iterated student ID goes over 100
"""


def student_counter():
  for i in range(1,5001):
    yield i

student_generator = student_counter()
for student_id in student_generator:
  if student_id > 100:
    student_generator.throw(ValueError, "Invalid student ID")
  print(student_id)

