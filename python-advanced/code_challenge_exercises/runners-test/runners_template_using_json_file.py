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
import random
import json


def generate_runners_to_file(n=100, path="runners.json"):
    tag_pool = ["linux", "docker", "gpu", "k8s", "arm", "windows"]

    runners = [
        {
            "name": f"runner-{i}",
            "online": random.choice([True, False]),
            "disk_gb": random.randint(1, 350),
            "tags": random.sample(tag_pool, random.randint(0, 3)),
        }
        for i in range(1, n + 1)
    ]

    data = {"runners": runners}

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def validate_runners(path: str) -> dict:
    usable = []
    rejected = {}

    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{path}' does not exist or cannot be found")

    if not isinstance(data, dict):
        raise TypeError(f"Must be a dictionary, got: {type(data).__name__}")

    runners = data.get("runners")

    if not isinstance(runners, list):
        raise TypeError(f"Value must be type list. Instead got: {type(runners).__name__}")

    for runner in runners:
        if not isinstance(runner, dict):
            raise TypeError(f"Each runner must be type dict. Instead got: {type(runner).__name__}")

        name = runner.get("name")
        online = runner.get("online")
        disk_gb = runner.get("disk_gb")
        tags = runner.get("tags")

        if not isinstance(name, str):
            raise TypeError(f"Value must be type str. Instead got: {type(name).__name__}")

        if not isinstance(online, bool):
            raise TypeError(f"Value must be type bool. Instead got: {type(online).__name__}")

        if not isinstance(disk_gb, int):
            raise TypeError(f"Value must be type int. Instead got: {type(disk_gb).__name__}")

        if not isinstance(tags, list):
            raise TypeError(f"Value must be type list. Instead got: {type(tags).__name__}")

        if not online:
            rejected[name] = "The runner is offline"
            continue

        if disk_gb < 10:
            rejected[name] = "The disk space is below threshold minimum"
            continue

        if "docker" not in tags:
            rejected[name] = "Missing required 'docker' tag"
            continue

        usable.append(name)

    return {
        "usable": usable,
        "rejected": rejected,
    }


PATH = "/home/andre/DevOps-Practice/python-practice/python-entry/runners-test/runners.json"
result = validate_runners(PATH)
pprint.pprint(result, indent=4)