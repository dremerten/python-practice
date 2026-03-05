grade_list = [3.5, 3.7, 2.6, 95, 87]

"""
Split it into three parts:

lambda x: x * 25 if x <= 4 else x
       │        │
       │        └─ what gets returned
       └─ input variable

Read it as:

function(x) → return x * 25 if x <= 4 else x
"""
grades_100scale = map(lambda x: x * 25 if x <= 4 else x, grade_list)
updated_grade_list = list(grades_100scale) 
print(updated_grade_list)