"""
Both var1 and var3 are associated with the global namespace before they are declared so they can be accessed within the global scope.
var2 uses the nonlocal keyword
and is in the local namespace, and is accessible within the local scope of function1
"""

# Outer function
def function1():
  global var1
  var1 = 1
  var2 = 2
  # Inner function
  def function2():
    nonlocal var2
    global var3
    var2 += 1
    var3 = 3
    print(f"The is the global Namespace: \n {globals()}\n")
    print(f"This is the local Namespace:\n {locals()}")
  
  # Call inner function
  function2()

# Call outer function
function1()