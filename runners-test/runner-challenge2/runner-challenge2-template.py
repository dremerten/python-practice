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

