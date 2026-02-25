def reversed_list(lst1, lst2):
  for index in range(len(lst1)):
    if lst1[index] != lst2[len(lst2) - 1 - index]:
        return False
  breakpoint()
  return True

lst1 = [1, 2, 3]
lst2 = [3, 2, 1] 

print(reversed_list(lst1, lst2))


# Get the last index in a string
last_char = favorite_fruit[len(favorite_fruit)-1]