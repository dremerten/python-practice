'''
You are working on an infrastructure tool that loads service configuration from a YAML file.
The configuration may contain environment-specific overrides.

Your task is to load the YAML config and apply overrides based on an environment variable.

Requirements

1. Load the YAML file safely.
2. Raise a clear error if:
- The file does not exist
- The YAML is invalid
- Validate config file is type dictionary

3. Read the environment variable ENV
- If ENV=ci, apply overrides.ci
- If ENV=production, apply overrides.production
- If ENV is unset or has no override, use the base config

4. Overrides should merge into the base config (not replace it entirely).
5. The final returned object must be a dictionary.
'''

import yaml
import os

def load_config(path: str) -> dict: # validate config is a dictionary type
    try:
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f) # converts yaml to python dictionary
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The config file provided does not exist or can't be found: {path}") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"The config is invalid YAML: {path}") from e
    if not isinstance(cfg, dict):
        raise TypeError(f"The config is not a dictionary. Instead got {type(cfg).__name__}!")
    
    env = os.environ.get("ENV", "").lower() # get environment variable and convert to lowercase for case-insensitive comparison
    overrides = cfg.get("overrides", {}) # get overrides section from config, default to empty dictionary if not present
    result = cfg.copy()

    if isinstance(overrides, dict) and env in overrides:
        result.update(overrides[env])

    result.pop("overrides", None)

    return result

if __name__ == "__main__":
    config = load_config("config.yaml")
    print(config)