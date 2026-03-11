"""
deque in Python (TLDR)

deque = double-ended queue

It’s a list-like data structure from collections that lets you add and remove items from both ends efficiently.

from collections import deque

d = deque([1, 2, 3])
Why use deque instead of a list?
Operation	list	deque
append right	fast	fast
pop right	fast	fast
append left	slow	fast
pop left	slow	fast

Reason: Python lists must shift memory when inserting/removing at the front.

deque is optimized for O(1) operations on both ends.

#############################################################################
O(1) (Big-O Notation) — TLDR

O(1) means constant time.

The operation takes the same amount of time no matter how big the data gets.

Input size:   10 items   → time ≈ same
Input size: 1000 items   → time ≈ same
Input size: 1M items     → time ≈ same
Simple Example

Accessing an item in a Python list by index:

nums = [10, 20, 30, 40, 50]

print(nums[2])

Python jumps directly to index 2, so it does not need to scan the list.

Runtime = O(1).
#################################################################################



Core Methods
from collections import deque

d = deque([1, 2, 3])

d.append(4)        # add to right
d.appendleft(0)    # add to left

d.pop()            # remove right
d.popleft()        # remove left

Result:

deque([1, 2, 3])
append(4)     -> deque([1,2,3,4])
appendleft(0) -> deque([0,1,2,3,4])


DevOps / systems note (relevant to how you code Python tools):

If you're writing log processors, job schedulers, or streaming pipelines, deque is ideal for rolling buffers or sliding windows because maxlen automatically discards old entries.

Example for log tail buffer:

last_logs = deque(maxlen=100)

"""