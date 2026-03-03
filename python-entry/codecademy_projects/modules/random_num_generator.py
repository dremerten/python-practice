import random
import time
import sys

def random_number_generator(min_value: int, max_value: int):
    random_list = [random.randint(min_value, max_value) 
                   for _ in range(max_value - min_value + 1)]
    random_number = random.choice(random_list)
    return random_number

def loading_animation():
    print("\nGenerating random number", end="")
    for _ in range(5):
        time.sleep(0.3)
        print(".", end="")
        sys.stdout.flush()
    print("\n")

# Get user input
while True:
    try:
        print("You will prompted to enter a minimum and maximum number range to which a random number will be selected from.")
        min_value = int(input("Enter a minimum non-negative number: "))
        max_value = int(input("Enter a maximum non-negative number: "))

        if min_value < 0 or max_value < 0:
            print("Numbers must be non-negative. Try again.\n")
        elif min_value > max_value:
            print("Minimum cannot be greater than maximum. Try again.\n")
        else:
            break
    except ValueError:
        print("Please enter valid integers only.\n")

loading_animation()

result = random_number_generator(min_value, max_value)

print(f"Your random number between {min_value} and {max_value} is: {result}")