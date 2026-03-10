"""
In Python, a set is a group of elements that are unordered and do not contain duplicates. 
Although it may seem that the usefulness of this data structure is limited, 
it can actually be very helpful for organizing items and performing set mathematics.

For example, we can imagine two different groups of items that have some similarities and differences. 
Using set mathematics, we can find the matching items, differences, combine the
sets

Preview: Docs Stores unordered collections of unique elements.
based on different parameters, and more! This is especially helpful when combing through very large datasets.

Alternatively, there is also an immutable version of a set called a frozenset. 
A frozenset behaves similarly to a normal set, but it does not include methods that modify the frozenset in any way. 
"""

# Creating a set with curly braces
music_genres = {'country', 'punk', 'rap', 'techno', 'pop', 'latin'}

# Creating a set from a list using set()
music_genres_2 = set(['country', 'punk', 'rap', 'techno', 'pop', 'latin'])

# Creating a set from a list that contains duplicates
music_genres_3 = set(['country', 'punk', 'rap', 'pop', 'pop', 'pop'])
print(music_genres_3)

# sets can contain different data types as long as they are unique values
music_different = {70, 'music times', 'categories', True , 'country', 45.7}

# Creating an empty set using the set() constructor
# Doing set = {} will define a dictionary rather than a set.  

empty_genres = set()

"""
Lastly, similar to list comprehensions we can create sets using a set comprehension 
and a data set (such as a list). Here is an example:
"""

items = ['country', 'punk', 'rap', 'techno', 'pop', 'latin']
music_genres = {category for category in items if category[0] == 'p'}
print(music_genres)

"""
Would output a set containing all elements from items starting with the letter 'p'
"""