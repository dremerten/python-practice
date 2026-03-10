# Generator functions
def summa():
    yield 'Summa Cum Laude'
def magna():
    yield 'Magna Cum Laude' 
def cum_laude():
    yield 'Cum Laude'

def graduation_countdown(days):
  while days >= 0:
    days_left = yield days
    if days_left != None:
      days = days_left
    else:
      days -= 1
      

days = 25
countdown_generator = (x for x in range(days, -1, -1))
gpas = [3.2, 4.0, 3.6, 2.9]

grad_days = graduation_countdown(days)
for day in grad_days:
  if day == 15:
    grad_days.send(10)
  elif day == 3:
    grad_days.close()
  print(f"Days Left: {day}")

def honors_generator(gpas):
  for gpa in gpas:
    if gpa > 3.9:
      yield from summa()
    elif gpa > 3.7:
      yield from magna()
    elif gpa > 3.5:
      yield from cum_laude()

honors = honors_generator(gpas)
for honor_label in honors:
  print(honor_label)