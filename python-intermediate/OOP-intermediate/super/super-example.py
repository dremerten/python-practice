'''
Dog.speak()
   ↓
super().speak() → calls Animal.speak()
   ↓
print("Dog barks")

So the child extends the parent behavior instead of replacing it.
'''


class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        super().speak()
        print("Dog barks")

Dog().speak()