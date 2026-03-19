"""
ASYNCHRONOUS PROGRAMMING WITH ASYNCIO

The asyncio module uses async/await syntax to build and execute asynchronous 
code. These two keywords allow you to manage tasks concurrently within 
your programs.

1. The 'async' keyword: 
   Declares a function as a coroutine. Coroutines are functions that may 
   return normally with a value or suspend themselves internally. This 
   allows tasks to be paused and resumed, mimicking multitasking—a concept 
   very similar to threading.

2. The 'await' keyword: 
   Suspends execution of the current task until the awaited object is 
   completed. For example, 'await task2' inside 'task1' tells Python: 
   "Pause task1 here until task2 is finished."

Example Implementation:
"""

import time
import asyncio

async def greeting_with_sleep_async(string):
  s = time.perf_counter()
  print(string)
  await asyncio.sleep(2)
  print("says hello!")
  elapsed = time.perf_counter() - s
  print("Asyncio Elapsed Time: " + str(elapsed) + " seconds")

asyncio.run(greeting_with_sleep_async("Foobar"))
