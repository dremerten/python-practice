from collections import UserDict

class DisplayDict(UserDict):

    def display_info(self):
        print(f"Number of Keys: {len(self.keys())}")
        print(f"Keys: {list(self.keys())}")
        print(f"Number of Values: {len(self.values())}")
        print(f"Values: {list(self.values())}")

    def clear(self):
        print(f"Deleting all items from the dictionary!")
        super().clear()

disp_dict = DisplayDict({
    "user": "Mark",
    "device": "desktop",
    "num_visits": 37
})

disp_dict.display_info()

#disp_dict.clear()
