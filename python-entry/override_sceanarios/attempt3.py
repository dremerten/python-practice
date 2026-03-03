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
import pprint
import os

def load_config(path: str) -> dict:
   try:
      with open(path, 'r') as f:
         cfg = json.load(f)
   except FileNotFoundError as e:
      raise FileNotFoundError(
         f"The config file {path} can't be found or does not exist"
         )
   except json.JSONDecodeError as e:
      raise ValueError(f"The file must be valid JSON, got {type(path).__name__}")
   if not isinstance(cfg, dict):
      raise TypeError(
         f"Must be a dictionary, got {type(cfg).__name__}"
         )
   env = os.environ.get("ENV", "").strip().lower()
   overrides = cfg.get("overrides", {})
   if not isinstance(overrides, dict):
      raise TypeError(
         f"Must be a dictionary, got {type(overrides).__name__}"
         )
   result = cfg.copy()
   override_env = overrides.get(env)
   if env and isinstance(override_env, dict):
      result.update(override_env)
      result.pop("overrides", None)
   return result

if __name__ == "__main__":
   PATH = "/home/andre/DevOps-Practice/python-practice/override_sceanarios/config.json"
   result = load_config(PATH)
   print(result)









