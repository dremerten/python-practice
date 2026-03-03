class Student:
    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.grades = []

    def add_grade(self, grade):
        if isinstance(grade, Grade):
            self.grades.append(grade)
        else:
            return None

    def grades_list(self):
        return self.grades


class Grade:
    minimum_passing = 65

    def __init__(self, score):
        self.score = score

    def is_passing(self):
        return self.score >= Grade.minimum_passing

roger = Student("Roger van der Weyden", 10)
grade1 = Grade(44)
grade2 = Grade(100)

roger.add_grade(grade1)
roger.add_grade(grade2)

print(roger.grades_list())  # prints the list of Grade objects

for g in roger.grades_list():
    print(f"Score: {g.score}, Passing: {g.is_passing()}")