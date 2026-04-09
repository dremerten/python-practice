import json


def analyze_nginx_access_log(log_file_path: str) -> dict:
    results = {
    "line_count": 0,
    "unique_ip_count": 0,
    "method_counts": {},
    "status_counts": {},
    "most_requested_path": None,
    "top_ip_address": None,
    "error_request_count": 0,
    "user_agent_counts": {},
    "largest_response": {
        "bytes": None,
        "path": None,
        "ip_address": None
    },
    "average_response_bytes": None,
    "busiest_minute": None
}

    method_counts = {}
    status_counts = {}
    path_counts = {}
    ip_counts = {}
    user_agent_counts = {}
    error_request_count = 0
    total_response_bytes = 0
    line_count = 0
    minute_counts = {}

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    parts = line.split('"')
                    if len(parts) < 7:
                        continue

                    prefix = parts[0].strip()
                    request = parts[1].strip()
                    middle = parts[2].strip()
                    user_agent = parts[5].strip()
                    ip_address = prefix.split()[0]
                    timestamp = prefix.split()[3].strip("[")
                    method, path, protocol = request.split()[0], request.split()[1], request.split()[2]
                    status_code, response_bytes = middle.split()[0], middle.split()[1]
                    try:
                        status_code = int(status_code)
                        response_bytes = int(response_bytes)
                    except ValueError, TypeError:
                        continue

                except (IndexError, ValueError, TypeError):
                    continue

                line_count += 1
                method_counts[method] = method_counts.get(method, 0) + 1
                status_code_key = str(status_code)
                status_counts[status_code] = status_counts.get(status_code, 0) +1
                path_counts[path] = path_counts.get(path, 0) + 1
                ip_counts[ip_address] = ip_counts.get(ip_address, 0) + 1
                user_agent_counts[user_agent] = user_agent_counts.get(user_agent, 0) + 1
                if status_code >= 400:
                    error_request_count += 1
                
                total_response_bytes += response_bytes

                if (
                    results["largest_response"]["bytes"] is None 
                    or response_bytes > results["largest_response"]["bytes"]
                ):
                    results["largest_response"]["bytes"] = response_bytes
                    results["largest_response"]["path"] = path
                    results["largest_response"]["ip_address"] = ip_address
                
                minute_key = timestamp[:17]
                minute_counts[minute_key] = minute_counts.get(minute_key, 0) + 1

    except FileNotFoundError:
        return results

    results["line_count"] = line_count
    results["unique_ip_count"] = len(ip_counts)
    results["method_counts"] = method_counts
    results["status_counts"] = status_counts
    results["user_agent_counts"] = user_agent_counts
    results["error_request_count"] = error_request_count

    if path_counts:
        highest_path_count = max(path_counts.values())
        results["most_requested_path"] = min(
        path
        for path, count in path_counts.items()
        if count == highest_path_count
    )

    if ip_counts:
        highest_ip_count = max(ip_counts.values())
        results["top_ip_address"] = min(
        ip
        for ip, count in ip_counts.items()
        if count == highest_ip_count
    )

    if line_count > 0:
        average_response_bytes = total_response_bytes / line_count
        results["average_response_bytes"] = round(average_response_bytes, 2)

    if minute_counts:
        highest_count = max(minute_counts.values())
        results["busiest_minute"] = min([
            minute
            for minute in minute_counts
            if minute_counts[minute] == highest_count
        ])
    
    return results
    
if __name__ == "__main__":
    log_file_path = "nginx_access_1200.log"
    result = analyze_nginx_access_log(log_file_path)
    print(json.dumps(result, indent=4))