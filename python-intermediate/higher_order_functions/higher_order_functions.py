"""
Here, total_bill() is classified as a higher-order function because it takes in an argument that is a function (add_tax() 
Right off the bat, this setup may not be very useful compared to simply calling add_tax(100) directly, 
but what if we wanted to add a tip instead of tax? 
Let’s see how we can reuse our higher-order function to add a 20% gratuity instead of a 6% sales tax:
We can see that we can reuse total_bill() for both of these functions!
But this still isn’t any more useful than calling the function add_tax() or add_tip() directly on a value. 
The true power comes when we want to keep a consistent manipulation no matter what function is passed in.
"""

# Higher order function -> takes an argument that is a function
def total_bill(func, value):
  total = func(value)
  return total

def add_tax(total):
  tax = total * 0.09
  new_total = total + tax
  return new_total

def add_tip(total):
  tip = total * .2
  new_total = total + tip
  return new_total

print(f"Total Bill with 20% tax for tip: ${total_bill(add_tip, 100):.2f} dollars")
print(f"Total Bill with 9% sales tax added: ${total_bill(add_tax, 100):.2f} dollars")