def sum_values(my_dictionary):
  sum = 0
  for value in my_dictionary.values():
    sum += value
  return sum


print(sum_values({"milk":5, "eggs":2, "flour": 3}))