"""
API RESPONSE AUDIT — MID-LEVEL CHECKLIST

GOAL:
Implement a function that parses an API log file and produces summary metrics.

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: audit_api_responses(file_path: str) -> dict

[ ] Initialize:
    - results (dict) for FINAL output:
        status_counts -> dict[int, int]
        slow_endpoints -> dict[str, int | float]
        most_frequent_client_error -> str | None

    - client_error_counts -> dict[str, int]  # helper (NOT part of results)

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open the file using a context manager
[ ] Handle the case where the file does not exist
[ ] Iterate line by line

========================================================
3) LINE NORMALIZATION
--------------------------------------------------------
[ ] Strip whitespace
[ ] Skip empty lines

========================================================
4) BASIC VALIDATION
--------------------------------------------------------
[ ] Split using "|"
[ ] Skip lines that do not have exactly 4 fields

========================================================
5) FIELD EXTRACTION
--------------------------------------------------------
[ ] Extract:
    timestamp -> str
    endpoint -> str
    status_code_str -> str
    response_time_str -> str

[ ] Validate:
    if not timestamp or not endpoint or not status_code_str or not response_time_str:
        continue

========================================================
6) TYPE CONVERSION
--------------------------------------------------------
[ ] Convert:
    status_code_str -> int
    response_time_str -> int

[ ] Use try/except:
    try:
        status_code = int(status_code_str)
        response_time = int(response_time_str)
    except ValueError:
        continue

========================================================
7) STATUS CODE AGGREGATION
--------------------------------------------------------
[ ] For each status_code:
    - Check if status_code exists in results["status_counts"]
    - If not, initialize it to 0
    - Increment the count for that status_code

========================================================
8) SLOW REQUEST TRACKING
--------------------------------------------------------
[ ] If response_time_ms >= 1000:
    - Check if endpoint exists in results["slow_endpoints"]
    - If not, initialize it to 0
    - Increment the count for that endpoint

========================================================
9) CLIENT ERROR TRACKING
--------------------------------------------------------
[ ] If 400 <= status_code <= 499:
    - Check if endpoint exists in client_error_counts
    - If not, initialize it to 0
    - Increment the count for that endpoint

========================================================
10) FINAL COMPUTATION
--------------------------------------------------------
[ ] Outside the loop:

[ ] If client_error_counts is not empty:
    - Use max(...) with key=client_error_counts.get
    - Assign result to results["most_frequent_client_error"]

[ ] Otherwise:
    - Leave as None

========================================================
11) RETURN VALUE
--------------------------------------------------------
[ ] Return the results dictionary

========================================================
Expected Result:

{
    "status_counts": {
        401: 3,
        201: 3,
        500: 2,
        200: 2,
        403: 1,
        503: 1,
        404: 2
    },
    "slow_endpoints": {
        "/orders/create": 3,
        "/reports/daily": 3
    },
    "most_frequent_client_error": "/users/login"
}

"""

import pprint

def audit_api_responses(file_path: str) -> dict:
    results = {
        "status_counts": {},
        "slow_endpoints": {},
        "most_frequent_client_error": None
     }

    client_error_counts = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                line = line.split("|")
                if len(line) != 4:
                    continue

                timestamp = line[0].strip()
                endpoint = line[1].strip()
                status_code_str = line[2].strip()
                response_time_str = line[3].strip()
                if not timestamp or not endpoint or not status_code_str or not response_time_str:
                    continue

                try:
                    status_code = int(status_code_str)
                    response_time = int(response_time_str)
                except ValueError:
                    continue

                if status_code not in results["status_counts"]:
                    results["status_counts"][status_code] = 0
                results["status_counts"][status_code] += 1

                if response_time >= 1000:
                    if endpoint not in results["slow_endpoints"]:
                        results["slow_endpoints"][endpoint] = 0
                    results["slow_endpoints"][endpoint] += 1

                if 400 <= status_code <= 499:
                    if endpoint not in client_error_counts:
                        client_error_counts[endpoint] = 0
                    client_error_counts[endpoint] += 1

    except FileNotFoundError as e:
        raise FileNotFoundError from e

    if client_error_counts:
        results["most_frequent_client_error"] = max(
            client_error_counts,
            key=client_error_counts.get

        )

    return results

result = audit_api_responses(file_path="nginx.log")
pprint.pprint(result, indent=2)