"""
API RESPONSE AUDIT — MID-LEVEL CHECKLIST

GOAL:
Implement a function that parses an API log file and produces summary metrics.

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: audit_api_responses(file_path)
[ ] Initialize:
    - results dict with:
        status_counts
        slow_endpoints
        most_frequent_client_error
    - a separate dict to track client error counts

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
    timestamp
    endpoint
    status_code_text
    response_time_text

[ ] Ensure none of these are empty

========================================================
6) TYPE CONVERSION
--------------------------------------------------------
[ ] Convert status_code and response_time to integers
[ ] Skip the line if conversion fails

========================================================
7) STATUS CODE AGGREGATION
--------------------------------------------------------
[ ] Maintain a count of each status code

========================================================
8) SLOW REQUEST TRACKING
--------------------------------------------------------
[ ] Define "slow" as response_time >= 1000 ms
[ ] Track count of slow requests per endpoint

========================================================
9) CLIENT ERROR TRACKING
--------------------------------------------------------
[ ] Identify client errors (400–499)
[ ] Track occurrences per endpoint

========================================================
10) FINAL COMPUTATION
--------------------------------------------------------
[ ] Determine the endpoint with the highest client error count
[ ] If none exist, leave as None

========================================================
11) RETURN VALUE
--------------------------------------------------------
[ ] Return the results dictionary

========================================================
NOTES
--------------------------------------------------------
- Input may contain malformed lines — ignore them safely
- Do not let a single bad line break processing
- Favor simple, readable logic over clever shortcuts
"""