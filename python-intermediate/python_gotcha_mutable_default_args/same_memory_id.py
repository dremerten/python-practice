import time
import sys

# ---------- ANSI COLORS ----------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def type_line(text="", delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ---------- FUNCTIONS ----------

def update_order(new_item, current_order=[]):
    current_order.append(new_item)
    return current_order


def update_order_fixed(new_item, current_order=None):
    if current_order is None:
        current_order = []
    current_order.append(new_item)
    return current_order


# ---------- EXECUTION ----------

order1 = update_order("burger")
order2 = update_order("soda")

order1_fixed = update_order_fixed("burger")
order2_fixed = update_order_fixed("soda")


# ---------- TERMINAL RENDER ----------

type_line("booting python-mutable-analyzer v3.0...\n")
time.sleep(0.4)

type_line("diff --git a/mutable_default.py b/mutable_default.py\n")


# ----- BROKEN -----
type_line(f"{RED}--- BROKEN IMPLEMENTATION{RESET}")

type_line(f"{YELLOW}- def update_order(new_item, current_order=[]):{RESET}")
type_line(f"{YELLOW}-     current_order.append(new_item){RESET}")
type_line(f"{YELLOW}-     return current_order{RESET}\n")

type_line(f"{RED}- output order1 -> {order1}{RESET}")
type_line(f"{RED}- output order2 -> {order2}{RESET}")
type_line(f"{RED}- id(order1) -> {id(order1)}{RESET}")
type_line(f"{RED}- id(order2) -> {id(order2)}{RESET}")
print(f"=" * 60)
print("")
type_line(f"{RED}- Result: SAME memory address (shared list)\n{RESET}")

time.sleep(0.2)


# ----- FIXED -----
type_line(f"{YELLOW}+++ FIXED IMPLEMENTATION +++{RESET}")

type_line(f"{GREEN}+ def update_order_fixed(new_item, current_order=None):{RESET}")
type_line(f"{GREEN}+     if current_order is None:{RESET}")
type_line(f"{GREEN}+         current_order = []{RESET}")
type_line(f"{GREEN}+     current_order.append(new_item){RESET}")
type_line(f"{GREEN}+     return current_order{RESET}\n")

type_line(f"+ output order1 -> {order1_fixed}{RESET}")
type_line(f"+ output order2 -> {order2_fixed}{RESET}")
type_line(f"+ id(order1) -> {id(order1_fixed)}{RESET}")
type_line(f"+ id(order2) -> {id(order2_fixed)}{RESET}")
print(f"=" * 60)
print("")
type_line(f"{GREEN}+ result: DIFFERENT memory addresses (separate lists)\n{RESET}")
type_line(f"{GREEN} Recommendation: use None for mutable default arguments.")
type_line(f"{GREEN} A workaround for mutable default arguments by using None paired with a conditional statement.\n")