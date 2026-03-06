class Dog:
  sound = "Woof"

  def __init__(self, name, age, breed, energy_level='high', favorite_food='chicken', favorite_game='fetch'):
    self.name = name
    self.age = age
    self.breed = breed
    self.energy_level = energy_level
    self.favorite_food = favorite_food
    self.favorite_game = favorite_game

  def bark(self):
    print(Dog.sound)


ripley = Dog("ripley", 3, "boarder collie")
print(locals())
