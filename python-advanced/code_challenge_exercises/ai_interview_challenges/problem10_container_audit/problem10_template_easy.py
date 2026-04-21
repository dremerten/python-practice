"""
INTERVIEW CHALLENGE: CONTAINER DEPLOYMENT AUDIT

Implement exactly:
- validate_container(container: dict) -> list[str]
- audit_deployments(containers: list[dict]) -> dict

Also include these imports:
- import pprint
- import json

Do NOT change:
- constant names
- required keys
- disallowed tag values
- allowed restart policy values
- error message text
- return structure
- field names


#### Note #######

# to debug
with open("container_deployments.json") as f:
    containers = json.load(f)

for container in containers:
    validate_container(container)

======================================================================
1) CONSTANTS
======================================================================

[ ] Define a constant set named DISALLOWED_TAGS with exactly these values:
    - "latest"

[ ] Define a constant set named REQUIRED_KEYS containing exactly these keys:
    - container_id
    - environment
    - image
    - tag
    - privileged
    - restart_policy
    - cpu_limit
    - memory_limit

[ ] Define a constant set named ALLOWED_RESTART_POLICIES with exactly these values:
    - "always"
    - "unless-stopped"
    - "on-failure"

[ ] Define a constant tuple named ALLOWED_MEMORY_SUFFIXES with exactly these values:
    - "Mi"
    - "Gi"

======================================================================
2) FUNCTION: validate_container(container)
======================================================================

GOAL
[ ] Validate one container deployment
[ ] Return a list of problems
[ ] Return an empty list if the container is valid

SETUP
[ ] Create a variable named problems
[ ] problems must start as an empty list

INPUT VALIDATION
[ ] Check whether container is a dictionary
[ ] If container is not a dictionary:
    [ ] Return EXACTLY:
        ["Invalid container: not a dictionary"]

CONTAINER ID
[ ] Read container_id from container
[ ] If container_id is missing, use "<unknown>" as default value

REQUIRED KEYS
[ ] Create a variable named missing_keys
[ ] Compare REQUIRED_KEYS against the keys present in container (container.keys())
[ ] Store any missing keys (difference "-") in a variable named missing_keys

[ ] If missing_keys is not empty:
    [ ] Append EXACTLY this string to problems:

        f"Container {container_id}: missing required keys: {sorted(missing_keys)}"

    [ ] Return problems immediately

----------------------------------------------------------------------
VALIDATIONS
Run the following checks in this exact order.
All messages in this section must be appended to problems.
----------------------------------------------------------------------

PRIVILEGED
[ ] Evaluate container["privileged"]

[ ] If container["privileged"] is not False:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: privileged mode must be disabled"

TAG
[ ] Read tag from container["tag"]

[ ] If tag is in DISALLOWED_TAGS:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: disallowed tag '{tag}'"

RESTART POLICY
[ ] Read restart_policy from container["restart_policy"]

[ ] If restart_policy is not in ALLOWED_RESTART_POLICIES:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: invalid restart policy '{restart_policy}'"

CPU LIMIT
[ ] Read cpu_limit from container["cpu_limit"]

[ ] Use a try/except TypeError block

[ ] Inside the try block:
    [ ] Check whether cpu_limit is less than or equal to 0

[ ] If cpu_limit is less than or equal to 0:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: cpu_limit {cpu_limit} must be greater than 0"

[ ] Inside the except TypeError block:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: invalid cpu_limit value '{cpu_limit}'"

MEMORY LIMIT
[ ] Read memory_limit from container["memory_limit"]

[ ] If memory_limit is not a string:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: invalid memory_limit '{memory_limit}'"

[ ] Otherwise:
    [ ] Check whether memory_limit ends with ALLOWED_MEMORY_SUFFIXES

[ ] If memory_limit does end with ALLOWED_MEMORY_SUFFIXES:
    [ ] Create a variable named numeric_part
    [ ] numeric_part must be memory_limit[:-2]

    [ ] Use a try/except ValueError block

    [ ] Inside the try block:
        [ ] Convert numeric_part to int
        [ ] Check whether the converted value is less than or equal to 0

    [ ] If the converted value is less than or equal to 0:
        [ ] Append EXACTLY this string:

            f"Container {container_id}: invalid memory_limit '{memory_limit}'"

    [ ] Inside the except ValueError block:
        [ ] Append EXACTLY this string:

            f"Container {container_id}: invalid memory_limit '{memory_limit}'"

[ ] Else:
    [ ] Append EXACTLY this string:

        f"Container {container_id}: invalid memory_limit '{memory_limit}'"

RETURN VALUE
[ ] Return problems

======================================================================
3) FUNCTION: audit_deployments(containers)
======================================================================

GOAL
[ ] Validate all container deployments
[ ] Aggregate findings
[ ] Decide whether the deployment audit passes

RESULT STRUCTURE
[ ] Create a variable named result
[ ] result must start as EXACTLY:

    {
        "audit_passed": False,
        "environment": None,
        "total_containers": 0,
        "valid_containers": 0,
        "invalid_containers": 0,
        "flagged_containers": [],
        "reasons": [],
    }

INPUT VALIDATION
[ ] Check whether containers is a list

[ ] If containers is not a list:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Invalid input: containers must be provided as a list"

    [ ] Return result immediately

INITIAL METRICS
[ ] Set result["total_containers"] to len(containers)

[ ] Create a variable named environments
[ ] environments must start as an empty set

LOOP THROUGH CONTAINERS
[ ] Process each container in containers

FOR INVALID CONTAINER ENTRIES
[ ] If a container entry is not a dictionary:
    [ ] Increment result["invalid_containers"] by 1
    [ ] Append EXACTLY this string to result["flagged_containers"]:
        "<unknown>"
    [ ] Append EXACTLY this string to result["reasons"]:
        "Invalid container: not a dictionary"
    [ ] Continue to the next container

FOR VALID CONTAINER ENTRIES
[ ] Read container_id from the container
[ ] If container_id is missing, use "<unknown>"

[ ] Read environment from the container
[ ] If environment is missing, use None

[ ] If environment is not None:
    [ ] Add environment to the environments set

CONTAINER VALIDATION
[ ] Call validate_container(container)
[ ] Store the returned list in a variable named problems

CLASSIFICATION
[ ] If problems is not empty:
    [ ] Increment result["invalid_containers"] by 1
    [ ] Append container_id to result["flagged_containers"]
    [ ] Extend result["reasons"] with all strings from problems

[ ] Otherwise:
    [ ] Increment result["valid_containers"] by 1

----------------------------------------------------------------------
POST-PROCESSING RULES
All messages in this section must be added to result["reasons"].
----------------------------------------------------------------------

ENVIRONMENT CONSISTENCY
[ ] If the number of items in environments is exactly one:
    [ ] Use a built-in function that returns the count of elements in environments, 
    then take the only value using an iterator and assign it to result["environment"]

[ ] Elif len(environments) > 1:
    [ ] Append EXACTLY this string to result["reasons"]:

        "Containers belong to multiple environments"

ENVIRONMENT REQUIREMENT
[ ] If result["environment"] != "production":
    [ ] Append EXACTLY this string to result["reasons"]:

        "Environment is not production"

FINAL DECISION
[ ] Set result["audit_passed"] to True only if ALL of the following are true:
    [ ] result["invalid_containers"] == 0
    [ ] len(environments) == 1
    [ ] result["environment"] == "production"

RETURN VALUE
[ ] Return result

======================================================================
4) MAIN EXECUTION BLOCK
======================================================================

[ ] Add this exact main guard:

    if __name__ == "__main__":

[ ] Inside it, use a try block

[ ] Open the file named "container_deployments.json" in read mode

[ ] Load the JSON contents into a variable named containers using json.load(file)

[ ] Call audit_deployments(containers)
[ ] Store the returned value in a variable named result

[ ] Print the result using:
    pprint.pprint(result)

EXCEPTIONS
[ ] Add an except FileNotFoundError block
[ ] Print EXACTLY:
    "Error: container_deployments.json file was not found."

[ ] Add an except json.JSONDecodeError block
[ ] Print EXACTLY:
    "Error: container_deployments.json contains invalid JSON."

======================================================================
EXPECTED RESULTS
Using this container_deployments.json input:
======================================================================

Expected output:

{
    "audit_passed": False,
    "environment": None,
    "total_containers": 6,
    "valid_containers": 3,
    "invalid_containers": 3,
    "flagged_containers": [
        "ctr-002",
        "ctr-003",
        "ctr-005",
    ],
    "reasons": [
        "Container ctr-002: disallowed tag 'latest'",
        "Container ctr-003: privileged mode must be disabled",
        "Container ctr-005: invalid restart policy 'sometimes'",
        "Container ctr-005: cpu_limit -1 must be greater than 0",
        "Container ctr-005: invalid memory_limit '2048'",
        "Containers belong to multiple environments",
        "Environment is not production",
    ],
}
"""