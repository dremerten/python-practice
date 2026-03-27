import json


def review_nginx_traffic(file_path: str) -> dict:
    results = {
        "method_counts": {},
        "busiest_ip": None,
        "server_error_paths": {},
        "avg_slow_paths": {},
        "suspicious_ips": []
    }
    # helpers
    ip_request_counts = {}
    slow_path_tracker = {}
    suspicious_ip_counts = {}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                line = line.split("|")
                if len(line) != 7:
                    continue
                
                # Clean and unpack the first 7 fields
                required_fields = (timestamp, client_ip, method, path, 
                status_code_str, bytes_sent_str, request_time_str) = [item.strip() for item in line[:7]]
                if not all(required_fields):
                    continue

                try:
                    status_code = int(status_code_str)
                    bytes_sent = int(bytes_sent_str)
                    request_time = float(request_time_str)

                except ValueError:
                    continue

                # Use dict.get(key, default) to avoid checking if the key exists.
                # If the key is present, it returns its value; otherwise, it returns the default.
                # This is useful for counters and simple accumulations without needing an if statement. 
                results["method_counts"][method] = results["method_counts"].get(method, 0) + 1
                ip_request_counts[client_ip] = ip_request_counts.get(client_ip, 0) + 1

                if status_code in range(500, 600):
                    results["server_error_paths"][path] = results["server_error_paths"].get(path, 0) + 1
                
                if request_time >= 1.0:
                    if path not in slow_path_tracker:
                        slow_path_tracker[path] = []
                    slow_path_tracker[path].append(request_time)

                if status_code in (401, 403, 404, 429):
                    suspicious_ip_counts[client_ip] = suspicious_ip_counts.get(client_ip, 0) + 1
    
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file at {file_path} does not exist or can not be found!"
            )
    
    if ip_request_counts:
        results["busiest_ip"] = max(
            ip_request_counts, 
            key=ip_request_counts.get
        )

    for path, times in slow_path_tracker.items():
        if len(times) >= 3:
            average_request_time = sum(times) / len(times)
            results["avg_slow_paths"][path] = round(average_request_time, 3)

    for ip, count in suspicious_ip_counts.items():
        if count >= 4:
            results["suspicious_ips"].append(ip)
    results["suspicious_ips"].sort()
    
    return results


if __name__ == "__main__":
    result = review_nginx_traffic(file_path="nginx.txt")
    print(json.dumps(result, indent=4))