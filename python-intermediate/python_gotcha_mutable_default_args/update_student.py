def update_order(new_item, current_order=[]):
  current_order.append(new_item)
  return current_order

# First order, burger
order1 = update_order({'item': 'burger', 'cost': '3.50'})
# Second order, just a soda
order2 = update_order({'item': 'soda', 'cost': '1.50'})
#print(order2)

"""
Why This Happens

Mutable default arguments (like lists, dicts, sets) persist between function calls.
Default parameter values are evaluated from left to right when the function definition is executed. 
This means that the expression is evaluated once, when the function is defined, 
and that the same “pre-computed” value is used for each call.

#### The Correct Pattern
def update_order(new_item, current_order=None):
    if current_order is None:
        current_order = []
    current_order.append(new_item)
    return current_order

Now each call gets a fresh list unless one is explicitly passed.

"Default mutable arguments are evaluated once at definition time, 
so state leaks across calls. Use None as the default and initialize inside the function.
"""

"""
def createStudent(name, age, grades=[]):
    return {
        'name': name,
        'age': age,
        'grades': grades
    }

chrisley = createStudent('Chrisley', 15)
dallas = createStudent('Dallas', 16)

def addGrade(student, grade):
    student['grades'].append(grade)
    print(student['grades'])

addGrade(chrisley, 90)
addGrade(dallas, 100)

# notice how they have THE SAME ID number
print(id(chrisley['grades']))
print(id(dallas['grades']))
"""

##########################################################################################

def createStudent(name, age, grades=None):
  if grades is None:
    grades = []
  return {
    'name': name,
    'age': age,
    'grades': grades
  }

def addGrade(student, grade):
    student['grades'].append(grade)
    print(student['grades'])


chrisley = createStudent('Chrisley', 15)
dallas = createStudent('Dallas', 16)
addGrade(chrisley, 90)
addGrade(dallas, 100)

# notice how they have DIFFERENT ID numbers
print(id(chrisley['grades']))
print(id(dallas['grades']))