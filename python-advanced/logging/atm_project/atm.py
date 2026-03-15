import logging
import random
import sys
import time

# -------------------
# Logger Setup
# -------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Stream (stdout) handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))

# File handler
file_handler = logging.FileHandler('atm.log')
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))

# Add handlers
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# -------------------
# BankAccount Class
# -------------------
class BankAccount:
    def __init__(self):
        self.balance = 100000000
        logger.info("Hello! Welcome to the ATM Depot!")

    def authenticate(self):
        attempts = 0

        while True:
            pin_input = input("Enter account pin: ")

            # Validate length and digits first
            if len(pin_input) != 4 or not pin_input.isdigit():
                logger.error("PIN must be exactly 4 digits.")
                continue

            pin = int(pin_input)  # Convert after validation
            if pin != 7894:
                attempts += 1
                logger.error(f"Invalid PIN. Attempt {attempts}/3.")

                if attempts >= 3:
                    logger.warning("Too many wrong attempts. Account locked for 30 seconds.")

                    # Terminal countdown
                    for remaining in range(10, 0, -1):
                        print(f"Please wait: {remaining:2d} seconds", end='\r', flush=True)
                        time.sleep(1)
                    print(" " * 30, end='\r')  

                    attempts = 0 
                continue

            logger.info("Authentication successful.")
            attempts = 0  # Reset attempts on success
            return

    def _log_transaction(self, status: str):
        """Helper to log transaction info."""
        logger.info("Transaction Info:")
        logger.info(f"Status: {status}")
        logger.info(f"Transaction #{random.randint(10000, 1000000)}")

    def deposit(self):
        try:
            amount = float(input("Enter amount to be deposited: "))
            if amount < 0:
                logger.warning("You entered a negative number to deposit.")
            self.balance += amount
            logger.info(f"Amount Deposited: ${amount}")
            self._log_transaction("Successful")
        except ValueError:
            logger.error("You entered a non-number value to deposit.")
            self._log_transaction("Failed")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to be withdrawn: "))
            if amount > self.balance:
                logger.error("Insufficient balance to complete withdrawal.")
                self._log_transaction("Failed")
            else:
                self.balance -= amount
                logger.info(f"You withdrew: ${amount}")
                self._log_transaction("Successful")
        except ValueError:
            logger.error("You entered a non-number value to withdraw.")
            self._log_transaction("Failed")

    def display(self):
        logger.info(f"Available Balance: ${self.balance:.2f}")

    def menu(self):
        """Show the ATM menu and handle choices"""
        while True:
            print("\n--- ATM Menu ---")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. View Balance")
            print("4. All Done (Exit)")
            
            choice = input("Select an option (1-4): ").strip()

            if choice == "1":
                self.deposit()
            elif choice == "2":
                self.display()
                self.withdraw()
            elif choice == "3":
                self.display()
            elif choice == "4":
                logger.info("Thank you for using the ATM. Goodbye!")
                break
            else:
                logger.warning("Invalid option selected. Please choose 1-4.")

# -------------------
# Main Program
# -------------------
if __name__ == "__main__":
    acct = BankAccount()
    acct.authenticate()
    acct.menu()