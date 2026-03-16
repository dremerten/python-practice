from functools import reduce

fruits = {"Grape": (4, 6, 2), 
          "Lemon": (7, 3, 1), 
          "Orange": (5, 8, 1), 
          "Apple": (2, 8, 10), 
          "Watermelon": (0, 9, 6)}

# 1 Original version using reduce + map
total_fruits_1 = reduce(lambda x, y: x + y, map(lambda key: fruits[key][0] + fruits[key][1] + fruits[key][2], fruits))
print("Original reduce+map:", total_fruits_1)

# 2 Generator comprehension version with reduce
total_fruits_2 = reduce(lambda x, y: x + y, (sum(fruits[key]) for key in fruits))
print("Generator comprehension + reduce:", total_fruits_2)

# 3 Pythonic version using just sum()
total_fruits_3 = sum(sum(fruits[key]) for key in fruits)
print("Pythonic sum():", total_fruits_3)

