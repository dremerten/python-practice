"""
ENV FILE AUDIT — JUNIOR / MID-LEVEL

GOAL:
Implement a function that reads a .env file and performs basic validation
and analysis of environment variables.

You are auditing a .env file to identify:
- how many variables are defined
- which variables have empty values
- which variable names are duplicated
- which variables contain potentially sensitive keywords

The .env file format:
- Each line is KEY=VALUE
- Lines may contain whitespace
- Ignore empty lines and comments (lines starting with "#")

Example file:

APP_ENV=production
DB_HOST=localhost
DB_PASSWORD=secret
API_KEY=
LOG_LEVEL=info
DB_PASSWORD=another_secret

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: audit_env_file(file_path: str) -> dict

[ ] Initialize:
    results = {
        "total_variables": 0,
        "empty_values": [],
        "duplicate_variables": [],
        "sensitive_variables": []
    }

    seen_variables = set()
    duplicates = set()

    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Use a try block

[ ] Open the file using a context manager

[ ] Loop through each line in the file

[ ] Handle:
    - file not found
    - unexpected errors

[ ] On exception:
    - print error message
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
[ ] Split the line at the first "=":
    key, value = line.split("=", 1)

[ ] Strip whitespace from both key and value

[ ] If key is empty:
    - skip the line

========================================================
5) COUNT VARIABLES
--------------------------------------------------------
[ ] Increment results["total_variables"]

========================================================
6) EMPTY VALUE CHECK
--------------------------------------------------------
[ ] If value is empty:
    - append key to results["empty_values"]

========================================================
7) DUPLICATE DETECTION
--------------------------------------------------------
[ ] If key is already in seen_variables:
    - add key to duplicates set
[ ] Else:
    - add key to seen_variables

========================================================
8) SENSITIVE VARIABLE DETECTION
--------------------------------------------------------
[ ] Convert key to uppercase

[ ] If any keyword in sensitive_keywords is found in the key:
    - append key to results["sensitive_variables"]

========================================================
9) FINAL PROCESSING
--------------------------------------------------------
[ ] Convert duplicates set to a sorted list:
    results["duplicate_variables"] = sorted(duplicates)

[ ] Sort:
    - empty_values
    - sensitive_variables

========================================================
10) RETURN VALUE
--------------------------------------------------------
[ ] Return results

========================================================
Expected Result (for sample above)
--------------------------------------------------------
{
    "total_variables": 6,
    "empty_values": ["API_KEY"],
    "duplicate_variables": ["DB_PASSWORD"],
    "sensitive_variables": [
        "API_KEY",
        "DB_PASSWORD",
        "DB_PASSWORD"
    ]
}
"""