"""
NGINX TRAFFIC REVIEW — MID-LEVEL CHECKLIST

GOAL:
Implement a function that parses an NGINX access log file and produces
infrastructure-focused summary metrics.

You are reviewing web traffic to identify:
- request method volume
- the busiest client IP
- which paths are producing server-side failures
- which paths are consistently slow
- which client IPs look suspicious based on repeated auth/access errors

Log format for each line:
timestamp | client_ip | method | path | status_code | bytes_sent | request_time

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: review_nginx_traffic(file_path: str) -> dict

[ ] Initialize:
    - results (dict) for FINAL output:
        method_counts -> dict[str, int]
        busiest_ip -> str | None
        server_error_paths -> dict[str, int]
        avg_slow_paths -> dict[str, float]
        suspicious_ips -> list[str]

    - ip_request_counts -> dict[str, int]
    - slow_path_tracker -> dict[str, list[float]]
    - suspicious_ip_counts -> dict[str, int]

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open the file using a context manager
[ ] Handle file not found
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
[ ] Skip lines that do not have exactly 7 fields

========================================================
5) FIELD EXTRACTION
--------------------------------------------------------
[ ] Extract fields:
    timestamp, client_ip, method, path,
    status_code_str, bytes_sent_str, request_time_str

[ ] Strip whitespace from each field

[ ] Skip if required fields are missing

========================================================
6) TYPE CONVERSION
--------------------------------------------------------
[ ] Convert:
    status_code -> int
    bytes_sent -> int
    request_time -> float

[ ] Use try/except to skip invalid lines

========================================================
7) METHOD AGGREGATION
--------------------------------------------------------
[ ] Count occurrences of each HTTP method

========================================================
8) BUSIEST IP TRACKING
--------------------------------------------------------
[ ] Count requests per IP

========================================================
9) SERVER ERROR PATH TRACKING
--------------------------------------------------------
[ ] Track paths with 5xx status codes

========================================================
10) SLOW PATH COLLECTION
--------------------------------------------------------
[ ] If request_time >= 1.0:
    collect values per path (DO NOT average yet)

========================================================
11) SUSPICIOUS IP TRACKING
--------------------------------------------------------
[ ] Track IPs with status codes:
    401, 403, 404, 429

========================================================
12) FINAL COMPUTATION
--------------------------------------------------------
[ ] After processing ALL lines (outside the file loop):

[ ] If ip_request_counts is not empty:
    - Use max(...) with key=ip_request_counts.get
    - Assign the result to results["busiest_ip"]

[ ] For avg_slow_paths:
    - Loop through slow_path_tracker
    - Only include paths with 3 or more slow requests
    - Compute the average request time for each qualifying path
    - Round to 3 decimals
    - Store in results["avg_slow_paths"]

[ ] For suspicious_ips:
    - Loop through suspicious_ip_counts
    - Include only IPs with 4 or more suspicious responses
    - Store them in results["suspicious_ips"]
    - Sort the final list

[ ] If ip_request_counts is empty:
    - Leave results["busiest_ip"] as None

========================================================
13) HELPER DATA (FOR DEBUGGING / VALIDATION)
--------------------------------------------------------
[ ] After processing ALL lines, your helpers should look like:

ip_request_counts:
{
    "10.0.0.8": 8,
    "10.0.0.21": 11,
    "10.0.0.33": 9,
    "10.0.0.44": 7,
    "10.0.0.55": 5,
    "10.0.0.89": 6,
    "10.0.0.144": 7,
    "10.0.0.200": 4,
    "10.0.0.77": 2
}

slow_path_tracker:
{
    "/api/orders": [
        1.205, 1.205, 1.205, 1.205, 1.205, 1.205,
        2.801, 2.801, 2.801
    ],
    "/api/upload": [
        1.700, 1.700
    ],
    "/reports/daily": [
        1.450, 1.450, 1.450, 1.450,
        2.220, 2.220, 2.220
    ],
    "/api/users": [
        1.980, 2.110
    ]
}

suspicious_ip_counts:
{
    "10.0.0.21": 11,
    "10.0.0.89": 6
}

========================================================
14) RETURN VALUE
--------------------------------------------------------
[ ] Return results dictionary

========================================================
Expected Result
--------------------------------------------------------
{
    "method_counts": {
        "GET": 50,
        "POST": 9
    },
    "busiest_ip": "10.0.0.21",
    "server_error_paths": {
        "/api/orders": 3,
        "/reports/daily": 3,
        "/api/users": 2
    },
    "avg_slow_paths": {
        "/api/orders": 1.737,
        "/reports/daily": 1.78
    },
    "suspicious_ips": [
        "10.0.0.21",
        "10.0.0.89"
    ]
}
"""