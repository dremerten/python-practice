"""
CODE CHALLENGE: JSON Config Loader with ENV Overrides

Your task is to write the function below from scratch.

    def load_config(path: str) -> dict:

The function must load a JSON configuration file and apply
environment-specific overrides in a safe and predictable way.

------------------------------------------------------------
REQUIREMENTS
------------------------------------------------------------

1) Load JSON safely
   - Open the file at `path`
   - Parse it using json.load()
   - If the file does not exist:
       raise FileNotFoundError with a clear message
   - If the JSON is invalid:
       raise ValueError with a clear message

2) Validate the loaded data
   - The top-level JSON object MUST be a dictionary
   - If it is not a dictionary:
       raise TypeError explaining the actual type

3) Read environment
   - Read the ENV environment variable
   - Lowercase it
   - If ENV is missing or empty, treat it as "no overrides"

4) Work on a copy
   - Create a copy of the base config
   - Do NOT mutate the original loaded config

5) Handle overrides
   - Read the "overrides" key from the config (if present)
   - "overrides" must be a dictionary to be valid
   - If ENV matches a key inside overrides:
       - That value must be a dictionary
       - Merge it into the copied config using dict.update()

   Example structure:
   {
     "host": "localhost",
     "port": 8080,
     "debug": true,
     "overrides": {
       "dev":  {"debug": true},
       "prod": {"debug": false, "host": "api.company.com"}
     }
   }

6) Cleanup result
   - Remove the "overrides" key from the final result
   - Use .pop("overrides", None)

7) Return value
   - Return the final merged configuration dictionary

------------------------------------------------------------
SELF-CHECK (RUN THESE IN YOUR HEAD)
------------------------------------------------------------

- ENV unset  -> base config returned, no "overrides"
- ENV=dev   -> dev overrides applied
- ENV=prod  -> prod overrides applied
- Missing file -> FileNotFoundError
- Invalid JSON -> ValueError
- Top-level JSON list -> TypeError

------------------------------------------------------------
GOAL
------------------------------------------------------------

Focus on:
- Clear error handling
- Defensive type checks
- Clean, readable control flow
- Writing code in a logical top-to-bottom order

This is an entry-to-mid DevOps / Infrastructure Python exercise.
"""


import json
import os
import pprint

PATH="/home/andre/DevOps-Practice/python-practice/override_sceanarios/config2.json"

def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            base_cfg = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The config file at: {path} does not exist or can't be found"
            ) from e
    except json.JSONDecodeError as e:
        raise ValueError(
            f"The config file: {path} is invalid JSON!"
            ) from e
    if not isinstance(base_cfg, dict):
        raise TypeError(
            f"Must be a dictionary, got: {type(base_cfg).__name__}"
            )
    env = os.environ.get("ENV", "").strip().lower()
    overrides = base_cfg.get("overrides", {})
    result = base_cfg.copy()

    if env and isinstance(overrides, dict):
        env_overrides = overrides.get(env)
        if isinstance(env_overrides, dict):
            result.update(env_overrides)
    
    result.pop("overrides", None)
    return result
    
if __name__ == "__main__":
    cfg = load_config(PATH)
    print(cfg)


