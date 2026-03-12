from collections import UserList
data = [4, 6, 8, 9, 5, 7, 3, 1, 0]

# Custom Class that inherits from UserList Class
class ListSorter(UserList):

  # overwrite a method from the list class  
  def append(self, item):
    self.data.append(item)
    self.data.sort()

sorted_list = ListSorter(data)
sorted_list.append(30)
print(sorted_list)