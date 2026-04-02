# Python Conditionals (`if`, `elif`, `else`) — Complete Guide

---

## 🧠 Core Idea

Conditionals control **which code runs**.

You are answering:

> “What should happen given this condition?”

---

## 🧩 Basic Syntax

```python
if condition:
    ...
elif another_condition:
    ...
else:
    ...
```

Execution order:
1. `if`
2. `elif` (only if previous conditions are False)
3. `else` (fallback)

---

## ✅ CASE 1: Single Condition (`if`)

Use when checking one condition.

```python
if cpu > 85:
    problems.append("cpu high")
```

✔ Runs only if True  
✔ No fallback required  

---

## 🔁 CASE 2: Multiple Independent Conditions (multiple `if`)

Use when **multiple conditions can be true**

```python
if cpu > 85:
    problems.append("cpu high")

if memory > 90:
    problems.append("memory high")

if disk > 90:
    problems.append("disk high")
```

✔ All conditions run independently  
✔ Multiple results allowed  

---

## 🔀 CASE 3: Mutually Exclusive (`if / elif`)

Use when **only one condition should run**

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
```

✔ Stops at first True  
✔ Only one branch executes  

---

## 🎯 CASE 4: Binary Decision (`if / else`)

Use when there are **exactly two outcomes**

```python
if problems:
    result["unhealthy_hosts"] += 1
else:
    result["healthy_hosts"] += 1
```

✔ Exactly one path runs  
✔ Prevents double-counting  

---

## 🔀 CASE 5: Multiple Exclusive (`if / elif / else`)

Use when:
- Multiple possibilities exist
- Only one should run
- You need a fallback

```python
if status == "error":
    handle_error()
elif status == "warning":
    handle_warning()
else:
    handle_ok()
```

✔ Exactly one branch runs  

---

## ⚠️ CASE 6: Nested Conditionals

Use when logic depends on another condition.

```python
if environment == "production":
    if problems:
        alert()
    else:
        deploy()
```

✔ Layered decisions  

---

## ⚠️ CASE 7: Guard Clauses (Early Return)

Use to exit early.

```python
if not isinstance(host, dict):
    return ["Invalid host: not a dictionary"]
```

✔ Reduces nesting  

---

## ⚠️ CASE 8: Condition + try/except

Use when values may be invalid.

```python
try:
    if disk >= 90:
        problems.append("disk high")
except TypeError:
    problems.append("disk invalid")
```

✔ Handles bad data safely  

---

## 🚨 COMMON MISTAKES

### ❌ Missing `else`

```python
if problems:
    unhealthy += 1

healthy += 1
```

🔴 Bug:
- healthy always increments
- double-counting

✔ Fix:

```python
if problems:
    unhealthy += 1
else:
    healthy += 1
```

---

### ❌ Using `elif` for independent checks

```python
if cpu > 85:
    problems.append("cpu high")
elif memory > 90:
    problems.append("memory high")
```

🔴 Bug:
- memory check skipped

✔ Fix:

```python
if cpu > 85:
    problems.append("cpu high")

if memory > 90:
    problems.append("memory high")
```

---

### ❌ Overusing `else`

```python
if cpu > 85:
    ...
else:
    # assumes everything else is OK (not always true)
```

---

## 🧠 DECISION RULE

Ask:

> “Can more than one condition be true?”

| Answer | Use |
|------|-----|
| Yes | multiple `if` |
| No | `if / elif / else` |

---

## 🧪 REAL EXAMPLE

Each host must be:

- healthy OR
- unhealthy

Correct:

```python
if problems:
    result["unhealthy_hosts"] += 1
else:
    result["healthy_hosts"] += 1
```

✔ One classification only  

---

## ✅ SUMMARY

- `if` → first condition
- `elif` → alternative condition
- `else` → fallback
- multiple `if` → independent checks
- `if/elif/else` → mutually exclusive logic
- always avoid double-counting