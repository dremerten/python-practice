from collections import UserString

# Create a class which inherits from the UserString class
class IntenseString(UserString):

    # A new method to capitalize and add exclamation points to our string
    def exclaim(self):
        self.data = self.data.upper() + '!!!'
        return self.data


    # Overwrite the count method to only count a certain letter
    def count(self, sub=None, start=0, end=0):
        num = 0
        for let in self.data:
            if let == 'P':
                num+=1
        return num


intense_string = IntenseString("python rules por que no, para puerto rico")

print(intense_string.exclaim())
print(intense_string.count())