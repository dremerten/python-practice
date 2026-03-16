from collections import namedtuple
from functools import reduce

# Prices are in USD
menu_item = namedtuple("menu_item", ["name", "dish_type", "price"])

jsp = menu_item("Jumbo Shrimp Platter", "Appetizer", 29.95)
lc = menu_item("Lobster Cake", "Appetizer", 30.95)
scb = menu_item("Sizzling Canadian Bacon", "Appetizer", 9.95)
ccc = menu_item("Codecademy Crab Cake", "Appetizer", 32.95)
cs = menu_item("Caeser Salad", "Salad", 14.95)
mgs = menu_item("Mixed Green Salad", "Salad", 10.95)
cp = menu_item("Codecademy Potatoes", "Side", 34.95)
mp = menu_item("Mashed Potatoes", "Side", 14.95)
a = menu_item("Asparagus", "Side", 15.95)
rs = menu_item("Ribeye Steak", "Entree", 75.95)
phs = menu_item("Porter House Steak", "Entree", 131.95)
grs = menu_item("Grilled Salmon", "Entree", 36.95)

menu = (jsp, lc, scb, ccc, cs, mgs, cp, mp, a, rs, phs, grs)
entree = 0
least_expensive = 0


entrees = [item for item in menu if item.dish_type == "Entree"]
entree = max(entrees, key=lambda x: x.price)

sides_and_salads = [item for item in menu if item.dish_type in ("Side", "Salad")]
least_expensive = min(sides_and_salads, key=lambda x: x.price)

print(entree)
print(sides_and_salads)
print(least_expensive)