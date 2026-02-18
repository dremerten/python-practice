'''
Your function must:

def load_config(path: str) -> dict:

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
            cfg =  yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file at {path} can not be found or does not exist"
            ) from e
    except yaml.YAMLError as e:
        raise ValueError(
            f"The config file at {path} is invalid YAML"
            ) from e
    if not isinstance(cfg, dict):
        raise TypeError(f"The config file must be a dictionary. Instead got: {type(cfg).__name__}")

    steps = cfg.get("steps")
    if steps is not None and not isinstance(steps, list):
        raise TypeError(
            f"The 'steps' must be a list"
            )
    
    env = os.environ.get("ENV", "").strip().lower()
    overrides = cfg.get("overrides", {})
    result = cfg.copy()

    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        result.update(env_overrides)

    result.pop("overrides", None)
    return result

if __name__ =="__main__":
    cfg = load_config("./config2.yaml")
    pprint.pprint(cfg, indent=4)
    
