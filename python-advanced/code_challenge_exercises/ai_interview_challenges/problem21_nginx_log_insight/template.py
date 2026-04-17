"""

OBJECTIVE
You are given an NGINX access log file. Each line represents a request.

Your task is to analyze the log and compute:
- Total number of requests
- Count of each HTTP status code
- The IP address with the highest number of requests
- A sorted list of IPs that generated at least one error (status 4xx or 5xx)
- A dictionary of IPs that made more than 20 requests

You should handle malformed lines gracefully and skip bad data.

EXPECTED OUTPUT STRUCTURE
{
    "total_requests": int,
    "status_counts": {
        "200": int,
        "404": int,
        ...
    },
    "top_ip": str | None,
    "error_ips": [str, ...],
    "heavy_traffic_ips": {
        "ip_address": int
    }
}

# 1. Import modules
# 2. Define function with type hints
# 3. Initialize results dict
# 4. Initialize helper structures (ip_tracker, status_tracker, endpoint_tracker, error_ip_tracker)

# 5. Open log file in try/except block
    # 6. Catch FileNotFoundError with descriptive message
    # 7. Catch ValueError for malformed log data during processing

    # 8. Loop through each line in the log file
        # 9. Strip whitespace from the line
        # 10. Skip line if it is empty after stripping
        # 11. Split the line into parts
        # 12. Extract needed values (ip_address, request_method, endpoint, status_code, response_size)
        # 13. Skip line if required pieces are missing or malformed
        # 14. Convert response_size to int — skip line on ValueError
        # 15. Increment total request count
        # 16. Increment ip_tracker[ip_address]
        # 17. Increment status_tracker[status_code]
        # 18. Increment endpoint_tracker[endpoint]
        # 19. If status_code starts with "4" or "5", add ip_address to error_ip_tracker set

# 20. Post-loop: compute total_requests
# 21. Post-loop: store status_counts from status_tracker
# 22. Post-loop: only compute top_ip if ip_tracker is non-empty
# 23. Post-loop: find top_ip — max(ip_tracker, key=ip_tracker.get)
# 24. Post-loop: convert error_ip_tracker set to a sorted list and store in results["error_ips"]
# 25. Post-loop: build heavy_traffic_ips dict from ip_tracker for IPs with more than 20 requests
# 26. Return results

EXPECTED OUTPUT
{
    "total_requests": 260,
    "status_counts": {
        "404": 51,
        "200": 126,
        "500": 38,
        "403": 45
    },
    "top_ip": "192.168.1.14",
    "error_ips": [
        "192.168.1.1",
        "192.168.1.10",
        "192.168.1.11",
        "192.168.1.12",
        "192.168.1.13",
        "192.168.1.14",
        "192.168.1.15",
        "192.168.1.16",
        "192.168.1.17",
        "192.168.1.18",
        "192.168.1.19",
        "192.168.1.2",
        "192.168.1.3",
        "192.168.1.4",
        "192.168.1.5",
        "192.168.1.6",
        "192.168.1.7",
        "192.168.1.8",
        "192.168.1.9"
    ],
    "heavy_traffic_ips": {
        "192.168.1.14": 21
    }
}
"""