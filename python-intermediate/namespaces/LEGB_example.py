"""
In Python, the unofficial rule 
(often referred to in literature but does not exist in the official documentation) is known as the LEGB rule.
LEGB stands for Local, Enclosing, Global, and Built-in. 
These four letters represent the order of namespaces Python will check to see if a name exists
"""

# Global Variable
'''
How to change the value of a globla variable from within a nested function
'''
color = 'green'

def change_color(new_color):
  # Allow access to global variable inside an "Enclose Scope" Namespace
  global color

  def disp_color():
    print('The original color was: ' + color)
  # to_update scope is local to change_color() function  
  to_update = new_color
  print(locals())

  # call inner function
  disp_color()
  # update global var
  color = to_update
  print('The new color is: ' + color)
change_color('blue')
print(f"The global variable is now {color}")