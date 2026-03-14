import logging

# Welcome message
print("Welcome to Food in a Jiffy!")

# Configure logging
logging.basicConfig(
    filename="cashier.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Menu options
food_options = {
    "H": {"name": "Hamburger", "price": 2.49},
    "C": {"name": "Cheeseburger", "price": 4.99},
    "F": {"name": "Fries", "price": 2.50},
    "D": {"name": "Drink", "price": 1.99},
    "E": {"name": "End Order", "price": 0.00}
}

# Function to display the menu
def menu():
    print("\n--- Menu ---")
    for key, item in food_options.items():
        print(f"[{key}] {item['name']}: ${item['price']:.2f}")

# Start of ordering
cost = 0
order_list = []  # To keep track of items ordered
menu()

choice = input("\nSelect a letter corresponding to the menu choice to order: ").upper()

while choice != "E":
    if choice not in food_options:
        logger.error("Invalid choice '%s', please select again.", choice)
        print("Invalid choice. Please try again.")
    else:
        food = food_options[choice]
        try:
            num = int(input(f"\nHow many of the {food['name']} would the customer like to order? "))
            if num <= 0:
                print("Quantity must be at least 1. Using 1 by default.")
                num = 1
        except ValueError:
            print("\nInvalid number entered. Using quantity of 1.")
            num = 1

        food_price = round(food['price'] * num, 2)
        cost += food_price
        order_list.append((food['name'], num, food_price))
        print(f"\n{food['name']} x{num} - ${food_price:.2f}")
        logger.info("Added %d x %s for $%.2f", num, food['name'], food_price)

    menu()
    choice = input("\nSelect a letter corresponding to the menu choice to order: ").upper()

# Checkout
print("\n--- Order Summary ---")
for item_name, qty, price in order_list:
    print(f"{item_name} x{qty} - ${price:.2f}")

print(f"\nThe total for the order is ${cost:.2f}")

# Payment handling
while True:
    try:
        money = float(input("\nEnter the amount paid by the customer: "))
        if money < cost:
            print("There is not enough money. Please re-enter the amount paid.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a number.")

change = round(money - cost, 2)
print(f"The customer's change is ${change:.2f}")

# Log completed order
logger.info("Order completed. Total: $%.2f, Paid: $%.2f, Change: $%.2f", cost, money, change)
logger.info("Items: %s", ", ".join([f"{qty}x {name}" for name, qty, price in order_list]))
