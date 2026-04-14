"""
NGINX TRAFFIC REVIEW — MID-LEVEL CHALLENGE

GOAL:
Parse an NGINX access log and return infrastructure-focused summary metrics.

Log format (pipe-delimited, 7 fields):
    timestamp | client_ip | method | path | status_code | bytes_sent | request_time

========================================================
FUNCTION SIGNATURE
--------------------------------------------------------
review_nginx_traffic(file_path: str) -> dict

Return shape:
    {
        method_counts:      dict[str, int]
        busiest_ip:         str | None
        server_error_paths: dict[str, int]
        avg_slow_paths:     dict[str, float]
        suspicious_ips:     list[str]
    }

========================================================
TRACKING STATE
--------------------------------------------------------
Initialize your results dict with the return shape above.

Also initialize three helper dicts outside the loop:

    ip_request_counts   dict[str, int]   — total requests per IP
    slow_path_tracker   dict[str, list]  — raw request times per path
    suspicious_ip_counts dict[str, int]  — auth/access error count per IP

Some result keys (method_counts, server_error_paths) can
be written directly during the loop. The three helpers
exist because their final values can't be determined until
all lines are processed.

    Hint: dict.get(key, default) is your friend for
    counters — it lets you increment without checking
    if the key exists yet.

========================================================
FILE PARSING
--------------------------------------------------------
Open the file with a context manager inside a try/except.
Raise a FileNotFoundError with a descriptive message if
the file doesn't exist.

For each line:
    - Strip whitespace; skip if empty
    - Split on "|"; skip if the result isn't exactly 7 fields
    - Strip each field; skip the line if any field is empty
    - Convert status_code -> int, bytes_sent -> int,
      request_time -> float inside a nested try/except;
      skip the line on ValueError

========================================================
PER-LINE LOGIC
--------------------------------------------------------
With all 7 fields validated and typed, update your state:

    method_counts        — increment count for this method
    ip_request_counts    — increment count for this IP

    status 5xx           — increment count for this path in server_error_paths
                           (use range(500, 600) for the check)

    request_time >= 1.0  — collect raw times per path in slow_path_tracker
                           for later averaging. Each key is a path, each
                           value is a list of floats. If the path isn't a
                           key yet, initialize it to an empty list first,
                           then append the request_time.

                           Example shape after a few lines:
                           {
                               "/api/orders": [1.205, 2.801, 1.205],
                               "/api/upload": [1.700]
                           }

    status in            — increment count for this IP
    {401,403,404,429}      in suspicious_ip_counts

========================================================
POST-LOOP COMPUTATION
--------------------------------------------------------
After the file closes, use your three helpers to derive
the remaining output fields:

    busiest_ip      — use max() with a key argument on ip_request_counts;
                      only assign if the dict is non-empty

avg_slow_paths  — iterate slow_path_tracker using .items() so you
                      have access to both the path (key) and its list
                      of collected times (value).

                      For each path, check if the list has 3 or more
                      entries — len(times) >= 3. Skip paths that don't
                      meet that threshold.

                      For qualifying paths, compute the average:
                          sum(times) / len(times)
                      Round the result to 3 decimals and store it in
                      results["avg_slow_paths"] under the same path key.

                      Example: "/api/orders" collected [1.205, 2.801, 1.205]
                          average = (1.205 + 2.801 + 1.205) / 3 = 1.737
                          results["avg_slow_paths"]["/api/orders"] = 1.737

                      "/api/upload" only collected [1.700, 1.700] — 
                      only 2 entries, so it gets skipped entirely.

   suspicious_ips  — iterate suspicious_ip_counts using .items() so you
                      have access to both the IP (key) and its error
                      count (value).

                      For each IP, check if the count is 4 or more —
                      count >= 4. Skip IPs that don't meet that threshold.

                      For qualifying IPs, append the IP string to
                      results["suspicious_ips"].

                      After the loop, call .sort() on results["suspicious_ips"]
                      to order the final list alphabetically.

                      Example: suspicious_ip_counts looks like:
                          {"10.0.0.21": 11, "10.0.0.89": 6, "10.0.0.8": 2}

                          10.0.0.21 → 11 hits, qualifies → append
                          10.0.0.89 → 6 hits,  qualifies → append
                          10.0.0.8  → 2 hits,  skipped

                      results["suspicious_ips"] after sort:
                          ["10.0.0.21", "10.0.0.89"]
========================================================
EXPECTED OUTPUT
--------------------------------------------------------
{
    "method_counts":      {"GET": 50, "POST": 9},
    "busiest_ip":         "10.0.0.21",
    "server_error_paths": {"/api/orders": 3, "/reports/daily": 3, "/api/users": 2},
    "avg_slow_paths":     {"/api/orders": 1.737, "/reports/daily": 1.78},
    "suspicious_ips":     ["10.0.0.21", "10.0.0.89"]
}
"""