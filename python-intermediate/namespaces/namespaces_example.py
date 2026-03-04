"""
Now that we have examined the built-in and
global
Preview: Docs Loading link description
namespaces, let’s dive into the deepest level of namespaces - the local namespace. To do so, let’s start by examining this program:

global_variable = 'global'

def add(num1, num2):
  nested_value = 'Inside Function'   
  print(num1 + num2)

add(5, 10) 

Copy to Clipboard

Here, we have defined two values: a global_variable and a add() function. In Python, whenever the interpreter executes a function, it will generate a local namespace for that specific function. This namespace only exists inside of the function and remains in existence until the function terminates.

Similar to how we can see the global namespace using a built-in function called
globals()
Preview: Docs Loading link description
, Python provides a function called
locals()
Preview: Docs Loading link description
to see any generated local namespace. Let’s refactor our program just slightly and see what exists inside of a local namespace:

global_variable = 'global'

def add(num1, num2):
  nested_value = 'Inside Function'   
  print(num1 + num2)
  print(locals())

add(5, 10) 

Copy to Clipboard

Would output:

15
{'num1': 5, 'num2': 10, 'nested_value': 'Inside Function'}

Copy to Clipboard

Notice the following:

    We called locals() inside the add() function to get the local namespace generated when the function is executed. If we called locals() outside of a function in our program, it behaves the same as globals().

    The value printed
    from
    Preview: Docs Loading link description
    calling locals() represents the namespace that only exists inside of the function. Notice even the function parameters num1 and num2 exist alongside the variable name nested_value. The namespace does not include global_variable since it exists outside of the function (in the global namespace).

Let’s now practice examining the local namespace!
Instructions

    Checkpoint 1 Passed

    1.

    Note: Since we will be printing a lot of namespaces, the current editor has markers for where to write each checkpoint.

    First, let’s look at the differences between the global and local namespaces for a file with one variable defined. In the code editor, write two print statements that:
        print locals()
        print globals()

    Examine the output of both. Notice any similarities?

Checkpoint 2 Passed

2.

Now that we have seen what a local namespace looks like without any other code, let’s add some functions so we can check out local namespaces inside of a function.

Create a function called divide() that has two parameters num1 and num2.

The function should create a variable called result that is the result of dividing num1 by num2. The function should then also print locals().
Checkpoint 3 Passed

3.

Let’s add some more names! Create a function called multiply() that has two parameters num1 and num2.

The function should create a variable called product that is the result of multiplying num1 by num2. This function should also print locals().
Checkpoint 4 Passed

4.

To see our local namespace inside divide(), we need to execute it. Call divide() with the values of 3 & 4. Examine the local namespace it generates.
Checkpoint 5 Passed

5.

To see our local namespace inside multiply(), we need to execute it. Call multiply() with the values of 4 & 50. Examine the local namespace it generates. Notice any similarities?
Checkpoint 6 Passed

6.

Let’s examine how the local namespace called outside of functions has changed. Print locals() once more. Notice any changes?
"""


global_variable = 'global'

print(' -- Local and global Namespaces with empty script -- \n')
print(locals())
print(globals())

def divide(num1, num2):
  result = num1 / num2
  print(locals())

def multiply(num1, num2):
  product = num1 * num2
  print(locals())

print(' \n -- Local Namespace for divide -- \n')
divide(3, 4)

print(' \n -- Local Namespace for multiply -- \n')
multiply(4, 50)

print(' \n -- Local Namespace final -- \n')
print(locals())