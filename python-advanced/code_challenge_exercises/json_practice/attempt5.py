'''
Your function must:

def load_config(path: str) -> dict:

1. Load JSON from path using json.load
2. Fail safely if:
    - File doesn’t exist
    - JSON is invalid
3. Ensure the loaded config is a dictionary
4. If steps exists, ensure it is a list
5. If allowed_ips exists, ensure it is a list of strings
6. Read environment variable ENV
7. If ENV matches a key under overrides:
8. Apply the override dict to the base config (like update())
9. If the override includes steps or allowed_ips, it replaces the entire list
10. Do not mutate the original config dict
11. Remove overrides key before returning
12. Return the final config dict
'''

import json
import os
import pprint

PATH="/home/andre/DevOps-Practice/python-practice/python-entry/json_practice/config.json"

def load_config(path: str) ->  dict:
    try:
        with open(PATH, 'r') as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file at: {path} does not exist or can't be found!"
            )
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"The file is invalid JSON"
            )
    if not isinstance(cfg, dict):
        raise TypeError(
            f"Config file must be a dictionary, got: {type(cfg).__name__}"
            )

    steps = cfg.get("steps", None)
    if not isinstance(steps, list):
        raise TypeError(
            f"Must be a list, got: {type(steps).__name__}"
            )
    
    allowed_ips = cfg.get("allowed_ips")
    if allowed_ips is not None:
        if not isinstance(allowed_ips, list):
            raise TypeError(
                f"The allowed ips must be a list"
                )
        if not all(isinstance(ip, str) for ip in allowed_ips):
            raise TypeError(
                f"The ips must be strings {allowed_ips}"
                )

    env = os.environ.get("ENV", "").strip().lower()
    overrides = cfg.get("overrides", {})
    result = cfg.copy()
    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        if isinstance(env_overrides, dict):
            result.update(env_overrides)
    result.pop("overrides", None)
    return result
    
if __name__ == "__main__":
    cfg = load_config("/home/andre/DevOps-Practice/python-practice/json_practice/config.json")
    pprint.pprint(cfg, indent=4)







