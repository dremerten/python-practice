from functools import reduce

fruits = {"Grape": (4, 6, 2), 
          "Lemon": (7, 3, 1), 
          "Orange": (5, 8, 1), 
          "Apple": (2, 8, 10), 
          "Watermelon": (0, 9, 6)}

# 1 Original version using reduce + map
total_fruits_1 = reduce(lambda x, y: x + y, map(lambda q: fruits[q][0] + fruits[q][1] + fruits[q][2], fruits))
print("Original reduce+map:", total_fruits_1)

# 2 Generator comprehension version with reduce
total_fruits_2 = reduce(lambda x, y: x + y, (sum(fruits[q]) for q in fruits))
print("Generator comprehension + reduce:", total_fruits_2)

# 3 Pythonic version using just sum()
total_fruits_3 = sum(sum(fruits[q]) for q in fruits)
print("Pythonic sum():", total_fruits_3)

