"""
# This code defines a generator function `get_student_ids` that yields student IDs from 1 to MAX_STUDENTS.
# The generator can receive a new student ID through `send()`, which updates the `student_id` value.
# The `for` loop iterates through the student IDs and when it encounters the first ID (1), it sends 25 to the generator.
# This causes the generator to update the `student_id` to 25 and continue from there.
"""

MAX_STUDENTS = 500

def get_student_ids():
  student_id = 1
  while student_id <= MAX_STUDENTS:
    n = yield student_id 
    if n is not None:
      student_id = n
      continue
    student_id += 1

student_id_generator = get_student_ids()
for i in student_id_generator:
  if i == 1:
    i = student_id_generator.send(350)
  print(i)