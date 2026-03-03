import pprint

PATH="/home/andre/DevOps-Practice/python-practice/nginx_log_parsing/nginx_access.log"

def analyze_access_log(path: str) -> dict:
    results = {
        "http_status_counts": {},
        "path_error_counts": {},
        "top_error_path": None,
        "slow_requests_count": 0,
        "http_method_counts": {}
    }

    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) != 6:
                    continue

                http_method = parts[2]
                http_path = parts[3]

                status_code_str = parts[4]
                if not status_code_str.isdigit():
                    continue
                status_code = int(status_code_str)

                latency_str = parts[5]
                if not latency_str.endswith("ms"):
                    continue
                latency_num = latency_str[:-2]

                if not latency_num.isdigit():
                    continue
                latency_ms = int(latency_num)

                results["http_status_counts"].setdefault(status_code, 0)
                results["http_status_counts"][status_code] += 1

                results["http_method_counts"].setdefault(http_method, 0)
                results["http_method_counts"][http_method] += 1

                if latency_ms >= 250:
                    results["slow_requests_count"] += 1

                if 400 <= status_code <= 599:
                    results["path_error_counts"].setdefault(http_path, 0)
                    results["path_error_counts"][http_path] += 1

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The log file at: {path} can not be found or does not exist"
        ) from e

    # Compute top_error_path once
    highest = 0
    for p, count in results["path_error_counts"].items():
        if count > highest:
            highest = count
            results["top_error_path"] = p

    return results

if __name__ == "__main__":
    results = analyze_access_log(PATH)
    pprint.pprint(results, indent=4)
