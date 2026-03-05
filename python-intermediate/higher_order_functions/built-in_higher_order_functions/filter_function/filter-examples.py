"""
Similar to map(), the filter() function takes a function and an iterable as arguments. 
Just as the name suggests, the goal of the filter() function is to “filter” values out of an iterable.

The filter() function accomplishes this goal by applying a passed filtering function to each element in the passed iterable.
The filtering function should be a function that returns a boolean value: True or False. 
The returned filter object will hold only those elements of the passed iterable for which the filtering function returned True. 
"""
names = ["margarita", "Linda", "Masako", "Maki", "Angela"]
 
M_names = filter(lambda name: name[0] == "M" or name[0] == "m", names)  
print(list(M_names))