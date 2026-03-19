"""
Python3 script illustrating:

1. Sequential Programming
2. Concurrency
3. Parallelism
4. Asynchronous Programming

This version adds:
- simple terminal animations
- emoji progress bars
- visually clear section headers
"""

import time
import threading
import multiprocessing
import asyncio
import itertools
import sys


BAR_LENGTH = 20


def print_header(title: str, emoji: str) -> None:
    print("\n" + "=" * 60)
    print(f"{emoji}  {title}")
    print("=" * 60)


def progress_bar(current: int, total: int, prefix: str = "", done_emoji: str = "🟩", todo_emoji: str = "⬜") -> str:
    filled = int(BAR_LENGTH * current / total)
    empty = BAR_LENGTH - filled
    percent = int((current / total) * 100)
    bar = done_emoji * filled + todo_emoji * empty
    return f"{prefix} [{bar}] {percent:>3}%"


def animate_task(task_name: str, steps: int = 10, delay: float = 0.2, done_emoji: str = "🟩") -> None:
    for step in range(1, steps + 1):
        sys.stdout.write("\r" + progress_bar(step, steps, prefix=f"{task_name}", done_emoji=done_emoji))
        sys.stdout.flush()
        time.sleep(delay)
    print(f" ✅")


async def animate_task_async(task_name: str, steps: int = 10, delay: float = 0.2, done_emoji: str = "🟩") -> None:
    for step in range(1, steps + 1):
        sys.stdout.write("\r" + progress_bar(step, steps, prefix=f"{task_name}", done_emoji=done_emoji))
        sys.stdout.flush()
        await asyncio.sleep(delay)
    print(f" ✅")


def take_order(customer_name: str, delay: float = 0.15) -> None:
    print(f"🧍 {customer_name} steps up to the register...")
    animate_task(f"📝 Taking order for {customer_name}", steps=12, delay=delay, done_emoji="🟨")
    print(f"🥪 {customer_name}'s order is complete.\n")


async def prepare_food_async(customer_name: str, delay: float = 0.15) -> None:
    print(f"🎟️  {customer_name} places an order and gets a ticket.")
    await animate_task_async(f"🍔 Preparing food for {customer_name}", steps=12, delay=delay, done_emoji="🟦")
    print(f"📣 Ticket called for {customer_name}! Food is ready.\n")


def cpu_heavy_task(name: str, steps: int = 18, delay: float = 0.08) -> None:
    print(f"⚙️  {name} starts CPU-heavy work...")
    for step in range(1, steps + 1):
        _ = sum(i * i for i in range(5000))
        sys.stdout.write("\r" + progress_bar(step, steps, prefix=f"🔥 {name}", done_emoji="🟥"))
        sys.stdout.flush()
        time.sleep(delay)
    print(" ✅")
    print(f"🏁 {name} finished heavy computation.\n")


def sequential_programming() -> None:
    """
    Sequential Programming Analogy:
    Imagine a deli with one line and one register.

    Each customer must wait for the person in front of them to fully
    finish ordering before the next customer can begin.

    In Python, this means the program runs one step at a time,
    top to bottom, with each task blocking the next one.

    One customer orders, then the next, then the next.
    Nothing overlaps.
    """
    print_header("Sequential Programming", "🧾")
    take_order("Alice")
    take_order("Bob")
    take_order("Charlie")


def concurrency_with_threading() -> None:
    """
    Concurrency Analogy:
    Imagine a deli with multiple lines but only one cashier.

    The cashier switches between whoever is ready at the front of a line.
    If one customer pauses or is not ready, the cashier can move to another.

    In Python, threading can help with this kind of overlapping progress,
    especially for I/O-bound tasks like waiting on files, APIs, or network calls.

    The tasks make progress around the same time, but this does not
    necessarily mean true simultaneous CPU execution.
    """
    print_header("Concurrency with threading", "🔀")

    def worker(customer_name: str) -> None:
        spinner = itertools.cycle(["⏳", "🔄", "💫", "✨"])
        print(f"{next(spinner)} {customer_name} enters one of the lines...")
        animate_task(f"🧵 Thread serving {customer_name}", steps=12, delay=0.12, done_emoji="🟪")
        print(f"🍽️  {customer_name} has been served.\n")

    threads = [
        threading.Thread(target=worker, args=("Alice",)),
        threading.Thread(target=worker, args=("Bob",)),
        threading.Thread(target=worker, args=("Charlie",)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def parallelism_with_multiprocessing() -> None:
    """
    Parallelism Analogy:
    Imagine a deli with multiple lines and multiple registers.

    Now several cashiers can help customers at the exact same time.
    This reduces waiting because the work is divided across registers.

    In Python, multiprocessing works like this by using separate processes.
    Each process has its own memory space and can run on different CPU cores.

    This is best for CPU-bound work, where true parallel execution matters.
    """
    print_header("Parallelism with multiprocessing", "⚡")

    processes = [
        multiprocessing.Process(target=cpu_heavy_task, args=("Worker 1",)),
        multiprocessing.Process(target=cpu_heavy_task, args=("Worker 2",)),
        multiprocessing.Process(target=cpu_heavy_task, args=("Worker 3",)),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


async def asynchronous_programming() -> None:
    """
    Asynchronous Programming Analogy:
    Imagine a deli where customers place an order, receive a ticket,
    and then step aside instead of waiting in a line.

    When the food is ready, their ticket number is called.
    The tickets are not necessarily called in the order they were given.
    They are called whenever the food is ready.

    In Python, asyncio works like this.
    A task can start, pause while waiting, and allow other tasks to run.
    This is efficient for I/O-bound operations where waiting would otherwise
    block the whole program.
    """
    print_header("Asynchronous Programming with asyncio", "🎟️")

    await asyncio.gather(
        prepare_food_async("Alice", 0.12),
        prepare_food_async("Bob", 0.08),
        prepare_food_async("Charlie", 0.10),
    )


def show_summary(duration: float, label: str, emoji: str) -> None:
    print(f"{emoji} {label} took: {duration:.2f} seconds")


def main() -> None:
    total_start = time.time()

    start = time.time()
    sequential_programming()
    show_summary(time.time() - start, "Sequential", "🧾")

    start = time.time()
    concurrency_with_threading()
    show_summary(time.time() - start, "Threading", "🧵")

    start = time.time()
    parallelism_with_multiprocessing()
    show_summary(time.time() - start, "Multiprocessing", "⚙️")

    start = time.time()
    asyncio.run(asynchronous_programming())
    show_summary(time.time() - start, "Asyncio", "🎟️")

    print("\n" + "🌟" * 20)
    print(f"🏁 Full demo finished in {time.time() - total_start:.2f} seconds")
    print("🌟" * 20)


if __name__ == "__main__":
    main()