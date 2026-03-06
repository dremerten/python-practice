class InventoryError(Exception):
  def __init__(self, supply):
    self.supply = supply

  def __str__(self):
    return f"Sorry we are sold out.Currently {self.supply} in stock. Please try again next week."

inventory = {
  'Piano': 3,
  'Lute': 1,
  'Sitar': 2
}

def submit_order(instrument, quantity):
  supply = inventory[instrument]
  if quantity > supply or quantity == 0:
    raise InventoryError(supply)
  else:
    inventory[instrument] -= quantity
    print('Successfully placed order! Remaining supply: ' + str(inventory[instrument]))

instrument = 'Piano'
quantity = 2
submit_order(instrument, quantity)

instrument = 'Piano'
quantity = 1
submit_order(instrument, quantity)