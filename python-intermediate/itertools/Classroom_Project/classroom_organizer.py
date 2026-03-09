from roster import student_roster
import itertools

class ClassroomOrganizer:
  def __init__(self):
    self.sorted_names = self._sort_alphabetically(student_roster)
    self.index = 0

  def __iter__(self):
    return self

  def __next__(self):
    if self.index >= len(self.sorted_names):
      raise StopIteration
    name = self.sorted_names[self.index]
    self.index += 1
    return name

  def _sort_alphabetically(self,students):
    names = []
    for student_info in students:
      name = student_info['name']
      names.append(name)
    return sorted(names)

  def get_students_with_subject(self, subject):
    selected_students = []
    for student in student_roster:
      if student['favorite_subject'] == subject:
        selected_students.append((student['name'], subject))
    return selected_students

  def student_seating(self):
        student_combinations = list(itertools.combinations(self.sorted_names, 2))
        tables = []
        for i in range(0, len(student_combinations), 5):  # group by 5 tables
            tables.append(student_combinations[i:i+5])
        return tables

  def get_students_for_afterschool(self):
    math_students = self.get_students_with_subject("Math")
    science_students = self.get_students_with_subject("Science")
    combined_students = math_students + science_students
    group_combinations = list(itertools.combinations(combined_students, 4))
    return group_combinations
  

# Create organizer
classroom = ClassroomOrganizer()

# Get the combinations for afterschool program (Math + Science students)
afterschool_groups = classroom.get_students_for_afterschool()

# Print the result as a list
print(afterschool_groups)