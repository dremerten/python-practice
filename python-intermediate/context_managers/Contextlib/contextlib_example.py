from contextlib import contextmanager

"""
@contextmanager
def generator_function(<parameters>):
    <setup section - equivalent to __enter__ >
    try:
        yield <value>
    finally:
        <cleanup section - equivalent to __exit__ >
"""


# @contextmanager
# def poem_files(file, mode):
#   print("Opening File")
#   open_poem_file = open(file, mode)
#   try:
#     yield open_poem_file
#   finally:
#     print("Closing File")
#     open_poem_file.close()


# with poem_files('poem.txt', 'a') as opened_file:
#  print('Inside yield')
#  opened_file.write('Rose is beautiful, Just like you.')

from contextlib import contextmanager

@contextmanager
def open_file_contextlib(file, mode):
    open_file = open(file, mode)
    try:
        yield open_file
    # Exception Handling
    except Exception as exception:
        print('We hit an error: ' + str(exception))
    finally:
        open_file.close()

with open_file_contextlib('file.txt', 'w') as opened_file:
    opened_file.sign('We just made a context manager using contexlib')