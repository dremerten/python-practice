import pprint

def analyze_access_log(PATH: str) -> dict:
    # Initialize the results dictionary
    results = {
        "status_counts": {},
        "path_error_counts": {},
        "top_error_path": None,
        "slow_requests_count": 0,
        "method_counts": {}
    }

    try:
        # Open the log file for reading
        with open(PATH, 'r') as f:
            for line in f:
                # Strip leading/trailing whitespace and skip empty lines
                line = line.strip()
                if not line:
                    continue
                
                # Split the line into parts
                parts = line.split()
                
                # Skip malformed lines (expect exactly 6 fields)
                if len(parts) != 6:
                    continue
                
                # Extract individual components
                _, _, method, path, status_str, latency_str = parts
                
                # Validate status and convert to integer
                if not status_str.isdigit():
                    continue
                status = int(status_str)

                # Parse latency (ensure it's in milliseconds)
                latency_num = latency_str[:-2]
                if not latency_num.isdigit():
                    continue
                latency_ms = int(latency_num)

                # Update status counts
                results["status_counts"][status] = results["status_counts"].get(status, 0) + 1
                
                # Update method counts
                results["method_counts"][method] = results["method_counts"].get(method, 0) + 1

                # Count slow requests (latency >= 250ms)
                if latency_ms >= 250:
                    results["slow_requests_count"] += 1

                # Track errors (status code between 400-599)
                if 400 <= status <= 599:
                    results["path_error_counts"][path] = results["path_error_counts"].get(path, 0) + 1

        # Calculate the most error-prone path (if any)
        if results["path_error_counts"]:
            # Find the path with the highest error count using max
            results["top_error_path"] = max(results["path_error_counts"], key=results["path_error_counts"].get)
        else:
            results["top_error_path"] = None

    except FileNotFoundError as e:
        # Handle file not found error
        raise FileNotFoundError(f"The log file can't be found or does not exist: {e}")
    except Exception as e:
        # Handle any other I/O errors
        raise Exception(f"An error occurred while processing the log file: {e}")

    return results

if __name__ == "__main__":
    PATH = "/home/andre/DevOps-Practice/python-practice/python-advanced/code_challenge_exercises/nginx_log_parsing/nginx_access.log"
    results = analyze_access_log(PATH)
    pprint.pprint(results, indent=4)