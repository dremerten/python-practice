from datetime import time as time_module

class Menu:
  def __init__(self, name, items, start_time, end_time):
    self.name = name
    self.items = items
    self.start_time = start_time
    self.end_time = end_time

  def __repr__(self):
    return f"The {self.name} is available from {self.start_time} to {self.end_time}"

  def calculate_bill(self, purchased_items):
    total_price = 0
    for item in purchased_items:
      if item in self.items:
        total_price += self.items[item]
      else:
        print(f"{item} is not on the {self.name}.")
    return f"${total_price:.2f}"

class Franchise:
  def __init__(self, address, menus):
    self.address = address
    self.menus = menus

  def __repr__(self):
    return f"The address is {self.address}"

  def available_menus(self, time):
    available_menus = []
    current_time = time_module(time)
    for menu in self.menus:
      if menu.start_time <= current_time and current_time <= menu.end_time:
        available_menus.append(menu.name)
    return ", ".join(available_menus)

class Business:
  def __init__(self, name, franchises):
    self.name = name
    self.franchises = franchises


brunch = Menu("Brunch Menu", {
        'pancakes': 7.50, 
        'waffles': 9.00, 
        'burger': 11.00, 
        'home fries': 4.50, 
        'coffee': 1.50, 
        'espresso': 3.00, 
        'tea': 1.00, 
        'mimosa': 10.50, 
        'orange juice': 3.50
}, 
start_time=time_module(11, 0), end_time=time_module(16, 0))

early_bird = Menu("Early Bird Menu", {
        'salumeria plate': 8.00, 
        'salad and breadsticks (serves 2, no refills)': 14.00, 
        'pizza with quattro formaggi': 9.00, 
        'duck ragu': 17.50, 
        'mushroom ravioli (vegan)': 13.50, 
        'coffee': 1.50, 
        'espresso': 3.00
}, 
start_time=time_module(15, 0), end_time=time_module(18, 0))

dinner = Menu("Dinner Menu", {
        'crostini with eggplant caponata': 13.00,
        'caesar salad': 16.00, 
        'pizza with quattro formaggi': 11.00, 
        'duck ragu': 19.50, 
        'mushroom ravioli (vegan)': 13.50, 
        'coffee': 2.00, 
        'espresso': 3.00,
}, 
start_time=time_module(17, 0), end_time=time_module(23, 0))

kids = Menu("Kids Menu", {
        'chicken nuggets': 6.50, 
        'fusilli with wild mushrooms': 12.00, 
        'apple juice': 3.00
}, 
start_time=time_module(11, 0), end_time=time_module(21, 0))

arepas_menu = Menu("Take a' Arepa", {
      'arepa pabellon': 7.00, 
      'pernil arepa': 8.50, 
      'guayanes arepa': 8.00, 
      'jamon arepa': 7.50
}, start_time=time_module(10, 0), end_time=time_module(16, 0))

flagship_store = Franchise("1232 West End Road", [brunch, early_bird, dinner, kids])
print(flagship_store.available_menus(15))
new_installment = Franchise("12 East Mulberry Street", [brunch, early_bird, dinner, kids])
bis1 = Business("Basta Fazoolin' with my Heart", [flagship_store, new_installment])
arepas_place = Franchise("189 Fitzgerald Avenue", [arepas_menu])
bis2 = Business("Take a' Arepa!", [arepas_place])