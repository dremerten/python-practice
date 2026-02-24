def contains(big_string, little_string):
  return little_string in big_string

# Check if two strings contain the same characters
def common_letters(string_one, string_two):
  common = []
  for letter in string_one:
    if letter in string_two and not letter in common:
      common.append(letter)
  return common

  result = common_letter("New York", "San Francisco")
  print(result)