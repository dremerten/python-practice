'''
Your function must:

1. Load JSON safely from path
2. Fail safely if:
    - File doesn’t exist
    -JSON is invalid
3. Ensure the loaded config is a dictionary
4. Ensure runners exists and is a list
5. Ensure each runner is a dictionary
6. Read environment variable ENV
7. Determine min_disk_gb:
    -Default = 10

8. If ENV matches a key under overrides, use that value

A runner is usable if:
- online is True
- disk_gb >= min_disk_gb
- "docker" is in tags
- Otherwise, the runner is rejected with a reason

Do not mutate the original config
Return a dictionary like:

{
  "usable": ["runner-1"],
  "rejected": {
    "runner-2": "Runner is offline",
    "runner-3": "Insufficient disk space"
  }
}
'''

import json
import os
import pprint

def validate_runners(path: str) -> dict:
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {path}") from e

    if not isinstance(cfg, dict):
        raise TypeError(f"Config must be a dict, got: {type(cfg).__name__}")

    runners = cfg.get("runners")
    if not isinstance(runners, list):
        raise TypeError(f"'runners' must be a list, got: {type(runners).__name__}")

    env = os.environ.get("ENV", "").strip().lower()
    min_disk_gb = 10

    overrides = cfg.get("overrides", {})
    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        if isinstance(env_overrides, dict):
            override_min = env_overrides.get("min_disk_gb")
            if override_min is not None:
                if not isinstance(override_min, int):
                    raise TypeError(f"min_disk_gb override must be int, got: {type(override_min).__name__}")
                min_disk_gb = override_min

    usable = []
    rejected = {}

    for runner in runners:
        if not isinstance(runner, dict):
            continue

        name = runner.get("name", "<unknown>")
        online = runner.get("online", False)
        disk_gb = runner.get("disk_gb", 0)
        tags = runner.get("tags", [])

        if not isinstance(name, str):
            name = "<unknown>"
        if not isinstance(online, bool):
            online = False
        if not isinstance(disk_gb, int):
            disk_gb = 0
        if not isinstance(tags, list):
            tags = []

        if not online:
            rejected[name] = "Runner is offline"
            continue
        if disk_gb < min_disk_gb:
            rejected[name] = f"Insufficient disk space (need {min_disk_gb}GB)"
            continue
        if "docker" not in tags:
            rejected[name] = "Missing required tag: 'docker'"
            continue

        usable.append(name)

    return {"usable": usable, "rejected": rejected}


if __name__ == "__main__":
    cfg = validate_runners("/home/andre/DevOps-Practice/python-practice/runners-test/runner-challenge2/runners.json")
    pprint.pprint(cfg, indent=4)






