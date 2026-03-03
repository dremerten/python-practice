"""
 Largest Value

For the last challenge, we are going to create a function that is able to find the maximum value in the dictionary and return the associated key. This is a twist on the max algorithm since it is using a dictionary rather than a list. These are the steps:

    Define the function to accept one parameter for our dictionary
    Initialize the starting key to a very low number
    Initialize the starting value to a very low number
    Iterate through the dictionary’s key/value pairs.
    Inside the loop, if the current value is larger than the current largest value, replace the largest key and largest value with the current ones you are looking at
    Once you are done iterating through all key/value pairs, return the key which has the largest value
"""

def max_key(my_dictionary):
    largest_key = float("-inf")
    largest_value = float("-inf")
    for key, value in my_dictionary.items():
        if value > largest_value:
            largest_key = key
            largest_value = value
    return largest_key

print(max_key({1:100, 2:1, 3:4, 4:10}))
# should print 1
print(max_key({"a":100, "b":10, "c":1000}))