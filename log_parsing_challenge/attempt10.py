"""
DEVOPS / INFRASTRUCTURE PYTHON INTERVIEW CHALLENGE
System Log Analyzer (No Regex — Built-in Python Only)

GOAL:
Implement analyze_logs(path: str) -> dict

The function should:
1. Count WARNING and ERROR logs per service
2. Count frequency of each ERROR message
3. Return the most common ERROR message (or None if no errors)

Assume consistent formatting.

Log Format Example:
##################################################################
<TimeStamp> <Service> <Log Level> - <Error Message>
##################################################################

[2026-03-01 14:22:10] [payments] [ERROR] - DB connection timed out
[2026-03-01 14:22:11] [auth] [WARNING] - Token refresh delay
[2026-03-01 14:22:12] [payments] [ERROR] - DB connection timed out

Expected Return Structure:
{
    "service_counts": {
        "payments": {"ERROR": 2, "WARNING": 0},
        "db": {"ERROR": 0, "WARNING": 1}
    },
    "error_messages": {
        "DB connection timed out": 2
    },
    "most_common_error": "DB connection timed out"
}

Constraints:
- No regex
- Use basic string methods: split(), strip(), get()
- Do not crash on malformed input (skip safely)
"""

import pprint

PATH = "/home/andre/DevOps-Practice/python-practice/log_parsing_challenge/system.log"

def analyze_logs(path: str) -> dict:
    results = {
        "service_counts": {},
        "error_messages": {},
        "most_common_error": None
    }

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" - ")
            if len(parts) != 2:
                continue

            header, err_message = parts
            header = header.split()
            if len(header) < 4:
                continue

            service = header[2].strip("[]")
            log_level = header[3].strip("[]")

            if log_level not in ("INFO", "WARNING", "DEBUG", "ERROR", "TRACE"):
                continue

            results["service_counts"].setdefault(service, {"ERROR": 0, "WARNING": 0})

            if log_level in ("ERROR", "WARNING"):
                results["service_counts"][service][log_level] += 1

            if log_level == "ERROR":
                results["error_messages"][err_message] = results["error_messages"].get(err_message, 0) + 1

    #if results["error_messages"]:
        #results["most_common_error"] = max(results["error_messages"],key=results["error_messages"].get)

    highest_count = 0
    for err, count in results["error_messages"].items():
        if count > highest_count:
            results["most_common_error"] = err
            highest_count = count

    return results

if __name__ == "__main__":
    try:
        result = analyze_logs(PATH)
        pprint.pprint(result, indent=4)
    except FileNotFoundError:
        print(f"The log file at {PATH} can't be found or does not exist")



