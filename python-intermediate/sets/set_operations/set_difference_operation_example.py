"""
Similar to how we can find elements in common between sets, we can also find unique elements in one set. 
To do so, the set or frozenset use the .difference() method or the - operator. 
This returns a set or frozenset, which contains only the elements from the first set which are not found in the second set. 
Similar to the other operations, the type of the first operand (a set or frozenset on the left side of the operator or method) 
determines if a set or frozenset is returned when finding the difference.

Alternatively, we can use the - operator

This operation also supports an updating version of the method. 
You can use .difference_update() to update the original set with 
the result instead of returning a new set or frozenset object.
"""

# Given a set and frozenset of song tags for two python related hits
prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}

py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'})

# Find the elements which are only in prepare_to_py
only_in_prepare_to_py = prepare_to_py.difference(py_and_dry)
print(only_in_prepare_to_py)

song_data = {'Retro Words': ['pop', 'warm', 'happy', 'electronic', 'synth'],
             'Wait For Limit': ['rap', 'upbeat', 'romance', 'relationship'],
             'Stomping Cue': ['country', 'fiddle', 'party'],
             'Lowkey Space': ['electronic', 'dance', 'synth', 'upbeat'],
             'Back To Art': ['pop', 'sad', 'emotional', 'relationship'],
             'Blinding Era': ['rap', 'intense', 'moving', 'fast'],
             'Down To Green Hills': ['country', 'relaxing', 'vocal', 'emotional'],
             'Double Lights': ['electronic', 'chill', 'relaxing', 'piano', 'synth']}

user_liked_song = {'Back To Art': ['pop', 'sad', 'emotional', 'relationship']}
user_disliked_song = {'Retro Words': ['pop', 'warm', 'happy', 'electronic', 'synth']}

# Write your code below!
tag_diff = set(user_liked_song["Back To Art"]) - set(user_disliked_song["Retro Words"])
print(tag_diff)


recommended_songs = {}
for song_name, tags in song_data.items():
  for tag in tags:
    if tag in tag_diff:
      if song_name not in user_liked_song:
        recommended_songs[song_name] = tags
print(recommended_songs)

"""
<loop through each song in song_data>  
  <loop through each tag in the current song's tags>  
    <if the tag is in tags_int (user's interests)>  
      <if the song_name is not in user_recent_songs>  
        <add the song and its tags to recommended_songs>
"""
