"""
The code defines a small employee system using OOP features: abstract classes, inheritance, properties, and operator overloading.
What each part does (very short)

AbstractEmployee
An abstract base class.
Automatically assigns a unique ID to each employee.
Forces subclasses to implement say_id().

User
Stores a username.
Uses a property getter/setter to control access to _username.

Meeting
Keeps a list of attendees.
+ operator (__add__) adds an employee to the meeting.
len(meeting) returns number of attendees.

Employee
Inherits from AbstractEmployee and User.
Gets an auto ID and a username.
Implements say_id() and adds say_username().
"""

from abc import ABC, abstractmethod

class AbstractEmployee(ABC):
  new_id = 1
  def __init__(self):
    self.id = AbstractEmployee.new_id
    AbstractEmployee.new_id += 1

  @abstractmethod
  def say_id(self):
    pass

class User:
  def __init__(self):
    self._username = None

  @property
  def username(self):
    return self._username

  @username.setter
  def username(self, new_name):
    self._username = new_name

class Meeting:
  def __init__(self):
    self.attendees = []
  
  def __add__(self, employee):
    print("{} added.".format(employee.username))
    self.attendees.append(employee.username)

  def __len__(self):
    return len(self.attendees)

class Employee(AbstractEmployee, User):
    def __init__(self, username):
      super().__init__()
      User.__init__(self)
      self.username = username

    def say_id(self):
      print("My id is {}".format(self.id))
 
    def say_username(self):
      print("My username is {}".format(self.username))