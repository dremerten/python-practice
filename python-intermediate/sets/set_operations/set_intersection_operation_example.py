"""
Let’s say that we have two or more sets, and we want to find which items both sets have in common. 
The set container has a method called .intersection()
which returns a new set or frozenset consisting of those elements. 
An intersection can also be performed on multiple sets using the & operator.
Similar to the other operations, the type of the first operand 
(a set or frozenset on the left side of the operator or method) determines if a set or frozenset is returned when finding the intersection.
"""
# Given a set and frozenset of song tags for two python related hits
prepare_to_py = {'rock', 'heavy metal', 'electric guitar', 'synth'}

py_and_dry = frozenset({'classic', 'rock', 'electric guitar', 'rock and roll'})

# Find the intersection between them while providing the `frozenset` first.
frozen_intersected_tags = py_and_dry.intersection(prepare_to_py)
print(frozen_intersected_tags)

# Find the intersection using the operator `&` and providing the normal set first
intersected_tags = prepare_to_py & py_and_dry
print(intersected_tags)

"""
In addition to a regular intersection, the set container can also use a method called .intersection_update(). 
Instead of returning a new set, the original set is updated to contain the result of the intersection.
"""

"""
Now, let’s find the recommended songs based on the common tags we found in the previous step.
Find all other songs in song_data which have these tags. Store the songs which have any matching tags into a dictionary called recommended_songs.
 Make sure that you do not add any songs which the user has listened to recently!
"""

song_data = {'Retro Words': ['pop', 'warm', 'happy', 'electronic', 'synth'],
             'Wait For Limit': ['rap', 'upbeat', 'romance'],
             'Stomping Cue': ['country', 'fiddle', 'party'],
             'Lowkey Space': ['electronic', 'dance', 'synth', 'upbeat'],
             'Back To Art': ['pop', 'sad', 'emotional', 'relationship'],
             'Blinding Era': ['rap', 'intense', 'moving', 'fast'],
             'Down To Green Hills': ['country', 'relaxing', 'vocal', 'emotional'],
             'Double Lights': ['electronic', 'chill', 'relaxing', 'piano', 'synth']}

user_recent_songs = {'Retro Words': ['pop', 'warm', 'happy', 'electronic', 'synth'],
                     'Lowkey Space': ['electronic', 'dance', 'synth', 'upbeat']}


# Intersection of 2 sets
tags_int = set(user_recent_songs["Retro Words"]) & set(user_recent_songs["Lowkey Space"])
print(tags_int)

recommended_songs = {}
for song_name, tags in song_data.items():
  for tag in tags:
    if tag in tags_int:
      if song_name not in user_recent_songs:
        recommended_songs[song_name] = tags
print(recommended_songs)

"""
<loop through each song in song_data>  
  <loop through each tag in the current song's tags>  
    <if the tag is in tags_int (user's interests)>  
      <if the song_name is not in user_recent_songs>  
        <add the song and its tags to recommended_songs>
"""
        
