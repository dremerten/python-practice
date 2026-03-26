# 🧠 Python: Exists vs Empty (Cheat Sheet)

---

## 🔑 Core Rule (Memorize This)

if value:
    # exists AND not empty

if not value:
    # either None OR empty

---

## 📦 1. None (Existence Check Only)

if value is None:
    print("Does NOT exist")

if value is not None:
    print("Exists")

Use `is None` (NOT `== None`)

---

## 🔤 2. Strings

s = ""

if s:
    print("Not empty")

if not s:
    print("Empty or None")

### Explicit checks

if s == "":
    print("Empty string")

if s is None:
    print("Does not exist")

---

## 📚 3. Lists

lst = []

if lst:
    print("List has items")

if not lst:
    print("Empty or None")

### Explicit

if len(lst) == 0:
    print("Empty list")

---

## 🧾 4. Tuples

t = ()

if t:
    print("Not empty")

if not t:
    print("Empty tuple")

---

## 🧮 5. Dictionaries

d = {}

if d:
    print("Has keys")

if not d:
    print("Empty dict")

### Key existence

if "key" in d:
    print("Key exists")

---

## 🧊 6. Sets

s = set()

if s:
    print("Not empty")

if not s:
    print("Empty set")

---

## 🔢 7. Numbers (int, float)

Important: `0` is considered False

n = 0

if n:
    print("Non-zero")

if not n:
    print("Zero OR None")

### Safer check

if n is None:
    print("Does not exist")

if n == 0:
    print("Zero value")

---

## 📦 8. Boolean

flag = False

if flag:
    print("True")

if not flag:
    print("False")

---

## 🧰 9. Combined Safe Pattern (Production Style)

if value is None:
    print("Does not exist")
elif not value:
    print("Exists but empty")
else:
    print("Exists and has data")

---

## ⚠️ Common Gotchas

This mixes None + empty:

if not value:

This is TRUE for:
- None
- ""
- []
- {}
- 0
- False

---

## 🚀 Quick Reference Table

| Type   | Empty Value | if value | Notes |
|--------|------------|---------|------|
| None   | None       | False   | Use `is None` |
| String | ""         | False   | |
| List   | []         | False   | |
| Tuple  | ()         | False   | |
| Dict   | {}         | False   | |
| Set    | set()      | False   | |
| Int    | 0          | False   | ⚠️ tricky |
| Float  | 0.0        | False   | ⚠️ tricky |
| Bool   | False      | False   | |

---

## 🧠 TLDR

if value:
    pass  # has data

if value is None:
    ...
elif not value:
    ...
else:
    ...