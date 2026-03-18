"""
DEVOPS PYTHON CHALLENGE — CI RUNNER VALIDATION

GOAL
------------------------------------------------
You are given metadata about CI runners in a list of dictionaries.

Your task is to write a function that determines which runners are usable
for executing Docker-based CI jobs.

Some runners must be rejected depending on their state and configuration.


INPUT FORMAT
------------------------------------------------
Each runner is represented as a dictionary with the following fields:

name (str)      → runner hostname
online (bool)   → whether the runner is reachable
disk_gb (int)   → available disk space
tags (list)     → capabilities of the runner

Example input:

[
    {"name": "runner-1", "online": True,  "disk_gb": 50, "tags": ["linux", "docker"]},
    {"name": "runner-2", "online": False, "disk_gb": 80, "tags": ["linux"]},
    {"name": "runner-3", "online": True,  "disk_gb": 5,  "tags": ["docker"]},
    {"name": "runner-4", "online": True,  "disk_gb": 20, "tags": []}
]


FUNCTION REQUIREMENTS
------------------------------------------------
Create the function:

validate_runners(runners: list) -> dict

The function must return a dictionary with the following structure:

{
    "usable": [...],
    "rejected": {...}
}


USABLE RUNNERS
------------------------------------------------
A runner is considered usable if ALL of the following are true:

• runner is online
• runner has at least 10GB disk space
• runner has the "docker" tag


REJECTED RUNNERS
------------------------------------------------
If a runner fails validation, store it in the rejected dictionary.

The key should be the runner name.

The value should be a short explanation.

Possible rejection reasons:

"The runner is offline"
"The disk space is below threshold minimum"
"Missing required 'docker' tag"


TYPE VALIDATION
------------------------------------------------
You must validate the input types for the following fields:

name      → must be str
online    → must be bool
disk_gb   → must be int
tags      → must be list

If any type is incorrect, raise a TypeError.

Example message format:

Value must be type int. Instead got: str


EXPECTED OUTPUT FORMAT
------------------------------------------------
Example output:

{
    "usable": ["runner-1"],
    "rejected": {
        "runner-2": "The runner is offline",
        "runner-3": "The disk space is below threshold minimum",
        "runner-4": "Missing required 'docker' tag"
    }
}


CONSTRAINTS
------------------------------------------------
• Do not use external libraries
• Use only standard Python
• No regex
• Prefer readability and clear logic

"""


import pprint

runners = [
    {"name": "runner-1", "online": True,  "disk_gb": 50, "tags": ["linux", "docker"]},
    {"name": "runner-2", "online": False, "disk_gb": 80, "tags": ["linux"]},
    {"name": "runner-3", "online": True,  "disk_gb": 5,  "tags": ["docker"]},
    {"name": "runner-4", "online": True,  "disk_gb": 20, "tags": []},
]

def validate_runners(runners: list) -> dict:
    usable = []
    rejected = {}

    for runner in runners:
        name = runner.get("name", "<unknown>")
        pass



    return {
        "usable": usable,
        "rejected": rejected
    }


