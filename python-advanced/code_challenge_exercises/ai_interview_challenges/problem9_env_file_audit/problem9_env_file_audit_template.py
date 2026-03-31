"""

ENV FILE AUDIT — JUNIOR / MID-LEVEL

GOAL:
Implement a function that reads a .env file and performs basic validation
and analysis of environment variables.

You are auditing a .env file to identify:
- how many valid variables are defined
- which variables have empty values
- which variable names are duplicated
- which variables contain potentially sensitive keywords

The .env file format:
- Each valid line is KEY=VALUE
- Lines may contain whitespace
- Ignore empty lines
- Ignore comments (lines starting with "#")
- Ignore invalid lines that do not contain "="
- Ignore invalid lines where the key is empty

Example file:

# Application settings
APP_ENV=production
LOG_LEVEL=info

# Database config
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=secret
DB_PASSWORD=another_secret

# API keys
API_KEY=
SERVICE_TOKEN=abc123token

# Misc
CACHE_ENABLED=true
TIMEOUT=30

# Invalid / edge cases
INVALID_LINE_NO_EQUALS
=missing_key
EMPTY_VALUE=

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define:
    audit_env_file(file_path: str) -> dict

[ ] Initialize:

    results = {
        "total_variables": 0,
        "empty_values": [],
        "duplicate_variables": [],
        "sensitive_variables": []
    }

[ ] Create:
    seen_variables = set()
    duplicates = set()

[ ] Define sensitive keywords:
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Use a try block

[ ] Open the file using a context manager:
    with open(file_path, "r") as f:

[ ] Loop through each line in the file

[ ] Handle:
    - file not found
    - unexpected errors

[ ] On exception:
    - print an error message
    - return results

========================================================
3) LINE PROCESSING
--------------------------------------------------------
For each line:

[ ] Strip whitespace from the line

[ ] Skip the line if:
    - it is empty
    - it starts with "#"

[ ] Skip the line if it does not contain "="

========================================================
4) KEY-VALUE EXTRACTION
--------------------------------------------------------
[ ] Split the line at the first "=" only:
    key, value = line.split("=", 1)

[ ] Strip whitespace from both key and value

[ ] If key is empty:
    - skip the line

========================================================
5) COUNT VARIABLES
--------------------------------------------------------
[ ] Only after confirming the line is valid:
    - increment results["total_variables"]

Note:
A valid variable must:
- contain "="
- have a non-empty key

========================================================
6) EMPTY VALUE CHECK
--------------------------------------------------------
[ ] If value is empty:
    - append key to results["empty_values"]

Example:
    API_KEY=
    EMPTY_VALUE=

========================================================
7) DUPLICATE DETECTION
--------------------------------------------------------
[ ] If key is already in seen_variables:
    - add key to duplicates set

[ ] Else:
    - add key to seen_variables

Note:
- duplicates should appear only once in duplicate_variables
- use a set for duplicates, then convert to a sorted list later

========================================================
8) SENSITIVE VARIABLE DETECTION
--------------------------------------------------------
[ ] Convert the key to uppercase

[ ] Check whether any keyword in:
    ["PASSWORD", "SECRET", "KEY", "TOKEN"]
    appears inside the uppercase key

[ ] If yes:
    - append the original key to results["sensitive_variables"]

Examples of sensitive keys:
- DB_PASSWORD
- API_KEY
- SERVICE_TOKEN

Note:
- if a sensitive variable appears more than once, it may appear
  more than once in sensitive_variables

========================================================
9) FINAL PROCESSING
--------------------------------------------------------
After the main for loop finishes:

[ ] Convert duplicates set to a sorted list:
    results["duplicate_variables"] = sorted(duplicates)

[ ] Sort:
    - results["empty_values"]
    - results["sensitive_variables"]

========================================================
10) RETURN VALUE
--------------------------------------------------------
[ ] Return results

========================================================
Expected Result (for the example file above)
--------------------------------------------------------
{
    "total_variables": 12,
    "empty_values": ["API_KEY", "EMPTY_VALUE"],
    "duplicate_variables": ["DB_PASSWORD"],
    "sensitive_variables": [
        "API_KEY",
        "DB_PASSWORD",
        "DB_PASSWORD",
        "SERVICE_TOKEN"
    ]
}
"""