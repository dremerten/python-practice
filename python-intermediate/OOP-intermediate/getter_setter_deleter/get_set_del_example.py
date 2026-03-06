class Animal:
  def __init__(self, name):
    self._name = name
    self._age = None

  def get_age(self):
    return self._age

  def set_age(self, new_age):
    if isinstance(new_age, int):
      self._age = new_age
    else:
      raise TypeError

  def delete_age(self):
    del self._age
    print("_age Deleted")

a = Animal("Rufus")
print(a.get_age()) # None

a.set_age(10)
print(a.get_age()) # 10

#a.set_age("Ten") # Raises a TypeError

#a.delete_age() # "_age Deleted"
#print(a.get_age()) # Raises a AttributeError