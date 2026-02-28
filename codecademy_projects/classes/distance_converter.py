class DistanceConverter:
    kms_in_a_mile = 1.609

    def how_many_kms(self, miles):
        return miles * self.kms_in_a_mile


converter = DistanceConverter()
while True:
    user_input = input("Enter number of miles you wish to convert to kilometers (non-negative number): ")
    try:
        miles = float(user_input)
        if miles < 0:
            print("Please enter a non-negative number.")
        else:
            break  # valid input, exit loop
    except ValueError:
        print("Invalid input. Please enter a number.")

kms = converter.how_many_kms(miles)
print(f"There are {kms:.2f} kilometers in {miles} miles.")