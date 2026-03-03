"""
validate_runners(path: str) -> dict

Execution order / requirements (top to bottom):

1. Open the JSON file at the given path and load it safely.
2. Raise a clear error if:
   - The file does not exist.
   - The JSON is invalid.
3. Ensure the loaded config is a dictionary.
4. Read the "runners" key from the config.
5. Ensure "runners" exists and is a list.
6. Read the environment variable ENV (lowercased and stripped).
7. Set min_disk_gb to a default value of 10.
8. Read the "overrides" key from the config (default to {}).
9. If ENV is set and "overrides" is a dictionary:
   - Look up the ENV key inside "overrides".
   - If the ENV override is a dictionary:
     - Read "min_disk_gb" from it if present.
     - If present and not an integer, raise an error.
     - If present and an integer, override the default min_disk_gb value.
10. Initialize empty "usable" list and "rejected" dictionary.
11. Iterate over each item in the runners list:
    - If the runner is not a dictionary, skip it.
    - Extract name, online, disk_gb, and tags with safe defaults.
    - Normalize invalid types to safe defaults.
12. Evaluate runner usability rules in order:
    - If online is False, reject with reason "Runner is offline".
    - If disk_gb is less than min_disk_gb, reject with reason "Insufficient disk space".
    - If "docker" is not in tags, reject with reason "Missing required tag: 'docker'".
13. If all rules pass, add the runner name to the usable list.
14. After processing all runners, return the result dictionary:

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
   # 1-3
   try:
      with open(path, 'r') as f:
         cfg = json.load(f)
   except FileNotFoundError as e:
      raise FileNotFoundError(
         f"The config file can not be found or does not exist: {path}"
         ) from e
   except json.JSONDecodeError as e:
      raise ValueError(
         f"The config file is invalid JSON: {path}"
         ) from e
   if not isinstance(cfg, dict):
      raise TypeError(
         f"The config file must be a dictionary, got: {type(cfg).__name__}"
         )

   # 4-7
   runners = cfg.get("runners")
   if not isinstance(runners, list):
      raise TypeError(
         f"Must be a list, got {type(runners).__name__}"
         )
   env = os.environ.get("ENV", "").strip().lower()
   min_disk_gb = 10

   # 8-9
   overrides = cfg.get("overrides", {})
   if env and isinstance(overrides, dict):
      env_overrides = overrides.get(env)
      if isinstance(env_overrides, dict):
         override_min_disk = env_overrides.get("min_disk_gb")
         if override_min_disk is not None:
            if not isinstance(override_min_disk, int):
               raise TypeError(f"Must be a integer, got {type(override_min_disk).__name__}")
            min_disk_gb = override_min_disk
   # 10-14
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
         rejected[name] = "Missing required tag: 'docker'"
         continue
      usable.append(name)

   return{"usable": usable, "rejected": rejected}

if __name__ == "__main__":
   runner = validate_runners("/home/andre/DevOps-Practice/python-practice/runners-test/runner-challenge2/runners.json")
   pprint.pprint(runner, indent=4)

      




   






   