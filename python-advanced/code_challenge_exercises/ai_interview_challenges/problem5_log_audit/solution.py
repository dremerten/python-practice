"""
API RESPONSE AUDIT — MID-LEVEL CHECKLIST

GOAL:
Implement a function that parses an API log file and produces summary metrics.

========================================================
1) FUNCTION SETUP
--------------------------------------------------------
[ ] Define: audit_api_responses(file_path)
[ ] Initialize:
    - results dict with:
        status_counts
        slow_endpoints
        most_frequent_client_error
    - a separate dict to track client error counts

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open the file using a context manager
[ ] Handle the case where the file does not exist
[ ] Iterate line by line

========================================================
3) LINE NORMALIZATION
--------------------------------------------------------
[ ] Strip whitespace
[ ] Skip empty lines

========================================================
4) BASIC VALIDATION
--------------------------------------------------------
[ ] Split using "|"
[ ] Skip lines that do not have exactly 4 fields

========================================================
5) FIELD EXTRACTION
--------------------------------------------------------
[ ] Extract:
    timestamp
    endpoint
    status_code_text
    response_time_text

[ ] Ensure none of these are empty

========================================================
6) TYPE CONVERSION
--------------------------------------------------------
[ ] Convert status_code and response_time to integers
[ ] Skip the line if conversion fails

========================================================
7) STATUS CODE AGGREGATION
--------------------------------------------------------
[ ] Maintain a count of each status code

========================================================
8) SLOW REQUEST TRACKING
--------------------------------------------------------
[ ] Define "slow" as response_time >= 1000 ms
[ ] Track count of slow requests per endpoint

========================================================
9) CLIENT ERROR TRACKING
--------------------------------------------------------
[ ] Identify client errors (400–499)
[ ] Track occurrences per endpoint

========================================================
10) FINAL COMPUTATION
--------------------------------------------------------
[ ] Determine the endpoint with the highest client error count
[ ] If none exist, leave as None

========================================================
11) RETURN VALUE
--------------------------------------------------------
[ ] Return the results dictionary

========================================================
NOTES
--------------------------------------------------------
- Input may contain malformed lines — ignore them safely
- Do not let a single bad line break processing
- Favor simple, readable logic over clever shortcuts
"""

import pprint


def audit_api_responses(file_path: str) -> dict:
    results = {
        "status_counts": {},
        "slow_endpoints": {},
        "most_frequent_client_error": None
    }
    client_error_counts = {}

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 4:
                    continue

                timestamp = parts[0].strip()
                endpoint = parts[1].strip()
                status_code_text = parts[2].strip()
                response_time_text = parts[3].strip()

                if not timestamp or not endpoint or not status_code_text or not response_time_text:
                    continue

                try:
                    status_code = int(status_code_text)
                    response_time_ms = int(response_time_text)
                except (ValueError, TypeError):
                    continue

                if status_code not in results["status_counts"]:
                    results["status_counts"][status_code] = 0
                results["status_counts"][status_code] += 1

                if response_time_ms >= 1000:
                    if endpoint not in results["slow_endpoints"]:
                        results["slow_endpoints"][endpoint] = 0
                    results["slow_endpoints"][endpoint] += 1

                if 400 <= status_code <= 499:
                    if endpoint not in client_error_counts:
                        client_error_counts[endpoint] = 0
                    client_error_counts[endpoint] += 1

    except FileNotFoundError:
        print(f"Error: {file_path} does not exist")
        return results

    if client_error_counts:
        results["most_frequent_client_error"] = max(
            client_error_counts,
            key=client_error_counts.get
        )

    return results


if __name__ == "__main__":
    path = "nginx.log"
    result = audit_api_responses(path)
    pprint.pprint(result, indent=2)