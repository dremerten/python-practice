"""
Add Ten

Let’s loop through the keys again, but this time let’s modify the values within the dictionary. Our function should add 10 to every value in the dictionary and return the modified dictionary. Here is what we need to do:

    Define the function to accept one parameter for our dictionary
    Loop through every key in the dictionary
    Retrieve the value using the key and add 10 to it. Make sure to re-save the new value to the original key.
    After the loop, return the modified dictionary
"""

def add_ten(my_dictionary):
    for key in my_dictionary.keys():
        my_dictionary[key] = my_dictionary[key] + 10 # my_dictionary[key] += 10
    return my_dictionary

print(add_ten({1:5, 2:2, 3:3}))