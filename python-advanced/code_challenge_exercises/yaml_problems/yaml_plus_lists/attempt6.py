"""
Your function must:

1. Load a YAML file from a given path using yaml.safe_load

2. Raise a clear FileNotFoundError if the file does not exist

3. Raise a clear yaml.YAMLError if the YAML content is invalid

4. Ensure the loaded config is a dictionary
   - If not, raise a TypeError

5. Extract "steps" and "overrides" from the config
   - "steps" must be a list if it is not None
   - If "steps" is not a list, raise a TypeError

6. Read the ENV environment variable
   - Normalize it by stripping whitespace and converting to lowercase

7. Create a shallow copy of the config (do not mutate the original)

8. If ENV exists as a key inside "overrides":
   - Retrieve the corresponding override dictionary
   - Apply it to the copied config using dict.update()

9. Do not perform any deep merging
   - If "steps" exists in overrides, it replaces the original value entirely

10. Remove the "overrides" key from the final result

11. Return the final configuration dictionary
"""

import yaml
import pprint
import os

def load_config(PATH: str) -> dict:
    try:
        with open(PATH, 'r') as f:
            cfg = yaml.safe_load(f)
            if not isinstance(cfg, dict):
                raise TypeError(
                    f"Config must be a dictionary, got: {type(cfg).__name__}"
                    )
            steps, overrides = cfg["steps"], cfg["overrides"]
            if steps is not None:
                if not isinstance(steps, list):
                    raise TypeError(
                        f"Must be a list, got: {type(steps).__name__}"
                        )
            env = os.environ.get("ENV", "").strip().lower()
            result = cfg.copy()

            if env in overrides:
                overrides_env = overrides.get(env)
                result.update(overrides_env)

            result.pop("overrides", None)
            return result

    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"The config file is invalid YAML: {PATH}"
            )

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file {PATH} can not be found. Or does not exist"
            )
    
if __name__ == "__main__":
    PATH = "./config2.yaml"
    result = load_config(PATH)
    pprint.pprint(result, indent=4)