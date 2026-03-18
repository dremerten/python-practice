'''
Your function must:

1. Load YAML from path (use yaml.safe_load)
2. Fail safely if:
    - File does not exist 
    - YAML is invalid
3. Ensure the loaded config is a dictionary
4. Ensure steps is a list if present (or raise a clear error)
5. Read environment variable ENV
6. If ENV matches a key under overrides:
7. Apply that override dict onto the base config using the same idea as update()
8. If the override includes steps, it replaces the entire steps list (no deep merge)
9. Do not mutate the original config dict
10. Remove overrides key before returning
11. Return the final config dict
'''

import yaml
import os
import pprint

def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file at: {path} can not be found"
            ) from e
    except yaml.YAMLError as e:
        raise ValueError(
            f"The config file: {path} is not valid YAML"
            )
    if not isinstance(cfg, dict):
        raise TypeError(
            f"The config must be a dictionary, got {type(cfg).__name__}"
            )
    steps = cfg.get("steps")
    if not isinstance(steps, list):
        raise TypeError(
            f"Must be a list, got: {type(steps).__name__}"
            )
    env = os.environ.get("ENV", "").strip().lower()
    results = cfg.copy()
    overrides = cfg.get("overrides", {})
    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        if not isinstance(env_overrides, dict):
            raise TypeError(
                f"Must be a dictionary, got: {type(env_overrides).__name__}"
                )
        results.update(env_overrides)        
        results.pop("overrides", {})
    return results


if __name__ == "__main__":
    PATH="/home/andre/DevOps-Practice/python-practice/yaml_problems/yaml_plus_lists/config2.yaml"
    cfg = load_config(PATH)
    pprint.pprint(cfg, indent=4)