# Nested example
"""
The with statement is being called once but invoking two context managers.
Each context manager is separated by a comma and has its own target variable.
Our teacher.txt file is being opened in write mode because it will be written 
into and our student.txt is opened in read mode because we are attempting to copy the text into the teacher’s file
The resulting teacher.txt file will now include everything that was in the student.txt file.
"""

from contextlib import contextmanager
 
@contextmanager
def poem_files(file, mode):
  print('Opening File')
  open_poem_file = open(file, mode)
  try:
    yield open_poem_file
  finally:
    print('Closing File')
    open_poem_file.close()


@contextmanager
def card_files(file, mode):
  print('Opening File')
  open_card_file = open(file, mode)
  try:
    yield open_card_file
  finally:
    print('Closing File')
    open_card_file.close()

# Nested Context Managers
with poem_files('poem.txt', 'r') as poem:
  with card_files('card.txt', 'w') as card:
    print(poem, card)
    card.write(poem.read())
