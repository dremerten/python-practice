"""
When working with set or frozenset container, 
one of the most common operations we can perform is a merge.
To do this, we can return the union of two sets using the .union() method or | operator. 
Doing so will return a new set or frozenset containing all elements from both sets without duplicates.
"""

# Given a set and frozenset of song tags for two python related hits
prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}

py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'})

# Get the union using the .union() method
combined_tags = prepare_to_py.union(py_and_dry)
print(combined_tags)

"""

Using |:

# Get the union using the | operator
frozen_combined_tags = py_and_dry | prepare_to_py
print(frozen_combined_tags)

Would output:

frozenset({'electric guitar', 'rock and roll', 'rock', 'synth', 'heavy metal', 'classic'})

Note that the return value in both methods takes the form of the left operand.
In the first example since prepare_to_py() called the union() function, so the result was a regular set.
In the second example, since py_and_dry was the left operand, the end result was a frozenset.
"""

song_data = {'Retro Words': ['pop', 'warm', 'happy', 'electronic'],
             'Wait For Limit': ['rap', 'upbeat', 'romance'],
             'Stomping Cue': ['country', 'fiddle', 'party'],
             'Lowkey Space': ['electronic', 'dance', 'synth']}

user_tag_data = {'Lowkey Space': ['party', 'synth', 'fast', 'upbeat'],
                 'Retro Words': ['happy', 'electronic', 'fun', 'exciting'],
                 'Wait For Limit': ['romance', 'chill', 'rap', 'rhythmic'], 
                 'Stomping Cue': ['country', 'swing', 'party', 'instrumental']}


new_song_data = {}
for key, val in song_data.items():
  song_tag_set = set(val)
  user_tag_set = set(user_tag_data[key])
  new_song_data[key] = song_tag_set | user_tag_set
print(new_song_data)