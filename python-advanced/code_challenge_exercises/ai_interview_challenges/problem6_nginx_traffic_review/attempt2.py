import json


def review_nginx_traffic(file_path: str) -> dict:
    results = {
        "method_counts": {},
        "busiest_ip": None,
        "server_error_paths": {},
        "avg_slow_paths": {},
        "suspicious_ips": []
    }

    ip_request_counts = {}
    slow_path_tracker = {}
    suspicious_ip_counts = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    continue

                timestamp = parts[0].strip()
                client_ip = parts[1].strip()
                method = parts[2].strip()
                path = parts[3].strip()
                status_code_str = parts[4].strip()
                bytes_sent_str = parts[5].strip()
                request_time_str = parts[6].strip()

                required_fields = (
                    timestamp, 
                    client_ip, 
                    method, 
                    path, 
                    status_code_str, 
                    bytes_sent_str, 
                    request_time_str
                    )

                if not all(required_fields):
                    continue
                
                try:
                    status_code = int(status_code_str)
                    bytes_sent = int(bytes_sent_str)
                    request_time = float(request_time_str)
                except ValueError:
                    continue
                
                results["method_counts"][method] = results["method_counts"].get(method, 0) + 1
                ip_request_counts[client_ip] = ip_request_counts.get(client_ip, 0) + 1

                if status_code in range(500, 600):
                    results["server_error_paths"][path] = results["server_error_paths"].get(path, 0) +1

                if request_time >= 1.0:
                    slow_path_tracker[path] = slow_path_tracker.get(path, [])
                    slow_path_tracker[path].append(request_time)
                
                if status_code in {401,403,404,429}:
                    suspicious_ip_counts[client_ip] = suspicious_ip_counts.get(client_ip, 0) + 1

    except FileNotFoundError:
        print(f"The file: {file_path} can't be found or does not exist")

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
    result = review_nginx_traffic("nginx.txt")
    print(json.dumps(result, indent=4))
