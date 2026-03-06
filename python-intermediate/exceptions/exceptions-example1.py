"""
Python will first attempt to execute code inside the try clause code block.
If no exception is encountered in the code, the except clause is skipped and the program continues normally.
If an exception does occur inside of the try code block, 
Python will immediately stop executing the code and begin executing the code inside the except code block (sometimes called a handler).
"""


customer_rewards = {
  'Zoltan': 82570,
  'Guadalupe': 29850,
  'Mario': 17849
}

def display_rewards_account(customer):
  try:
    rewards_number = customer_rewards[customer]
  except KeyError as e:
    print(f"The Customer {e} was not found in rewards program!")
  else:
    print('Rewards account number is: ' + str(rewards_number))


customer = 'Joker'
display_rewards_account(customer)