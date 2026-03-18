"""
validate_runners(path: str) -> dict

Requirements:

1. Load JSON safely from the given path.
2. Fail safely if:
   - The file does not exist.
   - The JSON is invalid.
3. Ensure the loaded config is a dictionary.
4. Ensure the "runners" key exists and its value is a list.
5. Iterate over each item in "runners":
   - If the item is not a dictionary, skip it.
6. Read the environment variable ENV (lowercased).
7. Determine min_disk_gb:
   - Default value is 10.
   - If "overrides" exists in the config and is a dictionary:
     - If ENV matches a key in "overrides":
       - If "min_disk_gb" exists in that env override, use it.
       - If the override value is not an integer, raise a clear error.
8. A runner is considered usable if ALL of the following are true:
   - "online" is True
   - "disk_gb" is greater than or equal to min_disk_gb
   - "docker" is present in the "tags" list
9. Otherwise, the runner is rejected with the first failing reason:
   - "Runner is offline"
   - "Insufficient disk space"
   - "Missing required tag: 'docker'"
10. Do not mutate the original config or runner objects.
11. Return a dictionary in the following format:

{
  "usable": ["runner-1", ...],
  "rejected": {
    "runner-2": "Runner is offline",
    "runner-3": "Insufficient disk space"
  }
}
"""

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
                    raise TypeError(f"Must be int. Instead got: {type(override_min).__name__}")
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
            rejected[name] = "Insufficient disk space"
            continue
        if 'docker' not in tags:
            rejected[name] = "Missing 'docker' tags"
            continue
        usable.append(name)

    return {"usable": usable, "rejected": rejected}

if __name__ == "__main__":
    cfg = validate_runners("/home/andre/DevOps-Practice/python-practice/runners-test/runner-challenge2/runners.json")
    pprint.pprint(cfg, indent=4)










