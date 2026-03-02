"""
Frequency Count

This next function is similar, but instead of counting the length of each string in the list of strings, we will be counting the frequency of each string. This function will also accept a list of strings as input and return a new dictionary. Here is what we need to do:

    Define the function to accept one parameter for our list of strings
    Create a new empty dictionary
    Loop through every string in the list of strings
    Inside the loop, if the string is NOT already in our dictionary, store the string as a key with a value of 0 in our dictionary. 
    Otherwise, if the string is already in our dictionary, increment the value by 1.
    After the loop, return the new dictionary
"""


def frequency_dictionary(words):
    new_dict = {}
    for word in words:
        new_dict[word] = new_dict.get(word, 0) + 1
    return new_dict

print(frequency_dictionary(["apple", "apple", "cat", "cat"]))