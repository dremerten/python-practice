

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
                
                breakpoint()
        

        return results
    except FileNotFoundError:
        return results

if __name__ == "__main__":
    result = analyze_nginx_log("nginx.log")
    print(result)