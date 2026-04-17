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

    ip_counts = {}
    status_counts = {}
    error_tracker = set()

    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.split()
                ip = parts[0]
                status = parts[-3]

                results["total_requests"] += 1

                status_counts[status] = status_counts.get(status, 0) + 1
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

                if status.startswith("4") or status.startswith("5"):
                    error_tracker.add(ip)

    except FileNotFoundError:
        return results

    results["status_counts"] = status_counts

    if ip_counts:
        results["top_ip"] = max(ip_counts, key=ip_counts.get)

    results["error_ips"] = sorted(error_tracker)

    results["heavy_traffic_ips"] = {
        ip: count for ip, count in ip_counts.items() if count > 20
    }

    return results


if __name__ == "__main__":
    output = analyze_nginx_logs("nginx_access.log")
    print(json.dumps(output, indent=4))
