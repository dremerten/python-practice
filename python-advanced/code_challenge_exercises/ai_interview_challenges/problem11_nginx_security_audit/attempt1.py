import pprint


def analyze_nginx_log(file_path: str, suspicious_threshold: int = 5) -> dict:
    results = {
    "method_counts": {},
    "status_class_counts": {},
    "top_404_path": None,
    "suspicious_ips": {},
    "busiest_minute": None,
    "average_bytes_sent_by_successful_get": None,
    }

    path_404_counts = {}
    suspicious_ip_counts = {}
    minute_counts = {}
    successful_get_bytes_total = 0
    successful_get_count = 0

    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    suspicious_targets = (
        "/admin",
        "/wp-admin",
        "/wp-login.php",
        "/.env",
        "/phpmyadmin",
    )

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('"')
                if len(parts) < 6:
                    continue
                
                client_metadata = parts[0].strip()
                request_line = parts[1].strip()
                status_section = parts[2].strip()

                client_tokens = client_metadata.split()
                if not client_tokens:
                    continue
                ip_address = client_tokens[0]

                timestamp_start = client_metadata.find("[")
                timestamp_end = client_metadata.find("]")
                if (
                    timestamp_start == -1
                    or timestamp_end == -1
                    or timestamp_end <= timestamp_start + 1
                ):
                    continue
                timestamp = client_metadata[timestamp_start + 1:timestamp_end]
                request_tokens = request_line.split()
                if len(request_tokens) != 3:
                    continue

                method = request_tokens[0]
                path = request_tokens[1]
                status_tokens = status_section.split()
                if len(status_tokens) < 2:
                    continue

                try:
                    status_code = int(status_tokens[0])
                    bytes_sent = int(status_tokens[1])
                except ValueError:
                    continue

                question_mark_index = path.find("?")
                if question_mark_index != -1:
                    normalized_path = path[:question_mark_index]
                else:
                    normalized_path = path

                timestamp_main = timestamp.split()[0]
                timestamp_parts = timestamp_main.split(":")
                if len(timestamp_parts) < 3:
                    continue

                date_part = timestamp_parts[0]
                hour = timestamp_parts[1]
                minute = timestamp_parts[2]
                
                date_tokens = date_part.split("/")
                if len(date_tokens) != 3:
                    continue

                day = date_tokens[0]
                month = date_tokens[1]
                year = date_tokens[2]
                if month not in month_map:
                    continue

                minute_key = year + "-" + month_map[month] + "-" + day + " " + hour + ":" + minute
                if not ip_address or not timestamp or not method or not path or not minute_key:
                    continue

                results["method_counts"][method] = results["method_counts"].get(method, 0) + 1

                if 200 <= status_code <= 299:
                    status_class = "2xx"
                elif 300 <= status_code <= 399:
                    status_class = "3xx"
                elif 400 <= status_code <= 499:
                    status_class = "4xx"
                elif 500 <= status_code <= 599:
                    status_class = "5xx"
                else:
                    status_class = None

                if status_class is not None:
                    results["status_class_counts"][status_class] = results["status_class_counts"].get(status_class, 0) + 1
                
                minute_counts[minute_key] = minute_counts.get(minute_key, 0) + 1

                if status_code == 404:
                    path_404_counts[normalized_path] = path_404_counts.get(normalized_path, 0) + 1

                is_suspicious = False
                for target in suspicious_targets:
                    if normalized_path == target or normalized_path.startswith(target + "/"):
                        is_suspicious = True
                        break
                
                if is_suspicious:
                    suspicious_ip_counts[ip_address] = suspicious_ip_counts.get(ip_address, 0) + 1
                
                if method == "GET" and status_code == 200:
                    successful_get_bytes_total += bytes_sent
                    successful_get_count += 1

    except FileNotFoundError:
        return results

    if path_404_counts:
        highest_404_count = max(path_404_counts.values())

    top_404_candidates = []
    for current_path in path_404_counts:
        if path_404_counts[current_path] == highest_404_count:
            top_404_candidates.append(current_path)
        results["top_404_path"] = min(top_404_candidates)
    
    for ip_address in suspicious_ip_counts:
        if suspicious_ip_counts[ip_address] >= suspicious_threshold:
            results["suspicious_ips"][ip_address] = suspicious_ip_counts[ip_address]
        
    if minute_counts:
        highest_minute_count = max(minute_counts.values())
        busiest_minute_candidates = []
        for current_minute in minute_counts:
            if minute_counts[current_minute] == highest_minute_count:
                busiest_minute_candidates.append(current_minute)
        results["busiest_minute"] = min(busiest_minute_candidates)

    if successful_get_count > 0:
        average_bytes = successful_get_bytes_total / successful_get_count
        results["average_bytes_sent_by_successful_get"] = average_bytes = round(average_bytes, 2)

    return results


if __name__ == "__main__":
    result = analyze_nginx_log("nginx.log")
    pprint.pprint(result)