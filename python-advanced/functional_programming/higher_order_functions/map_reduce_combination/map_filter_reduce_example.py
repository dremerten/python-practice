from functools import reduce
from operator import mul

# Data
costs = {"shirt": (4, 13), "shoes": (2, 80), "pants": (3, 100),
         "socks": (5, 5), "ties": (3, 14), "watch": (1, 145)}
nums = (24, 6, 7, 16, 8, 2, 3, 11, 21, 20, 22, 23, 19, 12, 1, 4, 17, 9, 25, 15)

# ====== Old style (map + filter + reduce) ======
# total = reduce(lambda x,y: x+y, filter(lambda r: r>150, map(lambda q: costs[q][0]*costs[q][1], costs)))
# product = reduce(lambda x,y: x*y, map(lambda z: z+5, filter(lambda q: q<10, nums)))

# ====== Pythonic style ======
total = sum(q*c for q, c in costs.values() if q*c > 150)      # sum of expensive items
product = reduce(mul, (n+5 for n in nums if n < 10))           # product of (numbers <10)+5

print(f"Total: {total:.2f}")
print(f"Product: {product}")