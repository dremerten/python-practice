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
        conversion
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
[ ] If response_time >= 1000:
    - Check if endpoint exists in results["slow_endpoints"]
    - If not, initialize it to 0
    - Increment the count for that endpoint

========================================================
9) CLIENT ERROR TRACKING
--------------------------------------------------------
[ ] Check if the status code is in the 400–499 range
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