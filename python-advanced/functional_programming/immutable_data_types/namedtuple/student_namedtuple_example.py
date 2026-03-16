from collections import namedtuple

# Create a class called student
student = namedtuple("student", ["name", "grade", "course_number"]) 

# Create the records for the students
peter = student("Peter", 'B', 101)
amanda = student("Amanda", 'C', 101)
sarah = student("Sarah", 'A', 102)
lisa = student("Lisa", 'D', 101)
alex = student("Alex", 'A', 102)
maria = student("Maria", 'B', 101)
andrew = student("Andrew", 'C', 102)

# Create the math class
math_class = (peter, amanda, sarah, lisa, alex, maria, andrew)

def math_201(math_class):
    for s in math_class:
        if s.grade <= 'B':
            yield student(s.name, 'X', 201)

result = tuple(math_201(math_class))
print(result)
