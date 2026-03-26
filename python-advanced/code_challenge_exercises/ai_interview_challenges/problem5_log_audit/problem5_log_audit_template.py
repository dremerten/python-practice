"""
API RESPONSE AUDIT — MID-LEVEL CHECKLIST

GOAL:
Read a log file line by line and:
- Populate results["status_counts"]
- Populate results["slow_endpoints"]
- Set results["most_frequent_client_error"]

========================================================
1) FUNCTION SCAFFOLDING
--------------------------------------------------------
[ ] Define a function named audit_api_responses that takes file_path
[ ] Inside the function, create:
    results = {
        "status_counts": {},
        "slow_endpoints": {},
        "most_frequent_client_error": None
    }
[ ] Also create:
    client_error_counts = {}

========================================================
2) OPEN THE FILE
--------------------------------------------------------
[ ] Use:
    with open(file_path, "r") as file:
[ ] Loop through the file:
    for line in file:

========================================================
3) CLEAN EACH LINE
--------------------------------------------------------
[ ] Strip whitespace from line
[ ] If line is empty after stripping:
    continue

========================================================
4) SPLIT THE LINE
--------------------------------------------------------
[ ] Split line using:
    parts = line.split("|")
[ ] If len(parts) is not 4:
    continue

========================================================
5) EXTRACT THE FIELDS
--------------------------------------------------------
[ ] Set:
    timestamp = parts[0].strip()
    endpoint = parts[1].strip()
    status_code_text = parts[2].strip()
    response_time_text = parts[3].strip()

========================================================
6) CHECK REQUIRED VALUES
--------------------------------------------------------
[ ] If timestamp is empty:
    continue
[ ] If endpoint is empty:
    continue
[ ] If status_code_text is empty:
    continue
[ ] If response_time_text is empty:
    continue

========================================================
7) CONVERT TO INTS SAFELY
--------------------------------------------------------
[ ] Use try/except to convert:
    status_code = int(status_code_text)
    response_time_ms = int(response_time_text)
[ ] If try conversion fails then except (ValueError or TypeError):
    continue

========================================================
8) COUNT STATUS CODES
--------------------------------------------------------
[ ] If status_code not in results["status_counts"]:
    results["status_counts"][status_code] = 0
[ ] Increase:
    results["status_counts"][status_code] += 1

========================================================
9) COUNT SLOW ENDPOINTS
--------------------------------------------------------
Definition of slow:
- response_time_ms >= 1000

[ ] If response_time_ms >= 1000:
    [ ] If endpoint not in results["slow_endpoints"]:
        results["slow_endpoints"][endpoint] = 0
    [ ] Increase:
        results["slow_endpoints"][endpoint] += 1

========================================================
10) COUNT CLIENT ERROR ENDPOINTS
--------------------------------------------------------
Client errors:
- status_code from 400 to 499 inclusive

[ ] If 400 <= status_code <= 499:
    [ ] If endpoint not in client_error_counts:
        client_error_counts[endpoint] = 0
    [ ] Increase:
        client_error_counts[endpoint] += 1

========================================================
11) FIND THE MOST FREQUENT CLIENT ERROR ENDPOINT
--------------------------------------------------------
[ ] After the file read loop, check:
    if client_error_counts:
[ ] Set:
    results["most_frequent_client_error"] = max(
        client_error_counts,
        key=client_error_counts.get
    )

========================================================
12) RETURN THE RESULTS
--------------------------------------------------------
[ ] Return results

========================================================

EXPECTED RESULT
--------------------------------------------------------
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
========================================================
"""