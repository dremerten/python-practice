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
[ ] If conversion fails:
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
[ ] After the loop, check:
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
LOG FILE TO TEST WITH
--------------------------------------------------------
Create a file named: api_requests.log

Use this exact content:

2026-03-21T10:15:32Z | /users/login | 401 | 312
2026-03-21T10:15:35Z | /orders/create | 201 | 1208
2026-03-21T10:15:40Z | /users/login | 401 | 298
2026-03-21T10:15:45Z | /reports/daily | 500 | 1800
2026-03-21T10:15:50Z | /orders/create | 201 | 980
2026-03-21T10:15:55Z | /inventory/list | 200 | 150
2026-03-21T10:16:00Z | /users/login | 403 | 330
2026-03-21T10:16:05Z | /orders/create | 503 | 1420
2026-03-21T10:16:10Z | /reports/daily | 200 | 1100
2026-03-21T10:16:15Z | /users/profile | 404 | 210
bad line here
2026-03-21T10:16:25Z | /users/profile | abc | 210
2026-03-21T10:16:30Z | /inventory/list | 200 | xyz
2026-03-21T10:16:35Z | /users/login | 401 | 305
2026-03-21T10:16:40Z | /orders/create | 201 | 1000
2026-03-21T10:16:45Z | /users/profile | 404 | 220
2026-03-21T10:16:50Z | /reports/daily | 500 | 1750

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

import pprint


def audit_api_responses(file_path: str) -> dict:
    results = {
        "status_counts": {},
        "slow_endpoints": {},
        "most_frequent_client_error": None
    }
    client_error_counts = {}

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 4:
                    continue

                timestamp = parts[0].strip()
                endpoint = parts[1].strip()
                status_code_text = parts[2].strip()
                response_time_text = parts[3].strip()

                if not timestamp or not endpoint or not status_code_text or not response_time_text:
                    continue

                try:
                    status_code = int(status_code_text)
                    response_time_ms = int(response_time_text)
                except (ValueError, TypeError):
                    continue

                if status_code not in results["status_counts"]:
                    results["status_counts"][status_code] = 0
                results["status_counts"][status_code] += 1

                if response_time_ms >= 1000:
                    if endpoint not in results["slow_endpoints"]:
                        results["slow_endpoints"][endpoint] = 0
                    results["slow_endpoints"][endpoint] += 1

                if 400 <= status_code <= 499:
                    if endpoint not in client_error_counts:
                        client_error_counts[endpoint] = 0
                    client_error_counts[endpoint] += 1

    except FileNotFoundError:
        print(f"Error: {file_path} does not exist")
        return results

    if client_error_counts:
        results["most_frequent_client_error"] = max(
            client_error_counts,
            key=client_error_counts.get
        )

    return results


if __name__ == "__main__":
    path = "nginx.log"
    result = audit_api_responses(path)
    pprint.pprint(result, indent=2)