'''
Problem 1 — File + JSON handling (with basic error handling)

Write a function:

def load_config(path)
    ...

Requirements

1. Reads a JSON file from path and returns it as a Python dict.
2. If the file does not exist, raise a FileNotFoundError with a helpful message.
3. If the JSON is invalid, raise a ValueError with a helpful message.
4. If the JSON is valid but the top-level value is not a dict (e.g., it’s a list), raise a TypeError.
=====>  Example file (config.json)
'''

import json

def load_config(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The config file does not exist: {path}") from e
    except ValueError as e:
        raise ValueError(f"The config file is invaild JSON: {path}") from e
    
    if not isinstance(cfg, dict):
        raise TypeError(f"The config file is not a valid dictionary. It is type: {type(cfg)}")
    
    return cfg



if __name__ == "__main__":
    cfg = load_config("config-non.json")
    print(cfg)
    