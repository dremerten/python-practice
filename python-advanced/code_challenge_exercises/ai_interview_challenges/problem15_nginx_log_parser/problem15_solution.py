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
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    parts = line.split('"')
                    prefix = parts[0]
                    request = parts[1]
                    middle = parts[2]
                    user_agent = parts[5]

                    ip_address = prefix.split()[0]
                    timestamp = prefix.split("[", 1)[1].split("]", 1)[0]

                    method, path, protocol = request.split()

                    middle_parts = middle.strip().split()
                    status_code = int(middle_parts[0])
                    response_bytes = int(middle_parts[1])

                except (IndexError, ValueError, TypeError):
                    continue

                line_count += 1

                if method not in method_counts:
                    method_counts[method] = 0
                method_counts[method] += 1

                status_code_key = str(status_code)
                if status_code_key not in status_counts:
                    status_counts[status_code_key] = 0
                status_counts[status_code_key] += 1

                if path not in path_counts:
                    path_counts[path] = 0
                path_counts[path] += 1

                if ip_address not in ip_counts:
                    ip_counts[ip_address] = 0
                ip_counts[ip_address] += 1

                if user_agent not in user_agent_counts:
                    user_agent_counts[user_agent] = 0
                user_agent_counts[user_agent] += 1

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
                if minute_key not in minute_counts:
                    minute_counts[minute_key] = 0
                minute_counts[minute_key] += 1

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
        most_requested_path_candidates = []

        for path in path_counts:
            if path_counts[path] == highest_path_count:
                most_requested_path_candidates.append(path)

        results["most_requested_path"] = min(most_requested_path_candidates)

    if ip_counts:
        highest_ip_count = max(ip_counts.values())
        top_ip_candidates = []

        for ip_address in ip_counts:
            if ip_counts[ip_address] == highest_ip_count:
                top_ip_candidates.append(ip_address)

        results["top_ip_address"] = min(top_ip_candidates)

    if line_count > 0:
        average_response_bytes = total_response_bytes / line_count
        results["average_response_bytes"] = round(average_response_bytes, 2)

    if minute_counts:
        highest_minute_count = max(minute_counts.values())
        busiest_minute_candidates = []

        for minute in minute_counts:
            if minute_counts[minute] == highest_minute_count:
                busiest_minute_candidates.append(minute)

        results["busiest_minute"] = min(busiest_minute_candidates)

    return results

if __name__ == "__main__":
    log_file_path = "nginx_access.log"
    result = analyze_nginx_access_log(log_file_path)
    print(json.dumps(result, indent=4))