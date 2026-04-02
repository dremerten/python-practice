"""
INTERVIEW CHALLENGE: DEPLOYMENT READINESS EVALUATION

Implement exactly:
- validate_host(host: dict) -> list[str]
- evaluate_deployment(host_reports: list[dict]) -> dict

Do NOT change:
- constant names
- required keys
- threshold values
- error message text
- return structure

======================================================================
1) CONSTANTS
======================================================================

[ ] Define a constant named REQUIRED_AGENT_VERSION with this exact value:
    "3.2.1"

[ ] Define a constant set named REQUIRED_KEYS containing exactly these keys:
    - hostname
    - environment
    - reachable
    - disk_usage_percent
    - cpu_load_percent
    - memory_usage_percent
    - agent_version
    - last_checkin_minutes_ago

======================================================================
2) FUNCTION: validate_host(host)
======================================================================

GOAL
[ ] Validate one host
[ ] Return a list of problems
[ ] Return an empty list if the host is valid

SETUP
[ ] Create a variable named problems
[ ] problems must start as an empty list

INPUT VALIDATION
[ ] Check whether host is a dictionary
[ ] If host is not a dictionary:
    [ ] Return EXACTLY:
        ["Invalid host: not a dictionary"]

HOSTNAME
[ ] Read hostname from host
[ ] If hostname is missing, use "<unknown>" as default value

REQUIRED KEYS
[ ] Create a variable named missing_keys
[ ] missing_keys must be a list of required keys that are not present in host

[ ] If missing_keys is not empty:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} is missing required keys. Missing {missing_keys}"

    [ ] Return the problems list immediately
    [ ] Do not perform any more validation checks for this host

----------------------------------------------------------------------
VALIDATIONS
Run the following checks in this exact order.
All error messages in this section must be appended to the problems list.
----------------------------------------------------------------------

CONNECTIVITY
[ ] Evaluate host["reachable"]

[ ] If host["reachable"] is not True:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} is offline"

DISK USAGE
[ ] Use a try/except TypeError block when evaluating host["disk_usage_percent"]

[ ] Inside the try block:
    [ ] Evaluate whether host["disk_usage_percent"] is greater than or equal to 90

[ ] If host["disk_usage_percent"] is greater than or equal to 90:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} has exceeded max disk usage percent limit. Currently at {host['disk_usage_percent']}"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} disk usage percent is invalid"

CPU LOAD
[ ] Use a try/except TypeError block when evaluating host["cpu_load_percent"]

[ ] Inside the try block:
    [ ] Evaluate whether host["cpu_load_percent"] is greater than 85

[ ] If host["cpu_load_percent"] is greater than 85:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} has exceeded max cpu load percent limit. Currently at {host['cpu_load_percent']}"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} cpu load percent is invalid"

MEMORY USAGE
[ ] Use a try/except TypeError block when evaluating host["memory_usage_percent"]

[ ] Inside the try block:
    [ ] Evaluate whether host["memory_usage_percent"] is greater than 90

[ ] If host["memory_usage_percent"] is greater than 90:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} has exceeded max memory usage limit. Currently at {host['memory_usage_percent']}"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} memory usage percent is invalid"

AGENT VERSION
[ ] Evaluate host["agent_version"]

[ ] If host["agent_version"] does not equal REQUIRED_AGENT_VERSION:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} is not running the correct agent version. {REQUIRED_AGENT_VERSION} is required"

LAST CHECK-IN
[ ] Use a try/except TypeError block when evaluating host["last_checkin_minutes_ago"]

[ ] Inside the try block:
    [ ] Evaluate whether host["last_checkin_minutes_ago"] is greater than 5

[ ] If host["last_checkin_minutes_ago"] is greater than 5:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} has exceeded max checkin period of 5mins. Currently at {host['last_checkin_minutes_ago']}"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string to the problems list:

        f"Host {hostname} last checkin is invalid"

RETURN VALUE
[ ] After all checks above are complete, return the problems list

======================================================================
3) FUNCTION: evaluate_deployment(host_reports)
======================================================================

GOAL
[ ] Validate all hosts
[ ] Aggregate results
[ ] Decide whether deployment is allowed

RESULT STRUCTURE
[ ] Create a variable named result
[ ] result must start as EXACTLY:

    {
        "deployment_allowed": False,
        "environment": None,
        "total_hosts": 0,
        "healthy_hosts": 0,
        "unhealthy_hosts": 0,
        "failed_hosts": [],
        "reasons": [],
    }

INPUT VALIDATION
[ ] Check whether host_reports is a list

[ ] If host_reports is not a list:
    [ ] Append EXACTLY this string to result["reasons"]:

        "host report must be a list"

    [ ] Return result immediately

INITIAL METRICS
[ ] Set result["total_hosts"] to the number of items in host_reports

[ ] Create a variable named environments
[ ] environments must start as an empty set

LOOP THROUGH HOSTS
[ ] Process each host in host_reports

FOR INVALID HOST ENTRIES
[ ] If a host entry is not a dictionary:
    [ ] Increment result["unhealthy_hosts"] by 1
    [ ] Append EXACTLY this string to result["failed_hosts"]:
        "<unknown>"
    [ ] Append EXACTLY this string to result["reasons"]:
        "Invalid host: not a dictionary"
    [ ] Continue to the next host

FOR VALID HOST ENTRIES
[ ] Read hostname from the host
[ ] If hostname is missing, use "<unknown>"

[ ] Read environment from the host
[ ] If environment is missing, use None

[ ] If environment is not None:
    [ ] Add that value to the environments set

HOST VALIDATION
[ ] Call validate_host(host)
[ ] Store the returned list in a variable named problems

CLASSIFICATION
[ ] If problems is not empty:
    [ ] Increment result["unhealthy_hosts"] by 1
    [ ] Append hostname to result["failed_hosts"]
    [ ] Extend result["reasons"] with all strings from problems

[ ] Otherwise:
    [ ] Increment result["healthy_hosts"] by 1

----------------------------------------------------------------------
POST-PROCESSING RULES
All messages in this section must be added to result["reasons"].
Hint: Outside the for loop
----------------------------------------------------------------------

ENVIRONMENT CONSISTENCY
[ ] If the environments set contains exactly one value:
    [ ] Set result["environment"] to that single value
    HINT: Use next(iter(environments))

[ ] If the environments set contains more than one value:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Hosts belong to multiple environments"

MINIMUM HOST COUNT
[ ] If result["total_hosts"] is less than 3:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Total hosts are less than 3"

DEPLOYMENT TARGET
[ ] If result["environment"] is not "production":
    [ ] Append EXACTLY this string to result["reasons"]:

        "Deployment environment must be production"

FINAL DECISION
[ ] Set result["deployment_allowed"] to True only if ALL of the following are true:
    [ ] result["total_hosts"] is at least 3
    [ ] result["unhealthy_hosts"] is 0
    [ ] the environments set contains exactly one value
    [ ] result["environment"] is "production"

RETURN VALUE
[ ] Return result

EXPECTED RESULTS:

{
    "deployment_allowed": False,
    "environment": None,
    "total_hosts": 10,
    "healthy_hosts": 4,
    "unhealthy_hosts": 6,
    "failed_hosts": [
        "web-04",
        "web-05",
        "web-06",
        "web-07",
        "web-08",
        "web-09",
    ],
    "reasons": [
        "Host web-04 is offline",
        "Host web-05 has exceeded max disk usage percent limit. Currently at 95",
        "Host web-06 has exceeded max cpu load percent limit. Currently at 90",
        "Host web-07 has exceeded max memory usage limit. Currently at 95",
        "Host web-08 is not running the correct agent version. 3.2.1 is required",
        "Host web-09 has exceeded max checkin period of 5mins. Currently at 10",
        "Hosts belong to multiple environments",
        "Deployment environment must be production",
    ],
}
"""