def number_generator():
  i = 0
  while True:
    yield i
    i += 1
    
def even_number_generator(numbers):
  for n in numbers:
    if n % 2 == 0:
      yield n

even_numbers = even_number_generator(number_generator())

for e in even_numbers:
  print(e)
  if e == 40000:
    break
