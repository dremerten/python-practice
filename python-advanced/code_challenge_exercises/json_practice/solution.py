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

9. Return the final copy of the configuration dictionary
"""

import json
import os
import pprint

def load_config(path: str) -> dict:
    """
    Load a JSON configuration file, validate its structure, and apply environment overrides.

    Args:
        path (str): Path to the JSON config file.

    Returns:
        dict: A final copy of the configuration dictionary with environment overrides applied.
    """
    # 1. Load JSON from file
    try:
        with open(path, 'r') as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file at {path} cannot be found or does not exist."
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError(
            f"The config file at {path} contains invalid JSON."
        ) from e

    # 2. Validate top-level structure
    if not isinstance(cfg, dict):
        raise TypeError(f"The config must be a dictionary, got: {type(cfg).__name__}")

    # 3. Validate optional 'steps'
    steps = cfg.get("steps", [])
    if not isinstance(steps, list):
        raise TypeError(f"'steps' must be a list, got: {type(steps).__name__}")

    # 4. Validate optional 'allowed_ips'
    allowed_ips = cfg.get("allowed_ips", [])
    if not isinstance(allowed_ips, list):
        raise TypeError(f"'allowed_ips' must be a list, got: {type(allowed_ips).__name__}")
    if not all(isinstance(ip, str) for ip in allowed_ips):
        raise TypeError(f"All 'allowed_ips' must be strings, got: {allowed_ips}")

    # 5. Validate 'overrides'
    overrides = cfg.get("overrides", {})
    if not isinstance(overrides, dict):
        raise TypeError(f"'overrides' must be a dictionary, got: {type(overrides).__name__}")

    # 6. Determine active environment
    env = os.environ.get("ENV", "").strip().lower()

    # 7. Work on a copy to avoid mutating original config
    result = cfg.copy()

    # 8. Apply environment-specific overrides if they exist
    env_overrides = overrides.get(env)
    if isinstance(env_overrides, dict):
        result.update(env_overrides)
    elif env_overrides is not None:
        raise TypeError(
            f"Override for environment '{env}' must be a dictionary, got: {type(env_overrides).__name__}"
        )

    # 9. Remove overrides key before returning
    result.pop("overrides", None)

    return result


if __name__ == "__main__":
    cfg = load_config("./config.json")
    pprint.pprint(cfg, indent=4)


