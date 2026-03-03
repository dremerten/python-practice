"""
SYSTEM LOG ANALYSIS — STEP-BY-STEP CHECKLIST

GOAL:
Read a log file line by line and:
- Count WARNING and ERROR logs per service
- Count ERROR message frequencies across all services
- Find the most common ERROR message (or None if no errors)

========================================================
1) FUNCTION SCAFFOLDING
--------------------------------------------------------
[ ] Define function: analyze_logs(path: str) -> dict
[ ] Initialize results dictionary with:
    {
        "service_counts": {},
        "error_messages": {},
        "most_common_error": None
    }

========================================================
2) FILE HANDLING
--------------------------------------------------------
[ ] Open file using: with open(path, "r") as f
[ ] Iterate line by line: for line in f
[ ] Strip whitespace: line = line.strip()
[ ] Skip empty lines

========================================================
3) SPLIT METADATA FROM MESSAGE
--------------------------------------------------------
Log format:
[timestamp] [service] [log_level] - message

[ ] Split line using: line.split(" - ", 1)
[ ] If split does NOT return 2 parts → skip line
[ ] meta = left side (strip whitespace)
[ ] message = right side (strip whitespace)

========================================================
4) PARSE METADATA (NO REGEX)
--------------------------------------------------------
Example meta:
[2026-03-01 14:22:10] [payments] [ERROR]

[ ] Split meta using: meta.split()
[ ] Expect at least 4 tokens (timestamp has a space)
[ ] If fewer than 4 tokens → skip line
[ ] Extract:
    - service token at index 2
    - log level token at index 3
[ ] Strip brackets using .strip("[]")
[ ] If service or level is empty → skip line

========================================================
5) FILTER LOG LEVELS
--------------------------------------------------------
[ ] Only process log levels:
    - WARNING
    - ERROR
[ ] Ignore all other log levels (INFO, DEBUG, TRACE, etc.)

========================================================
6) UPDATE SERVICE COUNTS
--------------------------------------------------------
[ ] If service not in results["service_counts"]:
    initialize:
        {
            "ERROR": 0,
            "WARNING": 0
        }
[ ] Increment correct counter for the service

========================================================
7) TRACK ERROR MESSAGE FREQUENCIES
--------------------------------------------------------
[ ] Only for log level == "ERROR":
    - Increment results["error_messages"][message]
    - Use .get(message, 0) to avoid KeyError

========================================================
8) HANDLE MALFORMED LINES SAFELY
--------------------------------------------------------
[ ] Never crash on bad input
[ ] Skip lines that:
    - Don’t split correctly
    - Have missing tokens
    - Have empty service or level

========================================================
9) FIND MOST COMMON ERROR MESSAGE

[ ] Initialize highest_count = 0
[ ] Iterate over results["error_messages"].items()
[ ] For each (message, count):
    [ ] Compare count to highest_count
    [ ] If count is greater:
        [ ] Update results["most_common_error"] to this message
        [ ] Update highest_count to this count
========================================================
10) FINALIZE AND RETURN
--------------------------------------------------------
[ ] Return results dictionary
========================================================
"""

import pprint

FILE="/home/andre/DevOps-Practice/python-practice/log_parsing_challenge/system.log"

def analyze_logs(path: str) -> dict:
    results = {
        "service_counts": {},
        "error_messages": {},
        "most_common_error": None
    }
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line is None:
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
                results["error_messages"][message] = results["error_messages"].get(message, 0) +1
            
            if log_level == "WARNING":
                results["service_counts"][service]["WARNING"] += 1

    highest_count = 0
    for message, count in results["error_messages"].items():
        if count > highest_count:
            results["most_common_error"] = message
            highest_count = count
    return results


result = analyze_logs(FILE)
pprint.pprint(result, indent=4)