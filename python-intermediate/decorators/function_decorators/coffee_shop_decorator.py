"""
decorator function is used to 'decorate' or enhance a base function

# example WITHOUT a decorator
# Violates the 'single responsiblity priciple'
# 1. Brews tea
# 2. Timing process
# Functions should focus on 1 distinct task
"""
import time
import random

def timer_dec(base_fn):
    def enhanced_fn(*args, **kwargs):
        start_time = time.time()
        result = base_fn(*args, **kwargs)
        end_time = time.time()
        print(f"Execution Time: {end_time - start_time:.2f} seconds to brew!\n")
        return result
    return enhanced_fn


@timer_dec
def brew_tea(name: str, tea_type: str, steep_time: int | None = None): #  | None means = > This value can be this type or None
    try:
        if steep_time is None:
            steep_time = random.randint(1, 6)

        if not isinstance(steep_time, int):
            raise TypeError(f"{steep_time} must be an integer")

        if not isinstance(name, str) or not isinstance(tea_type, str):
            raise TypeError("Name and tea_type must be strings")

        print(f"Brewing {tea_type} tea for {steep_time} seconds...")
        time.sleep(steep_time)
        print(f"Order Up for {name}! Your {tea_type} Tea is ready!")

    except TypeError as e:
        print(f"Error: {e}")


@timer_dec
def matcha_latte(name: str, sweetness_level: str, creamer_type: str):
    try:
        if not all(isinstance(x, str) for x in (name, sweetness_level, creamer_type)):
            raise TypeError("All arguments must be strings")

        print("Making your Matcha Latte....")
        time.sleep(2)
        print(f"Order Up for {name}! Matcha is ready with sweetness level {sweetness_level} and {creamer_type} creamer!")

    except TypeError as e:
        print(f"Error: {e}")


# calls
brew_tea(
    name="Ripley",
    tea_type="green"
)

matcha_latte(
    name="Zenia",
    sweetness_level="medium",
    creamer_type="oat milk"
)



