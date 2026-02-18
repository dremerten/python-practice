"""
CODE CHALLENGE: System Log Analysis (No Regex)

You are given a system log file where each line follows this format:

    [timestamp] [service] [log_level] - [message]

Example:
    [2026-03-01 14:22:10] [payments] [ERROR] - Payment gateway timeout
    [2026-03-01 14:22:11] [auth]     [WARNING] - Token is about to expire

LOG LEVELS MAY INCLUDE (not limited to):
    INFO, DEBUG, WARNING, ERROR, TRACE

TASK:

Write a function that reads the log file and returns a dictionary with:

1. Counts of WARNING and ERROR logs PER SERVICE.
2. A dictionary of ERROR message frequencies across ALL services.
3. The most frequent ERROR message across ALL services.

FUNCTION SIGNATURE:

    def analyze_logs(path: str) -> dict:

EXPECTED RETURN FORMAT:

    {
        "service_counts": {
            "<service_name>": {
                "ERROR": int,
                "WARNING": int
            },
            ...
        },
        "most_common_error": str | None,
        "error_messages": {
            "<error_message>": int,
            ...
        }
    }

CONSTRAINTS:

- Use Python 3
- Do NOT use regular expressions
- Use only basic string methods: split(), split(maxsplit=1), strip()
- Read the file line by line (do not load the whole file into memory)
- Handle malformed lines safely (skip lines that don’t match the format)
- Only count WARNING and ERROR logs (ignore other levels for counting)
- If there are no ERROR logs, "most_common_error" should be None

HINTS (OPTIONAL):

- Use: line.split(" - ", 1) to separate metadata from message
- The metadata contains timestamp (with a space), service, and log level
- Extract service and log level from the metadata using split() and indexing
- Update:
    - results["service_counts"][service]["ERROR"/"WARNING"]
    - results["error_messages"][message] (only for ERROR)
- After processing the file, scan results["error_messages"] to find the most common error message

"""

import pprint


def analyze_logs(path: str) -> dict:
    results = {
        "service_counts": {},
        "most_common_error": None,
        "error_messages": {}
    }

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" - ", 1)
            if len(parts) != 2:
                continue

            meta, message = parts

            meta_parts = meta.split()
            if len(meta_parts) < 4:
                continue

            service = meta_parts[2].strip("[]")
            log_level = meta_parts[3].strip("[]")

            if service not in results["service_counts"]:
                results["service_counts"][service] = {"ERROR": 0, "WARNING": 0}

            if log_level == "ERROR":
                results["service_counts"][service]["ERROR"] += 1
                results["error_messages"][message] = (
                    results["error_messages"].get(message, 0) + 1
                )

            elif log_level == "WARNING":
                results["service_counts"][service]["WARNING"] += 1

    # compute most common ERROR message
    highest_count = 0
    for msg, count in results["error_messages"].items():
        if count > highest_count:
            results["most_common_error"] = msg
            highest_count = count

    return results

    



  












result = analyze_logs("/home/andre/DevOps-Practice/python-practice/log_parsing_challenge/system.log")
pprint.pprint(result, indent=4)
