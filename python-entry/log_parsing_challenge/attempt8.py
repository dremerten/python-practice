"""
SYSTEM LOG ANALYSIS — STEP-BY-STEP CHECKLIST

GOAL:
Read a log file line by line and:
- Count WARNING and ERROR logs per service
- Count ERROR message frequencies across all services
- Find the most common ERROR message (or None if no errors)

Log format:
[timestamp] [service] [log_level] - message

========================================================
1) FUNCTION SCAFFOLDING
--------------------------------------------------------
[ ] Define function: analyze_logs(path: str) -> dict
[ ] Initialize results dictionary with:
    {
        "service_type_counts": {},
        "error_message_counts": {},
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
[ ] If service not in results["service_type_counts"]:
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
    - Increment results["error_message_counts"][message]
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
[ ] Iterate over results["error_message_counts"].items()
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
import json
import time

FILE="/home/andre/DevOps-Practice/python-practice/log_parsing_challenge/system.log"

def analyze_logs(path: str) -> dict:
    results = {
        "service_type_counts": {},
        "error_message_counts": {},
        "most_common_error": None
    }
    time.sleep(0.5)

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" - ", 1)
            if len(parts) != 2:
                continue
            header, message = parts
            header = header.split()
            if len(header) < 4:
                continue

            service = header[2].strip("[]")
            log_level = header[3].strip("[]")
            
            # check if service key exists in results["service_type_counts"] if not then create it
            results["service_type_counts"].setdefault(service, {"INFO": 0, "WARNING": 0, "DEBUG": 0, "ERROR": 0, "TRACE":0})
            results["service_type_counts"][service][log_level] += 1

            if log_level == "ERROR":
                results["service_type_counts"][service][log_level]
                results["error_message_counts"][message] = results["error_message_counts"].get(message, 0) + 1

    highest_count = 0
    for message, count in results["error_message_counts"].items():
        if count > highest_count:
            highest_count = count
            results["most_common_error"] = message
    
    return results
  
results = analyze_logs(FILE)
pprint.pprint(results, indent=4)
