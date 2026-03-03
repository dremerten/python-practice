import time

countdown = 10
print("Starting Countdown to take off!")
while countdown > -1:
  time.sleep(1)
  print(f"Countdown... {countdown}")
  countdown -= 1
  if countdown == 0:
    time.sleep(2)
    print("Ready.....Blast Off!")
    break
