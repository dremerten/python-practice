"""
=============================================================================
CODING CHALLENGE: Infrastructure Deployment Gate
=============================================================================

Your team deploys software to a fleet of hosts. Before any deployment goes
out, you need to verify that every host in the fleet is healthy enough to
receive it.

You will receive host data as a list of dictionaries loaded from a JSON file.
An example host report looks like this:

    {
        "hostname": "web-prod-01",
        "environment": "production",
        "reachable": true,
        "disk_usage_percent": 72,
        "cpu_load_percent": 45,
        "memory_usage_percent": 60,
        "agent_version": "3.2.1",
        "last_checkin_minutes_ago": 2
    }

PART 1: validate_host(host)
Write a function that validates a single host report and returns a list of
strings describing any problems found. An empty list means the host is healthy.
You decide what "healthy" means based on the data available.

PART 2: evaluate_deployment(host_reports)
Write a second function that accepts the full list of host reports and returns
a dictionary summarizing whether a deployment should be allowed and why.

  The function MUST:
    - Accept a list of host reports
    - Return a single dictionary
    - Call your validate_host function — do not rewrite that logic here
    - Determine whether deployment is allowed based on the four conditions
      defined in the clarifications below
    - Collect all reasons why deployment was blocked

  The result dictionary MUST contain:
    - deployment_allowed  → boolean
    - environment         → the environment string, or None if undetermined
    - total_hosts         → count of all hosts passed in
    - healthy_hosts       → count of hosts with no problems
    - unhealthy_hosts     → count of hosts with any problems
    - failed_hosts        → list of hostnames that failed validation
    - reasons             → list of all problem strings collected

  Structure guidance:

  PHASE 1 — Initialize your result dict before anything else.
    Set deployment_allowed to False, environment to None, all counts to 0,
    and failed_hosts and reasons to empty lists. This is your return value
    no matter what happens next.

  PHASE 2 — Validate the input itself.
    Before looping, confirm that host_reports is actually a list. If it
    isn't, append a reason and return early.

  PHASE 3 — Set total_hosts.
    Assign the length of host_reports to result["total_hosts"] before
    the loop — you already know the total count at this point.

  PHASE 4 — Track environments across hosts.
    You need to detect whether all hosts share the same environment or
    belong to multiple. Think about what data structure lets you collect
    unique values without duplicates as you loop. You will use this after
    the loop to set result["environment"].

  PHASE 5 — Loop through each host.
    For each item in the list, handle these cases in order:
      a) If the item is not a dict — increment unhealthy_hosts, append
         "<unknown>" to failed_hosts, append a reason, then skip to the
         next item with continue.
      b) Get the hostname with a fallback of "<unknown>".
      c) Get the environment value. If it exists, add it to your
         environment tracker from Phase 4.
      d) Call validate_host() on the host. If problems were returned,
         increment unhealthy_hosts, append the hostname to failed_hosts,
         and add all the problems to reasons. Note: you are adding a list
         of strings to reasons, not a single string — pick the right list
         method. If no problems, increment healthy_hosts.

  PHASE 6 — Resolve the environment after the loop.
    Look at your environment tracker:
      - Exactly one unique value → set result["environment"] to that value
      - More than one → append a reason saying hosts belong to multiple
        environments

  PHASE 7 — Fleet-level checks.
    These run after the loop regardless of individual host results:
      - If total_hosts is less than 3, append a reason
      - If result["environment"] is not "production", append a reason

  PHASE 8 — Set deployment_allowed.
    Only set it to True if ALL of the following are true at once:
      - total_hosts is 3 or more
      - unhealthy_hosts is exactly 0
      - exactly one unique environment was seen
      - that environment is "production"
    This should be a single compound if statement, not nested ifs.

  PHASE 9 — Return the result dict.

PART 3:
Inside an if __name__ == "__main__" block, open "host_reports.json" using
a context manager inside a try/except. Handle two specific exceptions:
  - FileNotFoundError — print a message saying the file can't be found
  - json.JSONDecodeError — print a message saying the file is invalid JSON
Load the contents with the json module, call evaluate_deployment() with the
result, and print the output using json.dumps() with an indent of 4.

=============================================================================
CLARIFICATIONS (questions you would ask the interviewer):
=============================================================================

Q: What defines a healthy host?
A: A healthy host must meet ALL of the following:
     - It is reachable
     - Disk usage is below 90%
     - CPU load is below 85%
     - Memory usage is below 90%
     - It is running agent version 3.2.1
     - It checked in within the last 5 minutes

Q: Are there any constants I should define?
A: Yes. Define the required agent version and the set of fields you expect
   every host report to contain as constants at the top of your file.

Q: What conditions must be true for deployment to be allowed?
A: All hosts must be healthy, there must be at least 3 hosts, all hosts must
   belong to the same environment, and that environment must be "production".

Q: What should the result dictionary contain?
A: At minimum: whether deployment is allowed, the environment, total host
   count, healthy and unhealthy counts, a list of failed hostnames, and a
   list of reasons why deployment was blocked.

Q: How should I handle bad data — missing keys, wrong types, non-dict entries?
A: Treat them as unhealthy hosts. Capture the problem in your reasons list
   rather than letting the function crash.

Q: Should I use try/except blocks?
A: It is a valid choice since the data is coming from JSON and you cannot
   guarantee types. If you use them, catch TypeError specifically — not a
   bare except — and only wrap the line that can actually raise the exception.
   An alternative is an explicit isinstance check before the comparison.
   Either approach is acceptable as long as you can explain your reasoning.

=============================================================================
"""