from collections import namedtuple

# create a class called student
student = namedtuple("student", ["name", "age", "grade"]) 

# Create tuples for the three students
scott = student("Scott", 28, 'A')
nicole = student("Nicole", 26, 'B')
john = student("John", 29, 'D')

# Access Scott’s information for example
print(scott.name) # Output: Scott
print(scott.age) # Output: 28
print(scott.grade) # Output: ‘A’

# create a tuple of student objects
students = (scott, nicole, john)

# Access the first student (Scott)
print(students[0].name)   # Output: Scott
print(students[0].age)    # Output: 28
print(students[0].grade)  # Output: A

# Access the second student (Nicole)
print(students[1].name)   # Output: Nicole
print(students[1].age)    # Output: 26
print(students[1].grade)  # Output: B