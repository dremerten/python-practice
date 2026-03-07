# try:
#     print('1 + 2 = 3')
#     print('2 + 3 = 5')
#     print(3 + 4 + ' = 7')
#     print('4 + 5 = 9')
# except TypeError:
#     print("A TypeError occurred!")

'''
assert <condition>, 'Message if condition is not met'
'''

# EXAMPLE - bug is expected
def times_ten(number):
    return number * 100

result = times_ten(20)
assert result == 200, 'Expected times_ten(20) to return 200, instead got ' + str(result)

