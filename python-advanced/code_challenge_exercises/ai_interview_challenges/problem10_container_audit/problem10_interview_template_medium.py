"""
INTERVIEW CHALLENGE: CONTAINER DEPLOYMENT AUDIT

You are given a list of container deployment configurations loaded from JSON.
Each container is represented as a dictionary.

Your task is to implement a small audit utility that:
- validates each container
- aggregates all findings
- determines whether the overall deployment passes audit

Implement exactly these functions:
- validate_container(container: dict) -> list[str]
- audit_deployments(containers: list[dict]) -> dict

Also include these imports:
- import pprint
- import json

Do NOT change:
- function names
- parameter names
- constant names
- result field names
- error message text

======================================================================
1) CONSTANTS
======================================================================

Define these constants exactly:

DISALLOWED_TAGS
- type: set
- value: {"latest"}

REQUIRED_KEYS
- type: set
- values:
    - "container_id"
    - "environment"
    - "image"
    - "tag"
    - "privileged"
    - "restart_policy"
    - "cpu_limit"
    - "memory_limit"

ALLOWED_RESTART_POLICIES
- type: set
- values:
    - "always"
    - "unless-stopped"
    - "on-failure"

ALLOWED_MEMORY_SUFFIXES
- type: tuple
- values:
    - "Mi"
    - "Gi"

======================================================================
2) FUNCTION: validate_container(container)
======================================================================

Use this exact function signature:

    def validate_container(container: dict) -> list[str]:

Purpose:
- Validate one container dictionary
- Return a list of problem strings
- Return an empty list if the container is valid

Expected structure:

1. Create:
    problems = []

2. Input validation
- If container is not a dictionary, return exactly:
    ["Invalid container: not a dictionary"]

3. Read:
    container_id = container.get("container_id", "<unknown>")

4. Check required keys
- Create:
    missing_keys = REQUIRED_KEYS - container.keys()

- If any keys are missing:
    append exactly:
    f"Container {container_id}: missing required keys: {sorted(missing_keys)}"

- Then return problems immediately

5. Run these validations in this order:

A. Privileged mode
- Check:
    container["privileged"]

- If it is not False, append exactly:
    f"Container {container_id}: privileged mode must be disabled"

B. Tag
- Read:
    tag = container["tag"]

- If tag is in DISALLOWED_TAGS, append exactly:
    f"Container {container_id}: disallowed tag '{tag}'"

C. Restart policy
- Read:
    restart_policy = container["restart_policy"]

- If restart_policy is not in ALLOWED_RESTART_POLICIES, append exactly:
    f"Container {container_id}: invalid restart policy '{restart_policy}'"

D. CPU limit
- Read:
    cpu_limit = container["cpu_limit"]

- Use try/except TypeError
- In the try block:
    if cpu_limit <= 0:
        append exactly:
        f"Container {container_id}: cpu_limit {cpu_limit} must be greater than 0"

- In the except TypeError block:
    append exactly:
    f"Container {container_id}: invalid cpu_limit value '{cpu_limit}'"

E. Memory limit
- Read:
    memory_limit = container["memory_limit"]

- If memory_limit is not a string:
    append exactly:
    f"Container {container_id}: invalid memory_limit '{memory_limit}'"

- Otherwise:
    - check whether memory_limit ends with ALLOWED_MEMORY_SUFFIXES
    - if it does:
        create:
            numeric_part = memory_limit[:-2]

        use try/except ValueError
        convert numeric_part to int

        if int(numeric_part) <= 0:
            append exactly:
            f"Container {container_id}: invalid memory_limit '{memory_limit}'"

        if conversion fails, append exactly:
            f"Container {container_id}: invalid memory_limit '{memory_limit}'"

    - if it does not end with an allowed suffix:
        append exactly:
        f"Container {container_id}: invalid memory_limit '{memory_limit}'"

6. Return:
    problems

======================================================================
3) FUNCTION: audit_deployments(containers)
======================================================================

Use this exact function signature:

    def audit_deployments(containers: list[dict]) -> dict:

Purpose:
- Validate all containers
- Aggregate findings
- Determine whether the overall audit passes

Create this result dictionary exactly:

    result = {
        "audit_passed": False,
        "environment": None,
        "total_containers": 0,
        "valid_containers": 0,
        "invalid_containers": 0,
        "flagged_containers": [],
        "reasons": [],
    }

Expected structure:

1. Input validation
- If containers is not a list:
    append exactly:
    "Invalid input: containers must be provided as a list"

- Return result immediately

2. Initial setup
- Set:
    result["total_containers"] = len(containers)

- Create:
    environments = set()

3. Loop through each container in containers

4. If a container entry is not a dictionary:
- increment:
    result["invalid_containers"] += 1

- append to flagged_containers:
    "<unknown>"

- append to reasons:
    "Invalid container: not a dictionary"

- continue to the next item

5. For valid dictionary entries:
- read:
    container_id = container.get("container_id", "<unknown>")
    environment = container.get("environment", None)

- if environment is not None:
    environments.add(environment)

- call:
    problems = validate_container(container)

6. Classification
- If problems is not empty:
    - increment invalid_containers
    - append container_id to flagged_containers
    - extend reasons with problems

- Otherwise:
    - increment valid_containers

7. Post-processing rules

A. Environment consistency
- If len(environments) == 1:
    set:
        result["environment"] = next(iter(environments))

- Elif len(environments) > 1:
    append exactly:
        "Containers belong to multiple environments"

B. Environment requirement
- If result["environment"] != "production":
    append exactly:
        "Environment is not production"

8. Final decision
Set:

    result["audit_passed"] = (
        result["invalid_containers"] == 0
        and len(environments) == 1
        and result["environment"] == "production"
    )

9. Return:
    result

======================================================================
4) MAIN EXECUTION BLOCK
======================================================================

Add this exact main guard:

    if __name__ == "__main__":

Inside it:

1. Use a try block
2. Open:
    "container_deployments.json"
3. Load with:
    containers = json.load(file)
4. Call:
    result = audit_deployments(containers)
5. Print with:
    pprint.pprint(result)

Add these exception handlers:

except FileNotFoundError:
    print("Error: container_deployments.json file was not found.")

except json.JSONDecodeError:
    print("Error: container_deployments.json contains invalid JSON.")

======================================================================
WHAT THE INTERVIEWER IS LOOKING FOR
======================================================================

- Correct function signatures
- Clean use of helper function:
    validate_container(container)
- Correct variable names:
    problems
    missing_keys
    container_id
    restart_policy
    cpu_limit
    memory_limit
    numeric_part
    result
    environments
- Exact output structure
- Exact error strings
- Correct handling of edge cases
- Careful string matching, especially:
    "unless-stopped"

======================================================================
COMMON MISTAKES TO AVOID
======================================================================

- Using "unless_stopped" instead of "unless-stopped"
- Defining DISALLOWED_TAGS as a string instead of a set
- Forgetting to return early when required keys are missing
- Forgetting that result["environment"] stays None when environments are mixed
- Changing field names in result
- Changing the text of error messages
"""