# class FishInventory:
#   def __init__(self, fishList):
#       self.available_fish = fishList

# fish_inventory_cls = FishInventory(["Bubbles", "Finley", "Moby"])

# for fish in fish_inventory_cls:
#   print(fish)

'''
running this code will error with:

Traceback (most recent call last):
  File "/home/andre/DevOps-Practice/python-practice/python-intermediate/custom_iterators/custom_class_iterators.py", line 7, in <module>
    for fish in fish_inventory_cls:
                ^^^^^^^^^^^^^^^^^^
TypeError: 'FishInventory' object is not iterable

By default, custom classes are not iterable. We can’t just go around plugging our custom classes into for
loops
Preview: Docs Loading link description
and expecting any results! This presents a problem if the class we are working
with
Preview: Docs Loading link description
needs the ability to iterate.

When we create a FishInventory class object, 
we want to iterate over all the fish available within self.available_fish. 
If we attempt to directly iterate over our custom FishInventory class object, 
we will receive an error because we have not yet implemented the iterator protocol 
for this custom class. To make the FishInventory class iterable, 
we can simply define __iter__() and __next__() methods.

'''

# # custom iterator on class
# fish_inventory_cls = FishInventory(["Bubbles", "Finley", "Moby"])


# class FishInventory:
#   def __init__(self, fishList):
#       self.available_fish = fishList

#   def __iter__(self):
#     self.index = 0
#     return self

#   def __next__(self):
#     if self.index < len(self.available_fish):
#       fish_status = self.available_fish[self.index] + " is available!"
#       self.index += 1
#       return fish_status
#     else:
#       raise StopIteration


class CustomerCounter:
  def __iter__(self):
    self.count = 0
    return self

  def __next__(self):
    self.count += 1
    if self.count > 100:
      raise StopIteration
    return self.count

    
customer_counter = CustomerCounter()

for customer in customer_counter:
  print(customer)