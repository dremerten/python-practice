import yaml
import os
import pprint

def load_config(path: str) -> dict:
    try:
        with open(path, "r") as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config/yaml file cannot be found or does not exist: {path}"
        ) from e
    except yaml.YAMLError as e:
        raise ValueError(
            f"The config/yaml file is invalid YAML: {path}"
        ) from e

    if not isinstance(cfg, dict):
        raise TypeError(
            f"The config must be a dictionary. Instead got: {type(cfg).__name__}"
        )

    # Validate steps if present
    steps = cfg.get("steps")
    if steps is not None and not isinstance(steps, list):
        raise TypeError("steps must be a list")

    env = os.environ.get("ENV", "").strip().lower()
    result = cfg.copy()

    overrides = cfg.get("overrides", {})
    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        if isinstance(env_overrides, dict):
            # This will replace steps entirely if env_overrides contains "steps"
            result.update(env_overrides)

    result.pop("overrides", None)
    return result

if __name__ == "__main__":
    cfg = load_config("/home/andre/DevOps-Practice/python-practice/yaml_problems/yaml_plus_lists/config2.yaml")
    pprint.pprint(cfg, indent=4)