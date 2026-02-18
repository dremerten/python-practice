"""
PYTHON CHALLENGE — NGINX ACCESS LOG ANALYSIS

You are given an Nginx-style access log file where each line follows this format:

    <timestamp> <client_ip> <http_method> <path> <status_code> <latency_ms>

Example:
    2024-02-15T12:00:01 192.168.1.10 GET /api/users 200 45ms
    2024-02-15T12:00:02 192.168.1.11 POST /api/login 401 120ms
    2024-02-15T12:00:03 192.168.1.12 GET /api/orders 500 320ms

Write a function:

    def analyze_access_log(path: str) -> dict:

The function must read the file line by line, ignore malformed lines, and return
a dictionary with the following structure:

    {
        "http_status_counts": {},   # status_code -> count
        "http_method_counts": {},   # HTTP method -> count
        "path_error_counts": {},    # path -> count (4xx/5xx only)
        "top_error_path": None,     # path with highest error count or None
        "slow_requests_count": 0    # number of requests with latency >= 250ms
    }

Constraints:
- Do not use regular expressions
- Use only the Python standard library
- Do not load the entire file into memory
- Handle missing or invalid data safely
- Code must be readable and deterministic
"""

import pprint

def analyze_access_log(path: str) -> dict:
    results = {
        "http_status_counts": {},   # status_code -> count
        "http_method_counts": {},   # HTTP method -> count
        "path_error_counts": {},    # path -> count (4xx/5xx only)
        "top_error_path": None,     # path with highest error count or None
        "slow_requests_count": 0    # number of requests with latency >= 250ms
    }
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 6:
                    continue
                
                # unpack all tokens of part. Skip what is not needed
                _, _, http_method, path, status_code, latency_ms = parts
                if not status_code.isdigit():
                    continue
                status_code = int(status_code)
                if not latency_ms.endswith("ms"):
                    continue
                latency_val = latency_ms[:-2]
                if not latency_val.isdigit():
                    continue
                latency_ms = int(latency_val)

                results["http_status_counts"][status_code] = results["http_status_counts"].get(status_code, 0) + 1
                results["http_method_counts"][http_method] = results["http_method_counts"].get(http_method, 0) +1

                if 400 <= status_code <= 599:
                    results["path_error_counts"][path] = results["path_error_counts"].get(path, 0) +1

                if latency_ms >= 250:
                    results["slow_requests_count"] +=1

        highest_count = 0
        for path, count in results["path_error_counts"].items():
            if results["path_error_counts"]:
                results["top_error_path"] = max(results["path_error_counts"], key=results["path_error_counts"].get)

        return results

    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file at: {path} can't be found or does not exist") from e
                    

if __name__ == "__main__":
    PATH="/home/andre/DevOps-Practice/python-practice/nginx_log_parsing/nginx_access.log"
    result = analyze_access_log(PATH)
    pprint.pprint(result, indent=4)

'''
highest = 0
for path, count in results["path_error_counts"].items():
    if count > highest:
        highest = count
        results["top_error_path"] = path
'''