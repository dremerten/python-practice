list1 = list(range(100))
list2 = list(range(10, 1001, 10))  # 10 → 1000 stepping by 10


result = list(map(lambda x, y: x + y, list1, list2))
print(result[-10:])  # show first 10 results
print(len(result))
