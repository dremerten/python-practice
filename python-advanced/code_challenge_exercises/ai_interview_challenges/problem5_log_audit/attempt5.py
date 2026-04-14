import json


def audit_api_responses(file_path: str) -> dict:
    results = {
        "status_counts": {},
        "slow_endpoints": {},
        "most_frequent_client_error": None
    }
    client_error_counts = {}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 4:
                    continue

                timestamp, endpoint, status_code_str, response_time_str = (
                    parts[0].strip(),
                    parts[1].strip(),
                    parts[2].strip(),
                    parts[3].strip() 
                )

                if not timestamp or not endpoint or not status_code_str or not response_time_str:
                    continue

                try:
                    status_code = int(status_code_str)
                    response_time = int(response_time_str)
                except ValueError:
                    continue

                results["status_counts"][status_code] = results["status_counts"].get(status_code, 0) + 1
                if response_time >= 1000:
                    results["slow_endpoints"][endpoint] = results["slow_endpoints"].get(endpoint, 0) + 1

                if 400 < status_code < 499:
                    client_error_counts[endpoint] = client_error_counts.get(endpoint, 0) + 1
            
            if client_error_counts:
                results["most_frequent_client_error"] = max(
                    client_error_counts,
                    key=client_error_counts.get
                )
            breakpoint()
            return results

    except FileNotFoundError:
        print(f"The file {file_path} can't be found of does not exist")

if __name__ == "__main__":
    file_path = "nginx.log"


result = audit_api_responses(file_path)
print(json.dumps(result, indent=4))