'''
You are working on an infrastructure tool that loads service configuration from a YAML file.
The configuration may contain environment-specific overrides.

Your task is to load the YAML config and apply overrides based on an environment variable.


Requirements

1. Load the YAML file safely.
2. Raise a clear error if:
- The file does not exist
- The YAML is invalid

3. Read the environment variable ENV
- If ENV=ci, apply overrides.ci
- If ENV=production, apply overrides.production
- If ENV is unset or has no override, use the base config

4. Overrides should merge into the base config (not replace it entirely).
5. The final returned object must be a dictionary.
'''

import yaml
import os

def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The config file does not exist: {path}") from e
    except yaml.YAMLError as e:
        raise ValueError(f"The config is invalid yaml: {path}") from e
    
    if not isinstance(cfg, dict):
        raise TypeError("Config must be a dictionary")
    
    env = os.environ.get("ENV")
    result = cfg.copy()

    overrides = cfg.get("overrides", {})
    if isinstance(overrides, dict) and env in overrides:
        result.update(overrides[env])

    result.pop("overrides", None)

    return result

if __name__ == "__main__":
    config = load_config("config.yaml")
    print(config)






    
    


    

    