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
[ ] for line in f:
[ ] line = line.strip()
[ ] if empty -> continue

========================================================
3) SPLIT INTO FIELDS
--------------------------------------------------------
[ ] Split by whitespace: parts = line.split()
[ ] Expect exactly 6 fields:
    0 timestamp
    1 ip
    2 method
    3 path
    4 status
    5 latency (like "18ms")
[ ] If len(parts) != 6 -> skip (malformed line)

========================================================
4) EXTRACT + BASIC VALIDATION
--------------------------------------------------------
[ ] timestamp = parts[0]
[ ] ip = parts[1]
[ ] method = parts[2]
[ ] path = parts[3]
[ ] status_str = parts[4]
[ ] latency_str = parts[5]

[ ] Convert status_str -> int safely:
    - if not status_str.isdigit(): skip
    - status = int(status_str)

[ ] Parse latency:
    - latency_str must end with "ms"
    - latency_num = latency_str[:-2]
    - if not latency_num.isdigit(): skip
    - latency_ms = int(latency_num)

========================================================
5) UPDATE STATUS COUNTS
--------------------------------------------------------
[ ] status_counts[status] = status_counts.get(status, 0) + 1

========================================================
6) UPDATE METHOD COUNTS
--------------------------------------------------------
[ ] method_counts[method] = method_counts.get(method, 0) + 1

========================================================
7) COUNT SLOW REQUESTS
--------------------------------------------------------
[ ] If latency_ms >= 250:
    slow_requests_count += 1

========================================================
8) TRACK ERRORS PER PATH
--------------------------------------------------------
[ ] If status is between 400 and 599 (inclusive):
    path_error_counts[path] = path_error_counts.get(path, 0) + 1

========================================================
9) FIND TOP ERROR PATH
--------------------------------------------------------
[ ] If path_error_counts is empty:
    top_error_path = None
[ ] Else:
    - highest = 0
    - iterate path_error_counts.items()
    - if count > highest:
        highest = count
        top_error_path = path

========================================================
10) RETURN RESULTS
--------------------------------------------------------
[ ] return results
[ ] Never crash on malformed lines: always skip safely
"""


import pprint

def analyze_access_log(PATH: str) -> dict:
    # Initialize the results dictionary
    results = {
        "status_counts": {},
        "path_error_counts": {},
        "top_error_path": None,
        "slow_requests_count": 0,
        "method_counts": {}
    }

    try:
        # Open the log file for reading
        with open(PATH, 'r') as f:
            for line in f:
                # Strip leading/trailing whitespace and skip empty lines
                line = line.strip()
                if not line:
                    continue
                
                # Split the line into parts
                parts = line.split()
                
                # Skip malformed lines (expect exactly 6 fields)
                if len(parts) != 6:
                    continue
                
                # Extract individual components
                _, _, method, path, status_str, latency_str = parts
                
                # Validate status and convert to integer
                if not status_str.isdigit():
                    continue
                status = int(status_str)

                # Parse latency (ensure it's in milliseconds)
                latency_num = latency_str[:-2]
                if not latency_num.isdigit():
                    continue
                latency_ms = int(latency_num)

                # Update status counts
                results["status_counts"][status] = results["status_counts"].get(status, 0) + 1
                
                # Update method counts
                results["method_counts"][method] = results["method_counts"].get(method, 0) + 1

                # Count slow requests (latency >= 250ms)
                if latency_ms >= 250:
                    results["slow_requests_count"] += 1

                # Track errors (status code between 400-599)
                if 400 <= status <= 599:
                    results["path_error_counts"][path] = results["path_error_counts"].get(path, 0) + 1

        # Calculate the most error-prone path (if any)
        if results["path_error_counts"]:
            # Find the path with the highest error count using max
            results["top_error_path"] = max(results["path_error_counts"], key=results["path_error_counts"].get)
        else:
            results["top_error_path"] = None

    except FileNotFoundError as e:
        # Handle file not found error
        raise FileNotFoundError(f"The log file can't be found or does not exist: {e}")
    except Exception as e:
        # Handle any other I/O errors
        raise Exception(f"An error occurred while processing the log file: {e}")

    return results

if __name__ == "__main__":
    PATH = "/home/andre/DevOps-Practice/python-practice/python-advanced/code_challenge_exercises/nginx_log_parsing/nginx_access.log"
    results = analyze_access_log(PATH)
    pprint.pprint(results, indent=4)