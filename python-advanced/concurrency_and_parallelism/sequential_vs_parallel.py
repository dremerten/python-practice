import time
import threading
import asyncio
from multiprocessing import Process

# ------------------------------
# Color and emoji settings
# ------------------------------
COLORS = {
    "List1": "\033[94m",   # Blue
    "List2": "\033[92m",   # Green
    "List3": "\033[93m",   # Yellow
    "Thread": "\033[95m",  # Magenta
    "Process": "\033[91m", # Red
    "ENDC": "\033[0m"      # Reset
}

EMOJIS = {
    "List1": "🔵",
    "List2": "🟢",
    "List3": "🟡",
    "Thread": "🧵",
    "Process": "⚙️"
}

# Dictionary to store results
elapsed_times = {}

# ------------------------------
# Helper function to print colored progress
# ------------------------------
def print_progress(label, progress, total=1):
    bar_length = 20
    filled_length = int(bar_length * progress / total)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    color = COLORS.get(label.split('-')[0], COLORS["ENDC"])
    emoji = EMOJIS.get(label.split('-')[0], "")
    print(f"{color}[{emoji} {label}] |{bar}| {progress}/{total} step(s) completed{COLORS['ENDC']}", end="\r")
    if progress == total:
        print()  # Move to next line when done

# ------------------------------
# Average calculation functions
# ------------------------------
def cal_average(num, label="Task"):
    total = 0
    n = len(num)
    for i, t in enumerate(num, 1):
        total += t
        time.sleep(0.1)
        print_progress(label, i, n)
    avg = total / n
    return avg

async def cal_average_async(num, label="Task"):
    total = 0
    n = len(num)
    for i, t in enumerate(num, 1):
        total += t
        await asyncio.sleep(0.1)
        print_progress(label, i, n)
    avg = total / n
    return avg

# ------------------------------
# Execution functions
# ------------------------------
def main_sequential(list1, list2, list3):
    start = time.perf_counter()
    cal_average(list1, "List1")
    cal_average(list2, "List2")
    cal_average(list3, "List3")
    elapsed = time.perf_counter() - start
    elapsed_times['Sequential'] = elapsed
    return elapsed

async def main_async(list1, list2, list3):
    start = time.perf_counter()
    tasks = [
        cal_average_async(list1, "List1"),
        cal_average_async(list2, "List2"),
        cal_average_async(list3, "List3")
    ]
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    elapsed_times['Async'] = elapsed
    return elapsed

def main_threading(list1, list2, list3):
    start = time.perf_counter()
    lists = [list1, list2, list3]
    threads = []
    for i, lst in enumerate(lists, 1):
        thread = threading.Thread(target=cal_average, args=(lst, f"Thread-List{i}"))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    elapsed = time.perf_counter() - start
    elapsed_times['Threading'] = elapsed
    return elapsed

def main_multiprocessing(list1, list2, list3):
    start = time.perf_counter()
    lists = [list1, list2, list3]
    processes = [
        Process(target=cal_average, args=(lst, f"Process-List{i+1}"))
        for i, lst in enumerate(lists)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    elapsed = time.perf_counter() - start
    elapsed_times['Multiprocessing'] = elapsed
    return elapsed

# ------------------------------
# Function to display results matrix
# ------------------------------
def display_results_matrix():
    print("\n\033[1m--- Execution Time Results (seconds) ---\033[0m")
    print(f"{'Method':<20} | {'Elapsed Time':>12}")
    print("-"*36)
    for method, elapsed in elapsed_times.items():
        print(f"{method:<20} | {elapsed:>12.2f}")
    print("-"*36)

# ------------------------------
# Main Entry
# ------------------------------
if __name__ == '__main__':
    l1 = list(range(1, 100))
    l2 = list(range(1, 100))
    l3 = list(range(1, 100))

    print("\n--- Sequential Execution ---")
    main_sequential(l1, l2, l3)

    print("\n--- Asynchronous Execution ---")
    asyncio.run(main_async(l1, l2, l3))

    print("\n--- Threading Execution ---")
    main_threading(l1, l2, l3)

    print("\n--- Multiprocessing Execution ---")
    main_multiprocessing(l1, l2, l3)

    # Display final results matrix
    display_results_matrix()