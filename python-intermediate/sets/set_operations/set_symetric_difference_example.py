"""
The symmetric difference operator finds elements that are unique
to one set but not the other. In other words, it returns a set
of items that are in either set A or set B, but not in both.

Formula:
    A ^ B  or  A.symmetric_difference(B)
    Equivalent to: (A - B) | (B - A)

Example:
    A = {1, 2, 3}
    B = {3, 4}
    A ^ B  => {1, 2, 4}

We can also update the original set using this operation by using the .symmetric_difference_update() method to update the original set
with the result instead of returning a new set or frozenset object. 
"""

user_song_history = {'Retro Words': ['pop', 'warm', 'happy', 'electronic', 'synth'],
                     'Stomping Cue': ['country', 'fiddle', 'party'],
                     'Back To Art': ['pop', 'sad', 'emotional', 'relationship'],
                     'Double Lights': ['electronic', 'chill', 'relaxing', 'piano', 'synth']}

friend_song_history = {'Lowkey Space': ['electronic', 'dance', 'synth', 'upbeat'],
                     'Blinding Era': ['rap', 'intense', 'moving', 'fast'],
                     'Wait For Limit': ['rap', 'upbeat', 'romance', 'relationship'],
                     'Double Lights': ['electronic', 'chill', 'relaxing', 'piano', 'synth']}


user_tags = set()
for song_name, tags in user_song_history.items():
  for tag in tags:
    user_tags.add(tag)
#print(type(user_tags))

friend_tags = set()
for song_name, tags in friend_song_history.items():
  for tag in tags:
    friend_tags.add(tag)
#print(friend_tags)

unique_tags = user_tags ^ friend_tags
print(unique_tags)