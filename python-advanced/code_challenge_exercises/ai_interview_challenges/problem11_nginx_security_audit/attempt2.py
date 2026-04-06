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
                client_tokens = client_metadata.strip().split()
                if not client_tokens:
                    continue

                ip_address = client_tokens[0].strip()
                timestamp_start = client_metadata.find("[")
                timestamp_end = client_metadata.find("]")
                if (
                    timestamp_start == -1
                    or timestamp_end == -1
                    or timestamp_end <= timestamp_start + 1
                ):
                    continue

                timestamp = client_metadata[timestamp_start+1:timestamp_end]
                request_fields = request_line.split()
                if len(request_fields) != 3:
                    continue

                method, path = request_fields[0], request_fields[1]
                status_fields = status_section.split()
                if len(status_fields) < 2:
                    continue

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

                timestamp = timestamp.split()
                timestamp_main = timestamp[0]
                timestamp_parts = timestamp_main.split(":")
                if len(timestamp_main) < 3:
                    continue

                date, hour, minute, _ = timestamp_parts[0], timestamp_parts[1], timestamp_parts[2], timestamp_parts[3]
                date_tokens = date.split("/")
                if len(date_tokens) != 3:
                    continue

                day, month, year = date_tokens[0], date_tokens[1], date_tokens[2]
                if month not in month_map:
                    continue

                minute_key = f"{year}-{month_map[month]}-{day} {hour}:{minute}"
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
    
    # F)
    if path_404_counts:
        highest_404_count = max(path_404_counts.values())

        top_404_candidates = [
            current_path
            for current_path in path_404_counts
            if path_404_counts[current_path] == highest_404_count
        ]
    
    results["top_404_path"] = min(top_404_candidates)

    # G)
    results["suspicious_ips"] = {
    ip_address: count
    for ip_address, count in suspicious_ip_counts.items()
    if count >= suspicious_threshold
    }

    if minute_counts:
        highest_minute_count = max(minute_counts.values())
        busiest_minute_candidates = [
            minute
            for minute in minute_counts
            if minute_counts[minute] == highest_minute_count
        ]
        results["busiest_minute"] = min(busiest_minute_candidates)

    if successful_get_count > 0:
        average_bytes = successful_get_bytes_total / successful_get_count
        results["average_bytes_sent_by_successful_get"] = round(average_bytes, 2)
        
    return results
    
if __name__ == "__main__":
    result = analyze_nginx_log("nginx.log")
    pprint.pprint(result)