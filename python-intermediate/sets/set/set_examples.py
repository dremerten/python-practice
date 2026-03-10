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

# There are two different ways to add elements to a set
# 1. The.add() method - Adds a single element to a set if it is not already present.

# Create a set to hold the song tags
song_tags = {'country', 'folk', 'acoustic'}

# Add a new tag to the set and try to add a duplicate.
song_tags.add('guitar')
song_tags.add('country')

print(song_tags)
'''
{'country', 'acoustic', 'guitar', 'folk'}
'''

# 2. The .update() method can add multiple elements.

# Create a set to hold the song tags
song_tags = {'country', 'folk', 'acoustic'}

# Add more tags using a hashable object (such as a list of elements)
other_tags = ['live', 'blues', 'acoustic']
song_tags.update(other_tags)

print(song_tags)
'''
{'acoustic', 'folk', 'country', 'live', 'blues'}
'''

"""
Neither of these methods will add a duplicate item to a set.
A frozenset can not have any items added to it and so neither of these methods will work.
Notice that when the elements are printed, they are not printed in the same order in which they entered the set. 
This is because set and frozenset containers are unordered.
"""

song_data = {'Retro Words': ['pop', 'warm', 'happy', 'electric']}

user_tag_1 = 'warm'
user_tag_2 = 'exciting'
user_tag_3 = 'electric'

tag_set = set(song_data["Retro Words"])

tag_set.update([user_tag_1, user_tag_2, user_tag_3])
song_data["Retro Words"] = tag_set
print(song_data)

"""
There are two methods for removing specific elements
from a set:

The .remove() method searches for an element within the set and removes it if it exists, otherwise, a KeyError is thrown.
"""
# Given a list of song tags
song_tags = {'guitar', 'acoustic', 'folk', 'country', 'live', 'blues'}

# Remove an existing element
song_tags.remove('folk')
print(song_tags)

# Try removing a non-existent element
#song_tags.remove('fiddle')


{'blues', 'acoustic', 'country', 'guitar', 'live'}

"""
Followed by:

Traceback (most recent call last):
File "some_file_name.py", line 9, in <module>
  song_tags.remove('fiddle')
KeyError: 'fiddle'
"""

"""
The .discard() method works the same way but does not throw an exception if an element is not present.
NOTE: Note that items cannot be removed from a frozenset so neither of these methods would work.
"""

#### Removing from a Set ####


song_data_users = {'Retro Words': ['pop', 'onion', 'warm', 'helloworld', 'happy', 'spam', 'electric']}

# Write your code below!
tag_set = set(song_data_users["Retro Words"])
tag_set.discard("onion")
tag_set.discard("helloworld")
tag_set.discard("spam")

song_data_users["Retro Words"] = tag_set
print(song_data_users)


#### Finding elements in a Set ####
"""
In Python, set and frozenset items cannot be accessed by a specific index
This is due to the fact that both containers are unordered and have no indices. 
However, like most other Python containers, we can use the in keyword to test if an element is in a set or frozenset.
"""

# Given a set of song tags
song_tags = {'guitar', 'acoustic', 'folk', 'country', 'live', 'blues'}

# Print the result of testing whether 'country' is in the set of tags or not
print('country' in song_tags)

allowed_tags = ['pop', 'hip-hop', 'rap', 'dance', 'electronic', 'latin', 'indie', 'alternative rock', 'classical', 'k-pop', 'country', 'rock', 'metal', 'jazz', 'exciting', 'sad', 'happy', 'upbeat', 'party', 'synth', 'rhythmic', 'emotional', 'relationship', 'warm', 'guitar', 'fiddle', 'romance', 'chill', 'swing']

song_data_users = {'Retro Words': ['pop', 'explosion', 'hammer', 'bomb', 'warm', 'due', 'writer', 'happy', 'horrible', 'electric', 'mushroom', 'shed']}

# Create a set from song_data_users 'Retro Words' Values
tag_set = set(song_data_users["Retro Words"])

# capture all the bad tags from tag_set
bad_tags = [tag for tag in tag_set if tag not in allowed_tags]
print(bad_tags)

# remove inncorect tags from tag set
for tag in bad_tags:
  if tag not in allowed_tags:
    tag_set.discard(tag)

song_data_users["Retro Words"] = tag_set
print(song_data_users)

