class School:
  def __init__(self, name: str, level: str, numberOfStudents: int):
    self.name = name
    self.level = level
    self.numberOfStudents = numberOfStudents

  def getName(self):
    return self.name
  
  def getLevel(self):
    return self.level

  def getNumberOfStudents(self):
    return self.numberOfStudents

  def setNumberOfStudents(self, numberOfStudents):
    if isinstance(numberOfStudents, int):
      self.numberOfStudents = numberOfStudents
    else:
      raise TypeError

  def __repr__(self):
    return f"A {self.level} school named {self.name} with {self.numberOfStudents} students"

class PrimarySchool(School):
  def __init__(self, name, numberOfStudents, pickupPolicy):
    super().__init__(name, "primary", numberOfStudents)
    self.pickupPolicy = pickupPolicy

  def getPickupPolicy(self):
    return self.pickupPolicy
  
  def __repr__(self):
    schoolRepr = super().__repr__()
    return schoolRepr + f". The pickup policy is {self.pickupPolicy}"

class HighSchool(School):
  def __init__(self, name, numberOfStudents, sportsTeams):
    super().__init__(name, 'high', numberOfStudents)
    self.sportsTeams = sportsTeams

  def getSportsTeams(self):
    return self.sportsTeams

  def __repr__(self):
    prischoolRepr = super().__repr__()
    return prischoolRepr + f". Currently playing on the {self.sportsTeams} Teams this school year"

# Test out code
c = HighSchool("Codecademy High", 500, ["Tennis", "Basketball"])
print(c.getSportsTeams())
print(c)
b = PrimarySchool("Codecademy", 300, "Pickup Allowed")
print(b.getPickupPolicy())
print(b)
a = School("Codecademy", "high", 100)
print(a)
print(a.getName())
print(a.getLevel())
a.setNumberOfStudents(200)
print(a.getNumberOfStudents())