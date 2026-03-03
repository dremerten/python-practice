'''

Now, write a script to read these files and identify the version mismatches.
The Goal: Find every service that exists in both files but has a different version number.

1. Open and load json files
2. Get the keys for both staging and prod
3. Need to find the intersection -> find common/shared keys
4. The Goal: Find every service that exists in both files but has a different version number.
5. for loop (services of intersection keys)
6. if/else staging != prod

NOTES:
If you want to find...	            Use this Set Op	Terminology to use
All possible services	            A | B	Union
Services in both	                A & B	Intersection
Services ONLY in Staging	        A - B	Difference
Services NOT in both	            A ^ B	Symmetric Difference
'''

import json

def load_json(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file does not exist or cannot be found: {path}"
        ) from e
    except json.JSONDecodeError as e:
        raise ValueError(
            f"The file is invalid JSON: {path}"
        ) from e

    if not isinstance(data, dict):
        raise TypeError(
            f"The file must be a dictionary. Instead got: {type(data).__name__}"
        )

    return data



