"""
Python module, multiprocessing. This module is unique
from threading and asyncio in that allows the user to leverage multiple processors 
on a given machine simultaneously.
 This is because instead of threads or asynchronous tasks, multiprocessing is powered by subprocesses.
"""

import time
import multiprocessing

def greeting_with_sleep(string):
  print(string)
  time.sleep(2)
  print(string + " says hello!")

def main_multiprocessing():
  s = time.perf_counter()
  processes = []
  greetings = ['Codecademy', 'Chelsea', 'Hisham', 'Ashley']

  for i in range(len(greetings)):
    p = multiprocessing.Process(target=greeting_with_sleep, args=(greetings[i],))
    processes.append(p)
    p.start()

  for p in processes:
    p.join()
  
  elapsed = time.perf_counter() - s
  print("Processing Elapsed Time: " + str(elapsed) + " seconds")

main_multiprocessing()