import asyncio
from tqdm import tqdm


async def factorial(name, number):
    """
This program calculates factorials using async (concurrent) tasks.

What is a factorial?
A factorial means multiplying a number by all the numbers below it down to 1.
Example:
    4! = 4 × 3 × 2 × 1 = 24
    5! = 5 × 4 × 3 × 2 × 1 = 120

What does the code do?
- It creates multiple tasks (35 total)
- Each task calculates the factorial of a different number
- All tasks run at the same time using asyncio (they take turns instead of blocking)

Why use async?
- The `await asyncio.sleep(1)` simulates work
- While one task is "waiting", others can run
- This makes the program feel faster and more efficient

What is the progress bar doing?
- It updates each time a task finishes
- It shows how many of the 35 factorial calculations are complete

Big picture:
- Many factorial calculations are running concurrently
- Results are collected as each task finishes
"""
    f = 1
    for i in range(2, number + 1):
        print(f"🔹 Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"✅ Task {name}: factorial({number}) = {f}")
    return name, f


async def main():
    tasks = [
        asyncio.create_task(
            factorial(chr(65 + i), i + 2) if i < 26 else factorial(f"A{i-25}", i + 2)
        )
        for i in range(12)
    ]

    results = []

    with tqdm(total=len(tasks), desc="Completed Tasks", unit="task") as pbar:
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            results.append(result)
            pbar.update(1)

    print("\n📦 Final Results:")
    for name, value in results:
        print(f"{name}: {value}")


asyncio.run(main())