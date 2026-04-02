"""
TRY / EXCEPT CHEAT SHEET (when to use each pattern)

--------------------------------------------------
1) RE-RAISE WITH CONTEXT  →  "I can't fix it, but I improve the error"
--------------------------------------------------
Use inside helper / library functions.

Why:
- You want the caller to still handle the error
- You add useful debugging context
- You DO NOT hide the failure

Example:
"""
def load_rules(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        # add context, preserve original traceback
        raise FileNotFoundError(f"Rules file missing: {path}") from e


"""
--------------------------------------------------
2) PRINT / HANDLE  →  "This is the final stop (user-facing)"
--------------------------------------------------
Use at the top level (CLI, main script, API boundary).

Why:
- This is where you communicate with the user
- The program likely exits or stops here

Example:
"""
if __name__ == "__main__":
    try:
        rules = load_rules("firewall_rules.json")
    except FileNotFoundError:
        print("Error: firewall_rules.json not found")


"""
--------------------------------------------------
3) IGNORE / FALLBACK  →  "It's okay if this fails"
--------------------------------------------------
Use only when the error is expected and harmless.

Why:
- The file/resource is optional
- You have a safe fallback

Example:
"""
try:
    with open("optional_config.json") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}  # fallback instead of failing


"""
--------------------------------------------------
QUICK DECISION RULES
--------------------------------------------------

Ask yourself:

1. Can I fix or recover from this error here?
   - YES → handle it (fallback/retry)
   - NO  → go to #2

2. Am I the final layer (talking to the user)?
   - YES → print/log the error
   - NO  → re-raise with context

3. Is this failure harmless/optional?
   - YES → ignore or fallback
   - NO  → do NOT swallow it


--------------------------------------------------
COMMON MISTAKES (avoid these)
--------------------------------------------------

❌ Swallowing errors in helper functions
"""
def bad_load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print("error")  # BAD: caller can't react properly


"""
❌ Losing traceback (harder to debug)
"""
def bad_raise(path):
    try:
        with open(path):
            pass
    except FileNotFoundError:
        raise FileNotFoundError("Missing file")  # BAD


"""
✔ Correct version (preserve original error)
"""
def good_raise(path):
    try:
        with open(path):
            pass
    except FileNotFoundError as e:
        raise FileNotFoundError("Missing file") from e


"""
--------------------------------------------------
ONE-LINE MEMORY TRICK
--------------------------------------------------

- Library code  → raise
- Entry point   → print
- Optional case → fallback

--------------------------------------------------
"""