"""
Count First Letter

This function accepts a dictionary where the keys are last names and the values are lists of first names 
of people who have that last name. We need to calculate the number of people who have the same first letter in their last name. 

Here are the steps we need:

    Define the function to accept one parameter for our dictionary
    Create a new empty dictionary called letters
    Loop through every key in our names dictionary
    Inside the loop, get the first letter of the last name we are looking at. 
    If the first letter is not in our letter dictionary, 
    add it as a key and set the value to the number of people that have that last name. 
    Otherwise, if the first letter is already in our letter dictionary, increment the value stored with that key by the number of people that have that last name
    After the loop, return the letters dictionary
"""

def count_first_letter(names):
  letters = {}
  for key in names:
    if key[0] not in letters:
        letters.setdefault(key[0], 0)
    letters[key[0]] += len(names[key])
  return letters

print(count_first_letter({"Stark": ["Ned", "Robb", "Sansa"], "Snow" : ["Jon"], "Sannister": ["Jaime", "Cersei", "Tywin"]}))