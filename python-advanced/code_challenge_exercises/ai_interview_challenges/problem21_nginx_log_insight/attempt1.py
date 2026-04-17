import json
from typing import Any



def analyze_nginx_logs(log_file: str) -> dict[str, Any]:
    results: dict[str, Any] = {
        "total_requests": 0,
        "status_counts": {},
        "top_ip": None,
        "error_ips": [],
        "heavy_traffic_ips": {}
    }

    ip_tracker = {}
    status_tracker = {}
    endpoint_tracker = {}
    error_ip_tracker = set()
    
    try:
        with open("nginx_access.log", 'r') as file:
            for line in file:
                line = line.strip()
                line_split = line.split()
                parts = [x for x in line_split if x not in ("-", '', None)]
                if len(parts) < 9:
                    continue

                ip_address = parts[0]
                request_method = parts[3].strip('"')
                endpoint = parts[4].strip()
                status_code = parts[6].strip()
                response_size =parts[7].strip()
                if not any({ip_address, request_method, endpoint, status_code, response_size}):
                    print(f"Missing required field....skipping")
                    continue
                
                try:
                    response_size = int(response_size)
                except ValueError:
                    print(f"ValueError occured skipping....")

                results["total_requests"] += 1
                ip_tracker[ip_address] = ip_tracker.get(ip_address, 0) + 1
                status_tracker[status_code] = status_tracker.get(status_code, 0) + 1
                endpoint_tracker[endpoint] = endpoint_tracker.get(endpoint, 0) + 1

                if status_code.startswith("4" or "5"):
                    error_ip_tracker.add(ip_address)

    except FileNotFoundError:
        print(f"The file {log_file} can't be found or does not exist")
    except ValueError as err:
        raise ValueError(f"Malformed log data during processing: {err}") from err

    results["status_counts"] = status_tracker

    if ip_tracker:
        results["top_ip"] = max(ip_tracker, key=ip_tracker.get)
    
    results["error_ips"] = sorted(error_ip_tracker)

    results["heavy_traffic_ips"] = {
        ip: count for ip, count in ip_tracker.items() if count > 20
    }

    return results


if __name__ == "__main__":
    output = analyze_nginx_logs("nginx_access.log")
    print(json.dumps(output, indent=4))
