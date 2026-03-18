"""
ACCESS LOG ANALYSIS — STEP-BY-STEP CHECKLIST (NO REGEX)

GOAL:
Read an access log file line-by-line and compute:
- HTTP status code counts (e.g., 200/404/500)
- Error counts per path (status 400–599)
- Most error-prone path (or None)
- Count of slow requests (latency >= 250ms)
- HTTP method counts (GET/POST/etc.)

LOG FORMAT (consistent, space-separated):
timestamp client_ip method path status latency_ms

Example:
2026-02-16T14:22:10Z 10.2.4.18 GET /api/v1/payments 200 18ms

========================================================
1) FUNCTION + RESULT STRUCTURE
--------------------------------------------------------
[ ] Define function: analyze_access_log(path: str) -> dict
[ ] Initialize results:
    {
      "status_counts": {},
      "path_error_counts": {},
      "top_error_path": None,
      "slow_requests_count": 0,
      "method_counts": {}
    }

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open file: with open(path, "r") as f
[ ] For each `line` in the file:
[ ] `line = line.strip()` (remove leading/trailing whitespace)
[ ] If the line is empty, `continue` (skip)

========================================================
3) SPLIT INTO FIELDS
--------------------------------------------------------
[ ] Split the line by whitespace: `parts = line.split()`
[ ] Expect exactly 6 fields:
    - `0 timestamp`
    - `1 ip`
    - `2 method`
    - `3 path`
    - `4 status`
    - `5 latency (e.g., "18ms")`
[ ] If `len(parts) != 6`, skip the line (malformed line)

========================================================
4) EXTRACT + BASIC VALIDATION
--------------------------------------------------------
[ ] Extract the parts of the line:
    - You can either unpack the values individually, e.g., `timestamp = parts[0]`, or use a more compact method to unpack them all into variables at once.
    
[ ] Convert `status_str` to an integer:
    - Ensure the string is a valid number before converting.
    - If it's not a valid number, skip the line.

[ ] Parse the `latency_str`:
    - Ensure it ends with "ms".
    - Remove the "ms" part and convert the remaining value to an integer.
    - If the number is invalid, skip the line.

[ ] Perform validation at each step:
    - Only process lines that pass all checks.

========================================================
5) UPDATE STATUS COUNTS
--------------------------------------------------------
[ ] Update the count for each HTTP `status` code:
    - Use `results["status_counts"][status] = results["status_counts"].get(status, 0) + 1` to increment the count for the status code.

========================================================
6) UPDATE METHOD COUNTS
--------------------------------------------------------
[ ] Track the HTTP `method` counts (GET/POST/etc.):
    - Use `results["method_counts"][method] = results["method_counts"].get(method, 0) + 1` to increment the count for each method.

========================================================
7) COUNT SLOW REQUESTS
--------------------------------------------------------
[ ] Count requests with latency greater than or equal to 250ms:
    - If `latency_ms >= 250`, increment `results["slow_requests_count"]`.

========================================================
8) TRACK ERRORS PER PATH
--------------------------------------------------------
[ ] Track errors by `path` for HTTP status codes between 400 and 599:
    - If `400 <= status <= 599`, increment the count for that `path` in `results["path_error_counts"]`.

========================================================
9) FIND TOP ERROR PATH
--------------------------------------------------------
[ ] If `results["path_error_counts"]` is empty:
    - Set `results["top_error_path"] = None`.
[ ] Else:
    - Use `max()` to find the path with the highest error count:
        - `results["top_error_path"] = max(results["path_error_counts"], key=results["path_error_counts"].get)`.

========================================================
10) RETURN RESULTS
--------------------------------------------------------
[ ] Return the `results` dictionary, which contains:
    - `results["method_counts"]`: A dictionary mapping HTTP methods (e.g., GET, POST) to their respective counts.
    - `results["path_error_counts"]`: A dictionary mapping paths to their respective error counts (status codes between 400–599).
    - `results["top_error_path"]`: The path with the highest error count, or `None` if no errors were tracked.
    - `results["slow_requests_count"]`: The total number of requests with latency >= 250ms.
    - `results["status_counts"]`: A dictionary mapping HTTP status codes (e.g., 200, 404) to their respective counts.

[ ] Example output format:
{
    'method_counts': {
        'DELETE': 395,
        'GET': 363,
        'POST': 353,
        'PUT': 389
    },
    'path_error_counts': {
        '/': 114,
        '/api/v1/orders': 116,
        '/api/v1/payments': 98,
        '/api/v1/products': 110,
        '/api/v1/users': 103,
        '/health': 96,
        '/login': 92,
        '/logout': 92,
        '/metrics': 104
    },
    'slow_requests_count': 870,
    'status_counts': {
        200: 100,
        201: 125,
        204: 109,
        301: 141,
        302: 100,
        400: 141,
        401: 106,
        403: 104,
        404: 116,
        429: 129,
        500: 102,
        502: 124,
        503: 103
    },
    'top_error_path': '/api/v1/orders'
}

[ ] Never crash on malformed lines: always skip them safely.

========================================================
EXTRA ERROR HANDLING
--------------------------------------------------------
[ ] Handle missing files gracefully:
    - If the log file can't be found, raise a `FileNotFoundError` with a descriptive message.
[ ] Handle other potential exceptions gracefully:
    - If an unexpected error occurs, raise a generic `Exception` with a descriptive message.

========================================================
MAIN BLOCK (for testing the function)
--------------------------------------------------------
[ ] Add a main block to run the code and print the results using `pprint`.
[ ] Example:
    if __name__ == "__main__":
        PATH = "path/to/log/file.log"
        results = analyze_access_log(PATH)
        pprint.pprint(results, indent=4)
"""
