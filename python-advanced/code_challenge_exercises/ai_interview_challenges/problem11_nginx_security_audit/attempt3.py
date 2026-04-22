import json



def analyze_nginx_log(file_path: str, suspicious_threshold: int = 5) -> dict:
    results = {
    "method_counts": {},
    "status_class_counts": {},
    "top_404_path": None,
    "suspicious_ips": {},
    "busiest_minute": None,
    "average_bytes_sent_by_successful_get": None,
    }

    # helpers
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
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split('"')
                if len(parts) < 6:
                    continue

                client_metadata, request_line, status_section = (
                    parts[0].strip(),
                    parts[1].strip(),
                    parts[2].strip()
                )

                client_tokens = client_metadata.split(" - - ")
                if not client_tokens:
                    continue
                else:
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

                request_fields = request_line.split()
                if len(request_fields) < 2:
                    continue

                method, path, _ = (
                    request_fields[0], 
                    request_fields[1], 
                    request_fields[2]
                )

                status_fields = status_section.split()
                try:
                    status_code = int(status_fields[0])
                    bytes_sent = int(status_fields[1])
                except ValueError:
                    continue

                question_mark_index = path.find("?")
                if question_mark_index != -1:
                    normalized_path = path[:question_mark_index]
                else:
                    normalized_path = path

                timestamp_main = timestamp.split()
                timestamp_parts = timestamp_main[0].split(":")
                if len(timestamp_parts) < 3:
                    continue

                date, hour, minute = (
                    timestamp_parts[0].strip(),
                    timestamp_parts[1].strip(),
                    timestamp_parts[2].strip()
                )
                
                date_tokens = date.split("/")
                if len(date_tokens) != 3:
                    continue

                day, month, year = (
                    date_tokens[0].strip(),
                    date_tokens[1].strip(),
                    date_tokens[2].strip()
                )

                if month.title() not in month_map:
                    continue

                minute_key = f"{year}-{month_map.get(month)}-{day} {hour}:{minute}"
                if not all((ip_address, timestamp, method, path, minute_key)):
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
        top_404_candidates = [current_path for current_path in path_404_counts if path_404_counts[current_path] == highest_404_count]

        results["top_404_path"] = min(top_404_candidates)
    
    for ip, count in suspicious_ip_counts.items():
        if count >= suspicious_threshold:
            results["suspicious_ips"][ip] = results["suspicious_ips"].get(ip, count)

    if minute_counts:
        highest_minute_count = max(minute_counts.values())
        results["busiest_minute"] = min([k for k, v in minute_counts.items() if v == highest_minute_count])
    
    if successful_get_count > 0:
        average_bytes = successful_get_bytes_total / successful_get_count
        results["average_bytes_sent_by_successful_get"] = round(average_bytes, 2)
    
    return results

result = analyze_nginx_log("nginx.log")
print(json.dumps(result, indent=4))