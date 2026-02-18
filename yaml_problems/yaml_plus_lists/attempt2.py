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
import pprint
import os

def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file does not exist or can not be found at: {path}"
            ) from e
    except yaml.YAMLError as e:
        raise ValueError(
            f"The config is invalid YAML. Please check {path}"
            ) from e
    if not isinstance(cfg, dict):
        raise TypeError(
            f"The config file {path} must be a dictionary. Instead got: {type(cfg).__name__}"
            )
    
    env = os.environ.get("ENV", "").strip().lower()
    result = cfg.copy()

    steps = cfg.get("steps")
    if steps is not None and not isinstance(steps, list):
        raise TypeError(
            f"'steps' must be a list. Instead got type: {type(steps).__name__}"
            )

    overrides = cfg.get("overrides", {})
    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        result.update(env_overrides)
    result.pop("overrides", None)
    return result

if __name__ == "__main__":
    cfg = load_config("/home/andre/DevOps-Practice/python-practice/yaml_problems/yaml_plus_lists/config2.yaml")
    pprint.pprint(cfg, indent=4)