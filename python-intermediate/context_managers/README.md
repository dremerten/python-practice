# Python Context Managers — Complete Guide

Context managers allow Python programs to **safely manage resources** such as files, database connections, locks, or timers. They ensure that resources are **opened, used, and properly cleaned up automatically**.

This prevents bugs such as **forgotten file closes, leaked connections, or unhandled exceptions**.

Context managers are typically used with the `with` statement.

---

# Basic Syntax

```python
with resource as variable:
    # code that uses the resource
```

When the `with` block starts, the resource is **opened or initialized**.  
When the block finishes (even if an error occurs), the resource is **automatically cleaned up**.

---

# What Context Managers Handle Automatically

All context managers follow the same lifecycle:

1. **Open the resource**
2. **Enter the runtime context**
3. **Execute user operations**
4. **Handle possible exceptions**
5. **Close the resource**

This pattern prevents resource leaks and simplifies code.

---

# Built-in Context Manager Example (File Handling)

The most common context manager in Python is `open()`.

```python
with open("albatros.txt", "r") as poem:
    for _ in range(4):
        print(poem.readline())
```

Example Output:

```
Souvent, pour s'amuser, les hommes d'équipage
Prennent des albatros, vastes oiseaux des mers,
Qui suivent, indolents compagnons de voyage,
Le navire glissant sur les gouffres amers.
```

What happens internally:

1. `open()` opens the file  
2. `with` enters the runtime context  
3. Your code reads the file  
4. The file automatically closes when the block exits

Equivalent manual code (not recommended):

```python
poem = open("albatros.txt", "r")

for _ in range(4):
    print(poem.readline())

poem.close()
```

If an exception occurs before `close()`, the file may stay open — which is why context managers are safer.

---

# Creating Custom Context Managers

You can create your own context managers using two approaches:

1. **Class-Based Context Managers**
2. **Decorator-Based Context Managers**

---

# Class-Based Context Manager

A class context manager implements three special methods:

| Method | Purpose |
|------|------|
| `__init__()` | Setup resources |
| `__enter__()` | Start the context |
| `__exit__()` | Cleanup resources |

Example: Automatically generating employee bonus letters.

```python
class BonusLetter:

    def __init__(self, first, employee_id, salary, pct):
        self.first = first
        self.id = employee_id
        self.salary = salary
        self.pct = pct

        self.letter = open(f"{self.id}_bonus_notice.txt", "w")
        self.thanks_message = open("thanks_message.txt", "r")
        self.conclusion = open("conclusion.txt", "r")

    def __enter__(self):

        self.letter.write(f"Dear {self.first}!\n\n")
        self.letter.write(self.thanks_message.read())

        bonus_amount = round(self.salary * (self.pct / 100))

        self.letter.write(
            f"\nYou will receive a yearly bonus of ${bonus_amount}.\n"
        )

        return self.letter

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.letter.write(self.conclusion.read())

        self.thanks_message.close()
        self.conclusion.close()
        self.letter.close()

        return True
```

Using the context manager:

```python
with BonusLetter("John", 3789, 100000, 5) as letter:
    print("Letter generated!")
```

Example generated letter:

```
Dear John!

We value all our employees and are committed to their growth and well-being.

You will receive a yearly bonus of $5000.

Again, allow us to thank you for your efforts.

Sincerely,
HR Department
```

Important behavior:

If `__exit__()` returns `True`, Python **suppresses exceptions** and continues execution.

---

# Decorator-Based Context Manager

Python provides a simpler way to build context managers using the `contextlib` module.

Instead of writing a class, you create a **generator function** that uses `yield`.

Import:

```python
from contextlib import contextmanager
```

Structure:

```
setup
try:
    yield resource
except:
    handle error
finally:
    cleanup
```

---

# Decorator-Based Example

Example: Creating interview proposal letters.

```python
from contextlib import contextmanager

@contextmanager
def interview_proposal(title_name, position, date, time):

    proposal_letter = open(f"{title_name}_interview_proposal.txt", "w")

    try:
        proposal_letter.write(
            f"Dear {title_name},\n\n"
            f"Thank you for applying for the {position} role. "
            f"We would like to schedule an interview with you."
        )

        yield proposal_letter

    except Exception:
        print("Exception handled!")

    finally:
        proposal_letter.write(
            f"\n\nWould you be available on {date} at {time}?"
            f"\n\nWe look forward to hearing from you."
            f"\nThe HR Department"
        )

        proposal_letter.close()
```

Using the context manager:

```python
with interview_proposal(
    "Mr. Smith",
    "Software Developer",
    "Monday June 10",
    "2 PM"
) as letter:

    letter.write(
        " We were especially impressed by your leadership "
        "experience on wealth management software."
    )
```

Example generated output:

```
Dear Mr. Smith,

Thank you for applying for the Software Developer role. We would like to schedule an interview with you. We were especially impressed by your leadership experience on wealth management software.

Would you be available on Monday June 10 at 2 PM?

We look forward to hearing from you.
The HR Department
```

---

# Context Manager Comparison

| Approach | Best Use Case |
|------|------|
| Built-in (`with open`) | File handling |
| Class-based | Complex resource management |
| Decorator-based | Simple custom context logic |

---

# Mental Model (Easy Way to Remember)

Think of a context manager like **automatic setup and cleanup**.

```
enter → run code → exit
```

Example analogy:

```
open file
do work
close file
```

Context manager version:

```
with open(file) as f:
    do work
```

Python guarantees the cleanup step runs **even if an error occurs**.

---

# TL;DR

Context managers:

- Manage resources safely
- Automatically clean up
- Use the `with` statement
- Prevent resource leaks
- Simplify error handling

Three main ways to use them:

```
with open(file)
class MyContext: __enter__ / __exit__
@contextmanager decorator
```

