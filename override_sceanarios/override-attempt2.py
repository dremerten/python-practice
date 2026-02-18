import json
import os
import pprint

def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file can not be found or does not exist: {path}"
            ) from e
    except json.JSONDecodeError as e:
        raise TypeError(
            f"The config file is invalid JSON: {path}"
            ) from e
    if not isinstance(cfg, dict):
        raise TypeError(
            f"The config must be a dictionary. Instead got: {type(cfg).__name__}"
            )
    env = os.environ.get("ENV", "").lower()
    result = cfg.copy()
    
    overrides = cfg.get("overrides", {})
    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        if isinstance(env_overrides, dict):
            result.update(env_overrides)
    
    result.pop("overrides", None)
    return result


if __name__ == "__main__":
    cfg = load_config(
        "/home/andre/DevOps-Practice/python-practice/override_sceanarios/config.json"
        )
    pprint.pprint(cfg, indent=4)

