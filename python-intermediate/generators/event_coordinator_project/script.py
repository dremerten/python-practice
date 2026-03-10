def read_guestlist(file_name):
  
  with open(file_name) as f:
    entries = f.read().splitlines()
      

  while entries:
    line_data = entries.pop().split(',')
    name, age = line_data[0], int(line_data[1])
    guests[name] = age
    entry = yield name, age
    if entry is not None:
      entries.append(entry)

guests = {}

print('Guestlist:')
print('----------')
guestlist = read_guestlist('guest_list.txt')
for i in range(10):
  print(next(guestlist))

print(guestlist.send("Jane,35"))
for guest in guestlist:
  print(guest)

print()
print('Guests drinking age 21 and over list:')
print('------------------------')
age_21_over = (list(x for x in guests if guests[x] >= 21))
print(age_21_over)

print()

print("Fullseating list:")
print("-----------------")

def table1():
  table = 'Table number: ' + str(1)
  food = 'Chicken'
  for i in range(1,6):
    seat = i
    yield table, food, seat

def table2():
  table = 'Table number: ' + str(2)
  food = 'Steak'
  for i in range(1,6):
    seat = i
    yield table, food, seat

def table3():
  table = 'Table number: ' + str(3)
  food = 'Fish'
  for i in range(1,6):
    seat = i
    yield table, food, seat

def combinedtables():
  yield from table1()
  yield from table2()
  yield from table3()

fullseating = combinedtables()

def final(guests, fullseating):
  for i in guests:
    seating = next(fullseating)
    yield(i, seating)

fin = final(guests, fullseating)
for i in fin:
  print(i)



  

