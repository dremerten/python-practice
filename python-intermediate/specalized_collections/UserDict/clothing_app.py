from collections import UserDict, UserList
import pprint
data = {'order_4829': {'type': 't-shirt', 'size': 'large', 'price': 9.99, 'order_status': 'processing'},
        'order_6184': {'type': 'pants', 'size': 'medium', 'price': 14.99, 'order_status': 'complete'},
        'order_2905': {'type': 'shoes', 'size': 12, 'price': 22.50, 'order_status': 'complete'},
        'order_7378': {'type': 'jacket', 'size': 'large', 'price': 24.99, 'order_status': 'processing'}}

class OrderProcessingDict(UserDict):
  
  def clean_orders(self):
    to_delete = []
    for key, val in self.data.items():
      if val["order_status"] == "complete":
        to_delete.append(key)
    for item in to_delete:
        pprint.pprint(f"Deleting Item: ====>  {self.data[item]}", indent=4)
        del self.data[item]


process_dict = OrderProcessingDict(data)
process_dict.clean_orders()
pprint.pprint(f"Cleaned and Process Orders: ========> {process_dict}", indent=4)