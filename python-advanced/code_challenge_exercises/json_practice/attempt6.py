"""
Your function must:

def load_config(path: str) -> dict:

1. Load and parse the JSON file at `path`
   - Raise FileNotFoundError if the file does not exist
   - Raise ValueError if the file contains invalid JSON

2. Validate the top-level structure
   - The loaded data must be a dictionary, otherwise raise TypeError

3. Validate optional fields
   - "steps":
       * Default to an empty list if missing
       * Must be a list, otherwise raise TypeError
   - "allowed_ips":
       * Default to an empty list if missing
       * Must be a list, otherwise raise TypeError
       * Each element must be a string, otherwise raise TypeError

4. Validate overrides configuration
   - "overrides":
       * Default to an empty dictionary if missing
       * Must be a dictionary, otherwise raise TypeError

5. Determine active environment
   - Read ENV from environment variables
   - Normalize by stripping whitespace and converting to lowercase

6. Build the result configuration
   - Create a shallow copy of the base configuration to avoid mutation

7. Apply environment overrides (if applicable)
   - If ENV exists as a key in "overrides":
       * The override value must be a dictionary, otherwise raise TypeError
       * Merge it into the result using dict.update()
       * This replaces entire values (including lists like "steps" or "allowed_ips")

8. Finalize output
   - Remove the "overrides" key from the result only if an override was applied

9. Return the final configuration dictionary
"""

import json
import pprint
import os

def load_config(path: str):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {path}") from e

    if not isinstance(data, dict):
        raise TypeError(f"Config must be a dictionary, got: {type(data).__name__}")
    
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        raise TypeError(f"Must be a list, got: {type(steps).__name__}")
    
    allowed_ips = data.get("allowed_ips", [])
    if not isinstance(allowed_ips, list):
        raise TypeError(f"Allowed IP's mus be a list, got: {type(allowed_ips).__name__}")
    for ip in allowed_ips:
        if not isinstance(ip, str):
            raise TypeError(f"IP's must be strings, got: {type(ip).__name__}")

    env = os.environ.get("ENV", "").strip().lower()
    result = data.copy()
    overrides = data.get("overrides", {})
    if not isinstance(overrides, dict):
        raise TypeError(f"Must be a dictionary, got: {type(overrides).__name__}")
    if env in overrides:
        override_env = overrides.get(env)
        if not isinstance(override_env, dict):
            raise TypeError(f"Override for '{env}' must be a dictionary, got: {type(override_env).__name__}")

        result.update(override_env)
        result.pop("overrides", None)
    return result

if __name__ == "__main__":
    PATH = "/home/andre/DevOps-Practice/python-practice/python-advanced/code_challenge_exercises/json_practice/config.json"
    result = load_config(PATH)
    pprint.pprint(result)