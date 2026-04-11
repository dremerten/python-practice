"""
=============================================================================
CODING CHALLENGE: Infrastructure Deployment Readiness Evaluator
=============================================================================

OVERVIEW:
---------
You are a DevOps engineer responsible for writing a pre-deployment gate check.
Before any release goes out, your script must inspect a list of host health
reports (loaded from a JSON file) and decide whether a deployment is allowed
to proceed. Your program must validate each host individually, then evaluate
the entire fleet as a whole.

=============================================================================
SETUP & IMPORTS
=============================================================================

You will need three standard library modules:
  - One for pretty-printing Python data structures
  - One for working with JSON data
  - No third-party packages needed

You will also define two constants at the top of your file:
  1. A string representing the required agent version. Use "3.2.1"
  2. A set of strings representing the keys that EVERY valid host report
     must contain. The required keys are:
       hostname, environment, reachable, disk_usage_percent,
       cpu_load_percent, memory_usage_percent, agent_version,
       last_checkin_minutes_ago

=============================================================================
PART 1 — validate_host(host)
=============================================================================

Write a function that accepts a single host report (expected to be a dict)
and returns a LIST OF STRINGS describing every problem found with that host.
An empty list means the host is healthy.

Follow this exact order of checks:

  STEP 1 — Type check
    Before anything else, confirm the input is actually a dictionary.
    If it isn't, immediately return a list containing one string:
      "Invalid host: not a dictionary"

  STEP 2 — Get the hostname
    Pull the "hostname" value from the dict. Use a fallback of "<unknown>"
    in case the key doesn't exist. You'll use this in all your error messages.

  STEP 3 — Missing key check
    Using a list comprehension, find all keys from your REQUIRED_KEYS constant
    that are absent from the host dict. If any are missing, append an
    appropriate error message (include the list of missing keys in the message)
    and IMMEDIATELY return — do not continue checking the rest.

  STEP 4 — Reachability check
    Check if the "reachable" field is EXACTLY the boolean True (not just
    truthy — use identity comparison). If not, append a message saying the
    host is offline.

  STEP 5 — Disk usage check (wrap in try/except TypeError)
    If disk_usage_percent is greater than or equal to 90, append a message
    that includes the current value.

  STEP 6 — CPU load check (wrap in try/except TypeError)
    If cpu_load_percent is strictly greater than 85, append a message
    that includes the current value.

  STEP 7 — Memory usage check (wrap in try/except TypeError)
    If memory_usage_percent is strictly greater than 90, append a message
    that includes the current value.

  STEP 8 — Agent version check
    Compare agent_version to your required version constant using
    inequality (!=). If they don't match, append a message that tells
    the user what version IS required.

  STEP 9 — Last check-in check (wrap in try/except TypeError)
    If last_checkin_minutes_ago is strictly greater than 5, append a message
    that includes the current value and mentions the 5-minute max.

  STEP 10 — Return
    Return the problems list (which may be empty if all checks passed).

=============================================================================
PART 2 — evaluate_deployment(host_reports)
=============================================================================

Write a function that accepts a list of host report dicts and returns a
SINGLE DICTIONARY summarizing the overall deployment readiness.

  STEP 1 — Initialize the result dictionary
    Create a dict with these exact keys and starting values:
      "deployment_allowed"  → False
      "environment"         → None
      "total_hosts"         → 0
      "healthy_hosts"       → 0
      "unhealthy_hosts"     → 0
      "failed_hosts"        → empty list
      "reasons"             → empty list

  STEP 2 — Type check on input
    If host_reports is NOT a list, append "host report must be a list" to
    reasons and immediately return the result dict.

  STEP 3 — Set total_hosts
    Assign the length of the host_reports list to result["total_hosts"].

  STEP 4 — Initialize an environments tracker
    Create an empty SET. You'll use this to collect all unique environment
    values seen across hosts.

  STEP 5 — Loop through each host
    For each item in host_reports:

      a) If the item is not a dict:
           - Increment unhealthy_hosts
           - Append "<unknown>" to failed_hosts
           - Append "Invalid host: not a dictionary" to reasons
           - Use "continue" to skip to the next item

      b) Get the hostname (fallback: "<unknown>")
         Get the environment value (fallback: None)

      c) If the environment value is not None, add it to your environments set.

      d) Call your validate_host() function on the host.
         - If any problems were returned:
             * Increment unhealthy_hosts
             * Append the hostname to failed_hosts
             * Extend (not append) reasons with the list of problems
         - Otherwise:
             * Increment healthy_hosts

  STEP 6 — Resolve the environment field
    After the loop, look at your environments set:
      - If it has exactly 1 item → set result["environment"] to that value
        (Hint: use next(iter(...)) to pull a single item from a set)
      - If it has more than 1 item → append a message saying hosts belong
        to multiple environments

  STEP 7 — Fleet-level validations
    a) If total_hosts is less than 3, append a message saying so.
    b) If result["environment"] is not "production", append a message saying
       the environment must be production.

  STEP 8 — Determine if deployment is allowed
    Set deployment_allowed to True ONLY IF all four conditions are met:
      1. total_hosts is 3 or more
      2. unhealthy_hosts is exactly 0
      3. The environments set has exactly 1 entry
      4. result["environment"] equals "production"

  STEP 9 — Return the result dictionary.

=============================================================================
PART 3 — main block
=============================================================================

Inside an  if __name__ == "__main__"  block:

  1. Open a file called "host_reports.json" in read mode using a context
     manager (with statement).
  2. Use your JSON module to load the file contents into a variable.
  3. Call evaluate_deployment() with that variable.
  4. Pretty-print the result using your pprint module, with an indent of 4.

Optionally, leave a commented-out debug loop at the bottom that would iterate
over each host and call validate_host() — this can help isolate individual
host issues during testing.

=============================================================================
TIPS & REMINDERS
=============================================================================

  - All threshold comparisons matter: disk uses >=90, but cpu and memory
    use strictly >85 and >90 respectively. Pay attention.
  - Each try/except block should ONLY catch TypeError — not a bare except.
  - The "reachable" check uses  "is not True"  not  "!= True". Be intentional.
  - The reasons list uses .extend() when adding problems from validate_host,
    not .append() — think about why.
  - Your environments variable is a set, not a list. Order doesn't matter;
    uniqueness does.
  - The deployment gate requires ALL four conditions simultaneously — one
    compound if statement, not nested ifs.

=============================================================================
"""